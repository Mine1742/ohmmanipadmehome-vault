# Deploy containers to Azure App Service

Azure App Service runs custom Linux containers as web applications. You provide a container image from a registry, and App Service handles provisioning, load balancing, and scaling. 

## Container image sources

When you create a Web App for Containers, you select an image source that tells App Service where to pull your container image. The Azure portal presents two options:

- **Azure Container Registry (ACR)** is the recommended source for production workloads. ACR integrates with Microsoft Entra ID for authentication and supports managed identity, geo-replication, image scanning, and private network access. When you select ACR, you choose the specific registry, authentication method, image name, and tag.
- **Other container registries** includes any registry accessible via HTTPS that supports the Docker Registry HTTP API V2 specification. This option covers Docker Hub, GitHub Container Registry, and self-hosted registries. For private images, you provide the server URL, username, and password. Public images require only the image name.

## Deploy using the Azure portal

The Azure portal provides a guided experience for creating a Web App for Containers. This approach works well when you want to configure all settings visually and verify your choices before deployment.

### Create the web app

1. In the Azure portal, select **Create a resource** and search for **Web App**
2. Select **Create** and choose **Web App**
3. On the **Basics** tab, configure subscription, resource group, app name, and region
4. For **Publish**, select **Container**
5. For **Operating System**, select **Linux**
6. Select an App Service plan or create a new one
7. Select the **Container** tab to configure the image source

### Configure the container image

On the **Container** tab, you specify where App Service pulls your container image.

**For Azure Container Registry:**

1. In **Image Source**, select **Azure Container Registry**
2. Select your **Registry** from the dropdown (registries in the same subscription appear automatically)
3. Choose an **Authentication** method:
    - **Managed Identity**: Select an existing user-assigned managed identity, or use the system-assigned identity. The identity must have the AcrPull role on the registry.
    - **Admin credentials**: Use the registry's admin username and password. You must enable the admin user on the ACR.
4. Select the **Image** and **Tag** to deploy

**For other registries:**

1. In **Image Source**, select **Other container registries**
2. For private images, provide the **Server URL** (for example, `https://index.docker.io/v1/` for Docker Hub)
3. Enter **Username** and **Password** for private registries
4. Enter the **Full Image Name and Tag** (for example, `nginx:latest` or `myuser/myapp:v1`)

## ACR authentication options

Azure Container Registry supports two authentication methods when deploying to App Service: managed identity, or admin credentials. Your choice depends on security requirements and whether you manage your own infrastructure permissions.

### Managed identity authentication

Managed identity is the recommended approach for production. App Service authenticates to ACR using an Azure identity rather than stored credentials. This approach eliminates credential rotation concerns and provides better security auditing.

There are two kinds of managed identity:

- **System-assigned managed identity** is tied to the web app lifecycle. Azure creates the identity when you enable it on the web app and deletes it when you delete the app. This option is simpler when the web app is the only resource that needs the identity.
- **User-assigned managed identity** exists independently of the web app. You create the identity as a separate Azure resource and assign it to one or more web apps. This option works well when multiple apps need the same registry access or when you want to configure permissions before creating the web app.

### Admin credentials authentication

Admin credentials use a username and password stored in the ACR. This approach is simpler for development scenarios because it doesn't require role assignments. However, it stores credentials in your App Service configuration and requires manual rotation if compromised.

To use admin credentials, enable the admin user on your container registry:

Azure CLI

```
az acr update --name myregistry --admin-enabled true
```

## Deploy to App Service using CLI

You can deploy a container to App Service from the command line when you want a repeatable workflow that you can paste into a script or CI pipeline. This section assumes your container image already exists in Azure Container Registry and that App Service already has permission to pull it. In practice, that permission is often provided through managed identity and an AcrPull role assignment applied by a platform team.

### Create the web app

The `az webapp create` command creates the web app and sets the container image in one step. This example assumes the resource group and App Service plan already exist. Use your ACR login server and image name, including a tag, so the deployment is deterministic.

Azure CLI

```
az webapp create \
    --resource-group myResourceGroup \
    --plan myAppServicePlan \
    --name myDocumentProcessor \
    --container-image-name myregistry.azurecr.io/docprocessor:v1
```

## Deploy from other container registries

For registries other than ACR, provide the server URL and credentials when creating the web app. This approach works for Docker Hub, GitHub Container Registry, and self-hosted registries.

**Public images from Docker Hub:**

Azure CLI

```
az webapp create \
    --resource-group myResourceGroup \
    --plan myAppServicePlan \
    --name myWebApp \
    --container-image-name nginx \
    --docker-registry-server-url https://index.docker.io/v1/
```

**Private images:**

Azure CLI

```
az webapp create \
    --resource-group myResourceGroup \
    --plan myAppServicePlan \
    --name myWebApp \
    --container-image-name myusername/myapp:latest \
    --docker-registry-server-url https://index.docker.io/v1/ \
    --docker-registry-server-user myusername \
    --docker-registry-server-password <password>
```

For GitHub Container Registry, use `https://ghcr.io` as the server URL.

## Deploy using VS Code

VS Code with the Docker and Azure App Service extensions provides an interactive deployment experience. This approach works well during development when you want visual feedback and quick iteration.

1. Build your image locally using the Docker extension
2. Push the image to your container registry
3. In the Docker extension's REGISTRIES view, right-click the image tag and select **Deploy Image to Azure App Service**
4. Follow the prompts to select subscription, app name, resource group, and App Service plan

The extension can help you create the web app and deploy the selected image. For production deployments, validate registry authentication and role assignments separately so the app can reliably pull the image.

## Update the container image

When you deploy a new version of your application to ACR, update the container image reference. App Service restarts the web app, which stops and starts the container on each instance so the app runs the new image.

Azure CLI

```
az webapp config container set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --container-image-name myregistry.azurecr.io/docprocessor:v2
```

## Enable continuous deployment

For automated deployments, configure App Service to pull new images automatically when you push to the registry. This approach works well with CI/CD pipelines.

Enable continuous deployment:

Azure CLI

```
az webapp deployment container config \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --enable-cd true
```

This command returns a webhook URL. Configure your container registry to call this webhook when new images are pushed. For ACR, create a webhook in the registry settings that triggers on push events.

## Image pull behavior

Understanding when App Service pulls images helps you plan for deployment scenarios and troubleshoot issues.

- **Initial deployment:** App Service pulls all image layers when you first deploy the container or change the image reference.
    
- **App restart:** On restart, App Service checks for changes and pulls only modified layers. If the image is unchanged, the cached layers are used.
    
- **Scale out:** When App Service adds new instances, each instance pulls the image. New instances might need to pull the full image if layers aren't cached on the underlying infrastructure.
    
- **Pricing tier changes:** Moving to a different pricing tier might allocate new infrastructure, which pulls the image fresh and can affect startup time.
    

## Verify the deployment

After deploying a container, verify that the application starts successfully:

Azure CLI

```
az webapp show \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --query defaultHostName \
    --output tsv
```

Open the URL in a browser or use curl to verify the application responds. If the container fails to start, the diagnostic tools covered in Unit 5 help identify the issue.

## Additional resources

- [Deploy and run a containerized web app with Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-custom-container)
- [Use a custom container in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container)
- [Configure a custom container for Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container)
- [Azure Container Registry documentation](https://learn.microsoft.com/en-us/azure/container-registry/)


# Configure container runtime behavior


Container runtime settings control how App Service executes your container. These settings affect container startup, network configuration, file system behavior, and health monitoring. Configuring these settings correctly ensures your application starts reliably and performs well under load.

## Startup commands

App Service runs containers using the entrypoint and command defined in the Dockerfile. You can override these defaults with a custom startup command when you need to pass runtime arguments, run initialization scripts, or modify the container's default behavior.

Common scenarios for custom startup commands include:

- Passing environment-specific arguments to the application
- Running database migrations before starting the application
- Starting multiple processes within the container
- Overriding default framework configurations

Configure a startup command using the Azure CLI:

Azure CLI

```
az webapp config set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --startup-file "gunicorn --bind=0.0.0.0:8000 --workers=4 app:application"
```

The startup command replaces the CMD instruction from your Dockerfile. The ENTRYPOINT remains unchanged unless you modify the container configuration directly.

For containers that require shell processing, prefix the command with the shell:

Azure CLI

```
az webapp config set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --startup-file "/bin/bash -c 'python migrate.py && gunicorn app:application'"
```

## Port configuration

App Service needs to know which port inside your container receives HTTP requests. For custom containers, App Service can automatically route traffic when your container listens on port 80 or 8080. If your container listens on a different port, configure the `WEBSITES_PORT` app setting so App Service forwards requests to the correct port.

Azure CLI

```
az webapp config appsettings set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --settings WEBSITES_PORT=8000
```

App Service routes all incoming HTTP and HTTPS traffic to the specified port. The platform handles TLS termination before traffic reaches your container, so your container receives HTTP traffic even when clients connect over HTTPS.

App Service supports exposing only one port for HTTP requests to a custom container.

Common port configurations:

|Framework|Default Port|Setting|
|---|---|---|
|Node.js (Express)|3000|`WEBSITES_PORT=3000`|
|Python (Gunicorn)|8000|`WEBSITES_PORT=8000`|
|Java (Spring Boot)|8080|`WEBSITES_PORT=8080`|
|ASP.NET Core|80|No change needed|

## Persistent storage

By default, writes to the container file system are ephemeral. Data written to the file system is lost when the app restarts or moves to different infrastructure. This behavior matches standard container expectations but requires explicit planning when your application needs persistent files.

App Service can mount persistent storage at `/home` for Linux custom containers. Persistent storage is disabled by default for Linux custom containers. When this storage is enabled, files written to `/home` survive app restarts and are shared across all instances of a scaled-out app.

Enable persistent storage by setting the `WEBSITES_ENABLE_APP_SERVICE_STORAGE` app setting to `true`:

Azure CLI

```
az webapp config appsettings set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --settings WEBSITES_ENABLE_APP_SERVICE_STORAGE=true
```

With this setting enabled:

- The `/home` directory persists across container restarts
- All instances in a scaled-out app share the same `/home` content
- The `/home/LogFiles` directory stores container and application logs

Configure your application to write persistent data to `/home` or a subdirectory. For example, a document processing service might write processed output to `/home/output/`.

Storage capacity depends on your App Service plan. The storage quota is shared across all apps in the plan. For applications requiring large storage volumes or high I/O performance, consider mounting Azure Storage as an extra volume.

## Always-on

App Service apps can become idle after about 20 minutes of inactivity. The next request triggers a cold start, which means App Service has to start the app again and wait for it to become ready. Cold starts can take several seconds to minutes depending on image size, dependency initialization, and application startup time.

Enable always-on to keep your application loaded continuously:

Azure CLI

```
az webapp config set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --always-on true
```

With always-on enabled, App Service sends periodic requests to keep the application warm. This configuration eliminates cold start latency but requires the Basic pricing tier or higher.

Always-on is recommended for:

- Production applications where response time matters
- Applications with long startup times
- Containers with large images that take time to pull
- Services that maintain background processes or connections

## Health checks

Health checks monitor container responsiveness and automatically restart unhealthy instances. App Service sends HTTP requests to a specified path and evaluates the response to determine container health.

Configure a health check path:

Azure CLI

```
az webapp config set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --generic-configurations '{"healthCheckPath": "/health"}'
```

Your application should implement a health endpoint that returns an HTTP 200 status code when healthy. The endpoint can perform checks such as:

- Verifying database connectivity
- Confirming required services are reachable
- Checking available memory or disk space

App Service pings the health check path every minute. If an instance repeatedly fails (by default, after 10 failed pings), App Service removes that instance from the load balancer rotation. If the instance remains unhealthy for an extended period, App Service can replace it.

Health check configuration changes restart your app, so apply changes carefully in production.

A simple health endpoint implementation returns a 200 status when the application can handle requests:

Python

```
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200
```

For more sophisticated checks, verify dependencies and return appropriate status codes:

Python

```
@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.execute('SELECT 1')
        # Check storage access
        storage.list_containers()
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 503
```

## Additional resources

- [Configure a custom container for Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container)
- [Health check monitoring in App Service](https://learn.microsoft.com/en-us/azure/app-service/monitor-instances-health-check)
- [Mount Azure Storage as a local share](https://learn.microsoft.com/en-us/azure/app-service/configure-connect-to-azure-storage)
# Configure application settings

Application settings provide configuration values to your containerized application at runtime. App Service injects these values as environment variables when the container starts. Using app settings instead of hardcoded values allows you to deploy the same container image across different environments with environment-specific configuration.

## App settings

App settings are name-value pairs that App Service injects as environment variables. Your application reads these values using standard environment variable access methods for your programming language.

Create or update app settings using the Azure CLI:

Azure CLI

```
az webapp config appsettings set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --settings \
        STORAGE_ACCOUNT_NAME=mystorageaccount \
        LOG_LEVEL=INFO \
        MAX_DOCUMENT_SIZE_MB=50
```

Your application accesses these values as environment variables:

Python

```
import os

storage_account = os.environ.get('STORAGE_ACCOUNT_NAME')
log_level = os.environ.get('LOG_LEVEL', 'WARNING')
max_size = int(os.environ.get('MAX_DOCUMENT_SIZE_MB', 10))
```

All app settings are encrypted at rest. App Service stores settings in encrypted form and decrypts them only when injecting them into the container environment. This encryption applies to all settings regardless of whether they contain sensitive data.

App setting names can contain only letters, numbers, and underscores. For Linux containers, nested configuration keys that use colons in .NET applications should use double underscores instead. For example, `ConnectionStrings:DefaultConnection` becomes `ConnectionStrings__DefaultConnection`.

## Connection strings

Connection strings are a specialized form of app settings designed for database connectivity. App Service prefixes connection string environment variables with a type identifier that indicates the database type.

Configure a connection string:

Azure CLI

```
az webapp config connection-string set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --connection-string-type SQLAzure \
    --settings DefaultConnection="Server=myserver.database.windows.net;Database=mydb;..."
```

The connection string is available as an environment variable with a type prefix:

|Type|Environment Variable Prefix|
|---|---|
|SQL Server|`SQLCONNSTR_`|
|SQL Azure|`SQLAZURECONNSTR_`|
|MySQL|`MYSQLCONNSTR_`|
|PostgreSQL|`POSTGRESQLCONNSTR_`|
|Custom|`CUSTOMCONNSTR_`|

For the previous example, the environment variable name is `SQLAZURECONNSTR_DefaultConnection`.

For non-.NET applications, app settings are typically simpler than connection strings. The type prefix adds complexity without providing benefits for frameworks that don't expect the prefixed format. Use app settings for database connections in Python, Node.js, and similar runtimes.

## Bulk editing

When configuring many settings, bulk editing is more efficient than individual commands. You can export settings as JSON, modify them, and import the updated configuration.

Export current settings:

Azure CLI

```
az webapp config appsettings list \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --output json > settings.json
```

The exported JSON contains an array of setting objects:

JSON

```
[
  {
    "name": "STORAGE_ACCOUNT_NAME",
    "value": "mystorageaccount",
    "slotSetting": false
  },
  {
    "name": "LOG_LEVEL",
    "value": "INFO",
    "slotSetting": false
  }
]
```

Edit the file and import the updated settings. You can also pass JSON directly to the CLI using the `@` prefix to read from a file:

Azure CLI

```
az webapp config appsettings set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --settings @settings.json
```

In the Azure portal, the Environment variables option provides an Advanced edit option that displays settings in JSON format for bulk modifications.

## Slot settings

Deployment slots allow you to run different versions of your application side-by-side within the same App Service plan. Each slot has its own hostname and configuration, but it shares the underlying compute resources of the plan with the production slot. You can swap slots to promote changes from staging to production.

Some settings should stay with the slot rather than swapping with the application code. Mark these settings as slot settings:

Azure CLI

```
az webapp config appsettings set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --slot staging \
    --slot-settings \
        ENVIRONMENT=staging \
        API_ENDPOINT=https://api-staging.example.com
```

Settings marked as slot settings remain with the slot during swap operations. This behavior is important for:

- **Environment identifiers:** Settings like `ENVIRONMENT=production` shouldn't swap to staging
- **Environment-specific endpoints:** API URLs or database connections that differ between environments
- **Feature flags:** Settings that enable features only in specific environments
- **Diagnostic settings:** Verbose logging in staging that shouldn't affect production

View which settings are configured as slot settings:

Azure CLI

```
az webapp config appsettings list \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --query "[?slotSetting==\`true\`].name"
```

## Key Vault references

For secrets that require centralized management, audit trails, or automatic rotation, App Service supports referencing values stored in Azure Key Vault. The application reads resolved values as standard environment variables without code changes.

A Key Vault reference uses special syntax in the app setting value:

Azure CLI

```
az webapp config appsettings set \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --settings \
        API_KEY="@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/api-key)"
```

App Service resolves the reference and injects the secret value as the `API_KEY` environment variable. Your application code reads `API_KEY` without knowing the value came from Key Vault.

Key Vault references require:

- A managed identity enabled on the web app
- The managed identity granted access to read secrets from the Key Vault
- The Key Vault reference syntax in the app setting value

References without a version specifier automatically resolve to the latest secret version. When a secret rotates, App Service refreshes resolved values within 24 hours. Any configuration change that triggers an app restart also forces an immediate refetch of referenced secrets.

Key Vault integration is outside the scope of this module but provides important capabilities for production secrets management. See the additional resources for detailed configuration guidance.

## Verify configuration

After configuring settings, verify that the app is resolving and applying the expected values. For App Service, the SCM (Kudu) site provides a convenient view of configuration and diagnostics.

Access the SCM site at `https://<app-name>.scm.azurewebsites.net` and navigate to **Environment** (or browse to `https://<app-name>.scm.azurewebsites.net/Env`) to view environment variables that App Service applies to the app. This view shows both your app settings and system-provided variables.

You can also verify settings programmatically by adding a diagnostic endpoint to your application that returns nonsensitive configuration values, or by checking application logs for configuration-related messages at startup.

## Additional resources

- [Configure app settings in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/configure-common)
- [Use Key Vault references as app settings](https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references)
- [Set up staging environments in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots)
# Observe and troubleshoot containerized apps

App Service provides diagnostic tools for monitoring container health, viewing logs, and troubleshooting issues. Understanding these tools helps you identify problems quickly and maintain reliable production deployments.

## Container logs

App Service captures output from your container's stdout and stderr streams. This output includes application logs, framework messages, and error output. Enable container logging to persist these logs and make them available through the portal and CLI.

Enable container logging:

Azure CLI

```
az webapp log config \
    --resource-group myResourceGroup \
    --name myDocumentProcessor \
    --docker-container-logging filesystem
```

The `filesystem` option stores logs in the App Service file system. Logs are available at `/home/LogFiles/` and through the diagnostic tools described in this unit.

Container logs capture several types of output:

- **Application output:** Messages your application writes to stdout
- **Error output:** Exception traces and error messages written to stderr
- **Framework logs:** Web server startup messages, request logs, and framework diagnostics
- **Platform messages:** App Service messages about container lifecycle events

Configure your application to write meaningful log output to stdout. Most logging frameworks support console output that App Service captures automatically.

## Log stream

The log stream provides real-time access to container output. This tool is useful for debugging startup issues, monitoring live traffic, and observing application behavior during testing.

Stream logs using the Azure CLI:

Azure CLI

```
az webapp log tail \
    --resource-group myResourceGroup \
    --name myDocumentProcessor
```

The log stream displays new log entries as they appear. Press Ctrl+C to stop streaming.

In the Azure portal, navigate to your web app and select **Log stream** under **Monitoring**. The portal displays the same real-time log output in a browser-based viewer.

The log stream shows output from all instances in a scaled-out app. Each line includes an instance identifier to help you correlate logs across instances.

## Diagnostic console (Kudu)

Kudu (the SCM site) is the advanced diagnostic console for App Service. It provides access to app configuration views, log files in mounted storage, and diagnostic endpoints. Access the SCM site at:

```
https://<app-name>.scm.azurewebsites.net
```

The SCM site runs as a separate site for your app and requires authentication with credentials that can manage your web app.

Key Kudu features for container troubleshooting:

- **Environment variables:** The Environment page displays all environment variables available to your container. This view helps verify that app settings are configured correctly and shows system-provided variables.
    
- **File system browser:** The Debug console provides access to files in the mounted storage paths (such as `/home`). Browse log files at `/home/LogFiles/` and inspect any content you write to `/home`.
    
- **Limitations:** The SCM site isn't the same environment as your app container, so it doesn't let you browse the full container file system or inspect running processes inside the app container. Use SSH (when enabled in your image) for in-container inspection.
    
- **Diagnostic dump:** Download a ZIP file containing log files, configuration, and diagnostic information. This dump is useful for offline analysis or sharing with support.
    

## Platform diagnostics

For long-term log retention and advanced analysis, configure diagnostic settings to send logs to Azure Monitor, Event Hubs, or storage accounts.

Configure diagnostic settings to send logs to a Log Analytics workspace:

Azure CLI

```
resourceId=$(az webapp show -g myResourceGroup -n myDocumentProcessor --query id -o tsv)
workspaceId=$(az monitor log-analytics workspace show -g myResourceGroup -n myLogAnalyticsWorkspace --query id -o tsv)

az monitor diagnostic-settings create \
    --resource "$resourceId" \
    --name myDiagnosticSettings \
    --workspace "$workspaceId" \
    --logs '[{"category":"AppServiceConsoleLogs","enabled":true},{"category":"AppServiceHTTPLogs","enabled":true}]'
```

Available log categories for containerized apps include:

|Category|Description|
|---|---|
|AppServiceConsoleLogs|Container stdout and stderr output|
|AppServiceHTTPLogs|HTTP request and response information|
|AppServicePlatformLogs|Container lifecycle events and platform messages|
|AppServiceAppLogs|Application-level logs (when configured)|

With logs flowing to Log Analytics, you can write queries to analyze patterns, create alerts, and build dashboards. For example, query recent errors:

Kusto

```
AppServiceConsoleLogs
| where Level == "Error"
| where TimeGenerated > ago(1h)
| project TimeGenerated, ResultDescription
| order by TimeGenerated desc
```

## SSH access

For interactive troubleshooting, you can connect to a running container using SSH. This capability requires SSH to be enabled in your container image.

Configure your container to support SSH by including the OpenSSH server and configuring it to listen on port 2222. The container must:

1. Install the `openssh-server` package
2. Configure SSH to listen on port 2222
3. Set the root password to `Docker!` (required by App Service)
4. Start the SSH daemon alongside your application

Example Dockerfile additions for SSH support:

Dockerfile

```
RUN apt-get update && apt-get install -y openssh-server \
    && echo "root:Docker!" | chpasswd

COPY sshd_config /etc/ssh/

EXPOSE 8000 2222

CMD ["/bin/bash", "-c", "service ssh start && gunicorn app:application"]
```

After configuring SSH in your container, access the SSH console through the Azure portal by navigating to your web app and selecting **SSH** under **Development Tools**.

## Common issues and solutions

Understanding common container deployment issues helps you troubleshoot problems efficiently.

### Container fails to start

**Symptoms:** The application URL returns an error, and container logs show startup failures.

**Diagnosis:**

1. Check container logs for application errors using the log stream
2. Verify the image exists in the registry and credentials are correct
3. Confirm the container runs locally with the same configuration

**Common causes:**

- Missing environment variables that the application requires at startup
- Port mismatch between `WEBSITES_PORT` and the port the container listens on
- Application crashes during initialization due to missing dependencies

### 404 responses after deployment

**Symptoms:** The container appears to start, but requests return 404 Not Found errors.

**Diagnosis:**

1. Verify `WEBSITES_PORT` matches the port your application listens on
2. Check that the application binds to `0.0.0.0` rather than `localhost`
3. Confirm the application serves requests at the root path or expected routes

**Common causes:**

- Application listening on localhost instead of all interfaces
- Incorrect port configuration
- Application routing not configured for the expected paths

### Missing environment variables

**Symptoms:** The application logs errors about missing configuration or undefined values.

**Diagnosis:**

1. Verify app settings are saved in the portal or CLI
2. Check environment variables in Kudu to confirm injection
3. If you use SSH for troubleshooting, verify variables using the SCM `/Env` view when shell output seems incomplete

**Common causes:**

- Settings not saved after editing
- Typos in setting names
- Application checking for variables before App Service injects them

### Slow cold starts

**Symptoms:** First requests after idle periods take longer than subsequent requests.

**Diagnosis:**

1. Check container image size using `docker images`
2. Review application startup time in logs
3. Verify always-on setting

**Solutions:**

- Enable always-on to keep the application warm
- Reduce container image size by using smaller base images and multi-stage builds
- Optimize application startup by deferring heavy initialization

## Additional resources

- [Enable diagnostic logging for apps in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs)
- [Troubleshoot an app in Azure App Service using Visual Studio](https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-dotnet-visual-studio)
- [Azure App Service diagnostics overview](https://learn.microsoft.com/en-us/azure/app-service/overview-diagnostics)
- - [Configure a custom container for Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container) provides comprehensive documentation for all container configuration options including advanced scenarios.
    
- [Use Key Vault references as app settings](https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references) explains how to integrate Azure Key Vault for centralized secrets management with automatic rotation.
    
- [Enable diagnostic logging for apps in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs) covers all logging options including Azure Monitor integration for long-term retention and analysis.
    
- [Tutorial: Migrate custom software to Azure App Service using a custom container](https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container) walks through containerizing an existing application and deploying it to App Service.