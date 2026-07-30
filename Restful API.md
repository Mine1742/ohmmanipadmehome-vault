
A RESTful API is a **structured way for one system to ask another system to do something with data**.

Not run code.  
Not open a UI.  
Just: _create, read, update, or delete_ data over the network in a predictable way.

Think of REST as **remote file + record management**, not “programming.”

### 1. Everything is a _resource_

A resource is a **thing**, not an action.

Examples:

- a user
    
- a VM
    
- a ticket
    
- a PDF document
    
- a Bluebeam markup
    
- an Azure resource group
    

Each resource has a **unique address (URL)**.
### 2. The HTTP verb is the verb

REST splits **what** from **what you want to do with it**.

| HTTP Verb | Meaning (human language) |
| --------- | ------------------------ |
| GET       | “Show me this”           |
| POST      | “Create a new one”       |
| PUT       | “Replace this entirely”  |
| PATCH     | “Change part of this”    |
| DELETE    | “Remove this”            |

### 3. Requests are stateless

Each request must contain **everything needed to understand it**.

No memory.  
No “we talked earlier.”  
No session context assumed.

That means:

- authentication is sent every time (tokens, keys)
    
- parameters are explicit
    
- the server doesn’t “remember” you unless you give it an ID
    

This is why REST scales so well.

## What actually happens in a REST call (step-by-step)

Let’s walk a real example.

### Scenario: Get VM info from Azure

1. **Client** (CLI, script, app) sends a request:
    

`GET https://management.azure.com/subscriptions/{id}/resourceGroups/rg1/providers/Microsoft.Compute/virtualMachines/vm1?api-version=2023-03-01`

Headers:

`Authorization: Bearer <token>`

2. **Server**:
    

- checks the token
    
- checks permissions (RBAC)
    
- locates the resource
    
- returns data
    

3. **Response**:
    

`200 OK`

Body (JSON):

`{   "name": "vm1",   "location": "eastus",   "properties": {     "hardwareProfile": {...},     "osProfile": {...}   } }`

No UI.  
No buttons.  
Just structured data.

---

## JSON is the language of REST

REST doesn’t _require_ JSON, but in modern systems it’s the default.

Think of JSON as:

- a **wire format**
    
- not code
    
- not logic
    
- just data with structure
    

Key idea:

> REST moves _state_, not _behavior_.

---

## Why REST exists at all

Before REST:

- tight coupling
    
- custom protocols
    
- brittle integrations
    
- massive vendor lock-in
    

REST solved:

- scalability
    
- interoperability
    
- automation
    
- infrastructure as code
    

That’s why:

- Azure ARM
    
- Microsoft Graph
    
- GitHub
    
- ServiceNow
    
- Jira
    
- CI/CD pipelines
    

are all REST under the hood.

Your CLI commands are **REST calls with training wheels**.

---

## CLI ↔ REST relationship (important for you)

When you run:

`az vm list`

You are **not** doing something magical.

You are doing:

- CLI formats a REST request
    
- sends it to Azure
    
- receives JSON
    
- prints it nicely
    

You could reproduce the same call with:

- curl
    
- PowerShell
    
- Python
    
- Postman
    

This is why AZ-204 cares about REST fluency.

---

## Real-world use cases (concrete)

### 1. Automation

- Create 100 users
    
- Rotate secrets
    
- Deploy infrastructure
    
- Pull reports
    

REST is the backbone of DevOps.

---

### 2. Tool integration

Bluebeam ↔ Revit ↔ SharePoint ↔ Azure

Each system:

- exposes resources
    
- allows CRUD operations
    
- authenticates requests
    

REST is the glue.

---

### 3. SaaS platforms

Anything with:

- web UI
    
- mobile app
    
- API
    

uses REST so multiple clients can talk to the same backend.

---

### 4. Monitoring & observability

- pull logs
    
- query metrics
    
- trigger alerts
    

Again: resources + verbs.

---

## Common misconceptions that block understanding

1. **“REST is programming”**  
    No. REST is a protocol contract.
    
2. **“Endpoints are functions”**  
    They’re nouns, not verbs.
    
3. **“APIs must be complicated”**  
    Most are boring CRUD with auth.
    
4. **“I need to memorize everything”**  
    You need patterns, not endpoints.
    

---

## The one-sentence summary that actually sticks

> REST is a standardized way to **name things**, **act on them**, and **exchange their state** over the network, without either side needing to know how the other is built.

---

## How to make this click permanently

The fastest way:

- take one API (Azure or GitHub)
    
- ignore the SDK
    
- make 3 calls manually:
    
    - GET
        
    - POST
        
    - DELETE
        

When you see the raw request and response, the abstraction collapses in a good way.