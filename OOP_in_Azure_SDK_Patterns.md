# OOP in the Azure SDK — How the Patterns Show Up in Real Code

---

## The Credential System — Interfaces and Polymorphism in Action

This is the cleanest example of OOP in the entire Azure SDK. Remember from our
managed identity discussion — you can swap credential types without changing any
other code. Here's WHY that works, from an OOP perspective.

### The Interface (Abstract Base Class)

Deep inside the Azure SDK, there's essentially this contract:

```python
# This is a simplified version of what the SDK defines
from abc import ABC, abstractmethod

class TokenCredential(ABC):
    """Any class that wants to be a credential MUST implement get_token()"""

    @abstractmethod
    def get_token(self, *scopes, **kwargs):
        """Return an access token for the given scopes."""
        pass
```

This is an INTERFACE — it doesn't do anything itself. It just says: "If you
want to be a credential, you must have a get_token() method that accepts scopes
and returns a token."

### The Implementations (Concrete Classes)

Each credential type is a CLASS that implements that interface:

```python
class ManagedIdentityCredential(TokenCredential):
    """Gets tokens from the IMDS endpoint (the managed identity flow we discussed)"""

    def __init__(self, client_id=None):
        # ATTRIBUTE — stored for later use in get_token()
        self.client_id = client_id
        self._endpoint = "http://169.254.169.254/metadata/identity/oauth2/token"

    def get_token(self, *scopes, **kwargs):
        # METHOD — calls IMDS, returns a token
        # Uses self._endpoint and self.client_id internally
        response = requests.get(self._endpoint, params={
            "resource": scopes[0],
            "client_id": self.client_id,
            "api-version": "2019-08-01"
        }, headers={"Metadata": "true"})
        data = response.json()
        return AccessToken(data["access_token"], data["expires_on"])


class ClientSecretCredential(TokenCredential):
    """Gets tokens using a client ID + secret (the old way with a password)"""

    def __init__(self, tenant_id, client_id, client_secret):
        # Different ATTRIBUTES than ManagedIdentityCredential
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self, *scopes, **kwargs):
        # Same METHOD NAME, completely different implementation
        # Posts to Entra ID token endpoint with client_id + secret
        response = requests.post(
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": scopes[0]
            }
        )
        data = response.json()
        return AccessToken(data["access_token"], data["expires_in"])


class DefaultAzureCredential(TokenCredential):
    """Tries multiple credential types in order until one works"""

    def __init__(self):
        # ATTRIBUTE — a list of other credential OBJECTS
        # This is called COMPOSITION — an object containing other objects
        self._credentials = [
            EnvironmentCredential(),        # check env vars first
            ManagedIdentityCredential(),    # then try managed identity
            AzureCliCredential(),           # then try az login
            # ... more fallbacks
        ]

    def get_token(self, *scopes, **kwargs):
        # Tries each credential in order
        for credential in self._credentials:
            try:
                return credential.get_token(*scopes, **kwargs)
            except Exception:
                continue
        raise Exception("No credential could authenticate")
```

### Why This Design Matters — Polymorphism

Every Azure service client accepts a `TokenCredential`. It doesn't care WHICH
credential you give it — it just calls `get_token()` on whatever you pass in:

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import (
    DefaultAzureCredential,
    ManagedIdentityCredential,
    ClientSecretCredential
)

# ALL THREE of these work identically with SecretClient
# because they all implement the TokenCredential interface

# Option 1: Managed identity (production on Azure)
cred = ManagedIdentityCredential()

# Option 2: Client secret (legacy or specific scenarios)
cred = ClientSecretCredential("tenant-id", "client-id", "secret")

# Option 3: Auto-detect (recommended)
cred = DefaultAzureCredential()

# SecretClient doesn't know or care which one you picked
# It just calls cred.get_token() when it needs a token
client = SecretClient(
    vault_url="https://my-vault.vault.azure.net",
    credential=cred   # ← accepts ANY TokenCredential
)
secret = client.get_secret("db-password")
```

This is POLYMORPHISM — "many forms." The `credential` parameter can take many
different shapes (classes), but they all respond to the same method call
(`get_token()`). SecretClient is coded against the INTERFACE, not against any
specific implementation.

This is why you can develop locally using DefaultAzureCredential (which falls
back to your `az login` session), then deploy to Azure where it automatically
picks up the managed identity — zero code changes.

---

## Service Clients — Classes as API Wrappers

Every Azure service in the SDK follows the same pattern: a CLIENT CLASS that
wraps REST API calls.

```python
from azure.keyvault.secrets import SecretClient

# CONSTRUCTOR — creates an instance with its configuration
client = SecretClient(
    vault_url="https://my-vault.vault.azure.net",
    credential=DefaultAzureCredential()
)

# METHODS — each one wraps a REST API call
secret = client.get_secret("db-password")          # GET request
client.set_secret("db-password", "new-value")       # PUT request
client.begin_delete_secret("old-secret")             # DELETE request
deleted = client.list_deleted_secrets()               # GET (list)

# The client OBJECT holds state:
# - vault_url (attribute) — so you don't pass it to every method
# - credential (attribute) — handles token refresh automatically
# - internal HTTP pipeline (attribute) — retry policies, logging, etc.
```

Compare this to doing it without a class (raw REST calls):

```python
# WITHOUT OOP — you manage everything yourself, every single call
token = get_token(credential, "https://vault.azure.net/.default")
response = requests.get(
    "https://my-vault.vault.azure.net/secrets/db-password",
    headers={"Authorization": f"Bearer {token}"},
    params={"api-version": "7.4"}
)
# Handle token expiry yourself
# Handle retries yourself
# Pass the vault URL every time
# Pass the API version every time
```

The class bundles all that repetitive state and behavior so you don't deal
with it on every call.

---

## The Pager Pattern — Objects That Behave Like Collections

When you list resources in Azure, you get paginated results. The SDK wraps
this in an iterable object:

```python
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url="https://my-vault.vault.azure.net",
                      credential=DefaultAzureCredential())

# list_properties_of_secrets() returns an ItemPaged OBJECT
# ItemPaged is a CLASS that implements the iterator protocol
secrets = client.list_properties_of_secrets()

# You can iterate it like a simple list
for secret in secrets:
    print(secret.name)
    print(secret.updated_on)

# But under the hood, the ItemPaged object is:
# 1. Making API calls to get pages of results
# 2. Following nextLink URLs automatically
# 3. Yielding individual items from each page
# 4. Only fetching the next page when you need it (lazy loading)
```

The ItemPaged class internally looks something like this:

```python
class ItemPaged:
    def __init__(self, command, **kwargs):
        self._command = command          # The API call to make
        self._page_iterator = None       # Current page of results
        self._continuation_token = None  # nextLink for pagination

    def __iter__(self):
        return self

    def __next__(self):
        # If current page is exhausted, fetch next page
        # If no more pages, raise StopIteration
        # Otherwise, return next item from current page
        ...
```

This is ENCAPSULATION — the complexity of pagination is hidden inside the
object. Your code just writes a simple for loop.

---

## Long-Running Operations — The Poller Pattern

Some Azure operations take minutes (creating a VM, deleting a Key Vault secret
with soft delete, training an ML model). The SDK uses a POLLER object:

```python
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url="https://my-vault.vault.azure.net",
                      credential=DefaultAzureCredential())

# begin_delete_secret() returns a POLLER OBJECT, not the result
poller = client.begin_delete_secret("my-secret")

# The poller is an OBJECT with methods to manage the async operation:
print(poller.status())      # "inProgress" / "succeeded" / "failed"
print(poller.done())        # True / False

# Block until the operation completes
result = poller.result()    # Waits and returns the final result
print(result.name)          # "my-secret"
print(result.deleted_date)  # when it was deleted

# Or poll manually
while not poller.done():
    poller.wait(timeout=5)  # wait 5 seconds between checks
    print(f"Status: {poller.status()}")
```

The poller object ENCAPSULATES:
- The operation ID returned by Azure
- The polling URL to check status
- Retry logic and backoff timing
- Deserialization of the final result

Without OOP, you'd manually track the operation URL, write a polling loop,
handle timeouts, and parse the response every time.

---

## Azure Functions Bindings — Seeing Classes as Data Containers

In Azure Functions (which you've been working with), the trigger and binding
objects are class instances:

```python
import azure.functions as func
import logging

app = func.FunctionApp()    # app is an OBJECT (instance of FunctionApp class)

@app.route(route="orders/{id}")
def get_order(req: func.HttpRequest) -> func.HttpResponse:
    #        ^^^                         ^^^
    #   HttpRequest is a CLASS      HttpResponse is a CLASS
    #   'req' is an OBJECT          return value is an OBJECT

    # HttpRequest ATTRIBUTES (data the object carries):
    order_id = req.route_params.get("id")     # from URL
    api_key = req.headers.get("X-Api-Key")    # from headers
    body = req.get_body()                      # raw bytes
    json_data = req.get_json()                 # parsed JSON

    # HttpRequest METHODS (behavior):
    params = req.params                 # query string dict
    body_str = req.get_body().decode()  # get body as string

    # Create and return an HttpResponse OBJECT
    return func.HttpResponse(
        body='{"status": "found"}',     # constructor argument
        status_code=200,                # constructor argument
        mimetype="application/json"     # constructor argument
    )


# Service Bus trigger — the message is also a class instance
@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="orders",
    connection="ServiceBusConn"
)
def process_order(msg: func.ServiceBusMessage):
    # ServiceBusMessage ATTRIBUTES and METHODS:
    body = msg.get_body().decode()
    message_id = msg.message_id             # attribute
    session_id = msg.session_id             # attribute
    custom_props = msg.application_properties  # attribute
    enqueued_time = msg.enqueued_time_utc   # attribute
```

Each of these (HttpRequest, HttpResponse, ServiceBusMessage) is a CLASS that
bundles related data and methods. The Azure Functions runtime creates OBJECTS
from these classes and passes them to your function.

---

## Cosmos DB — Full OOP Pattern in Practice

Here's a realistic AZ-204 exam scenario with Cosmos DB, showing multiple
OOP concepts working together:

```python
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential

# CONSTRUCTOR — creates the top-level client object
credential = DefaultAzureCredential()
cosmos_client = CosmosClient(
    url="https://my-cosmos.documents.azure.com:443/",
    credential=credential
)

# OBJECT HIERARCHY — each method returns a child object
# CosmosClient → DatabaseProxy → ContainerProxy
database = cosmos_client.get_database_client("orders-db")     # returns DatabaseProxy object
container = database.get_container_client("orders")            # returns ContainerProxy object

# ContainerProxy METHODS — CRUD operations
# Create (returns the created item as a dict)
new_order = container.create_item(body={
    "id": "order-001",
    "customerId": "cust-abc",        # partition key
    "items": ["widget-a", "widget-b"],
    "total": 49.99
})

# Read (need id AND partition key)
order = container.read_item(
    item="order-001",
    partition_key="cust-abc"
)

# Query (returns an ItemPaged object — the pager pattern from above)
query_results = container.query_items(
    query="SELECT * FROM orders o WHERE o.total > @min_total",
    parameters=[{"name": "@min_total", "value": 25.00}],
    partition_key="cust-abc"          # scoped to single partition = fast
)
for item in query_results:            # iterating the pager object
    print(item["id"], item["total"])

# Upsert (create or replace)
container.upsert_item(body={
    "id": "order-001",
    "customerId": "cust-abc",
    "items": ["widget-a", "widget-b", "widget-c"],  # updated
    "total": 74.99
})

# Delete
container.delete_item(item="order-001", partition_key="cust-abc")

# ERROR HANDLING — the SDK defines custom EXCEPTION CLASSES
# These inherit from Python's built-in Exception class
try:
    order = container.read_item(item="nonexistent", partition_key="cust-abc")
except exceptions.CosmosResourceNotFoundError as e:
    #                ^^^^^^^^^^^^^^^^^^^^^^^^^^
    # This is a CLASS that inherits from CosmosHttpResponseError
    # which inherits from Azure's HttpResponseError
    # which inherits from Python's Exception
    print(f"Status code: {e.status_code}")   # attribute: 404
    print(f"Message: {e.message}")            # attribute: "Entity not found"
```

### The Inheritance Chain for Exceptions

```
Python's BaseException
    └── Exception
        └── AzureError (azure.core)
            └── HttpResponseError
                └── CosmosHttpResponseError
                    ├── CosmosResourceNotFoundError  (404)
                    ├── CosmosResourceExistsError     (409)
                    ├── CosmosAccessConditionFailedError (412 — etag mismatch)
                    └── ... etc
```

Each level INHERITS attributes and behavior from its parent while adding
specifics. You can catch at any level:

```python
try:
    container.read_item(item="x", partition_key="y")

except exceptions.CosmosResourceNotFoundError:
    # Catches ONLY 404s — most specific
    print("Item doesn't exist")

except exceptions.CosmosHttpResponseError:
    # Catches any Cosmos error (404, 409, 429, etc.) — broader
    print("Some Cosmos error occurred")

except Exception:
    # Catches anything at all — broadest
    print("Something went wrong")
```

---

## Putting It All Together — The OOP Mental Map for Azure SDK

```
INTERFACE (TokenCredential)
    │
    ├── defines the CONTRACT: must have get_token()
    │
    ├── IMPLEMENTED BY (concrete classes):
    │   ├── DefaultAzureCredential
    │   ├── ManagedIdentityCredential
    │   ├── ClientSecretCredential
    │   └── ... more credential types
    │
    └── CONSUMED BY (service clients accept any TokenCredential):
        ├── SecretClient (Key Vault)
        ├── BlobServiceClient (Storage)
        ├── CosmosClient (Cosmos DB)
        ├── ServiceBusClient (Service Bus)
        └── EventHubConsumerClient (Event Hubs)

Each SERVICE CLIENT is a CLASS with:
    ├── CONSTRUCTOR: takes endpoint URL + credential
    ├── ATTRIBUTES: stores config, manages HTTP pipeline
    ├── METHODS: wrap REST API calls (CRUD operations)
    ├── Returns OBJECTS:
    │   ├── ItemPaged — for list operations (encapsulates pagination)
    │   ├── Poller — for long-running operations (encapsulates polling)
    │   └── Data objects — items, secrets, messages, etc.
    └── Raises EXCEPTION classes arranged in INHERITANCE hierarchy
```

Every time you see this in Azure SDK code:

```python
client = SomeServiceClient(url, credential)   # create an OBJECT from a CLASS
result = client.some_method(args)             # call a METHOD on the OBJECT
for item in client.list_things():             # iterate an ItemPaged OBJECT
poller = client.begin_long_operation()        # get a Poller OBJECT
result = poller.result()                      # call METHOD on Poller
```

...you're looking at OOP in action. The classes organize complexity so that
your code stays clean and the Azure SDK handles the HTTP plumbing, token
management, pagination, retries, and error typing behind the scenes.
