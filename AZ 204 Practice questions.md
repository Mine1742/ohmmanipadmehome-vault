Question I of 50
You manage a multiregion deployment of an Azure Cosmos DB account named accountl.
You need to configure the default consistency level for accountl. The consistency level must maximize throughput and minimize
latency for write operations.
Which consistency level should you use?
o
bounded staleness
o
consistent prefix
O eventual
V This answer is correct.
session
This answer is incorrect.
This item tests the candidate's knowledge of selecting the consistency level, which is part of developing Azure Cosmos DB solutions. The eventual consistency level maximizes throughput and minimizes latency. The bounded staleness consistency level provides lower throughput and higher latency comparing with the remaining answer choices. The consistent prefix consistency level provides higher throughput and lower latency for write operations than the session consistency level but lower throughput and higher latency than the eventual consistency levels. The session
consistency level provides higher throughput and lower latency for write operations than the bounded staleness consistency level but lower throughput and higher latency than the eventual and consistent prefix consistency levels. 


You need to create a container in a container group and mount an Azure file share as volume.
Which code segment should you use?
Select only one answer.

```
az container create -g MyResourceGroup --name myapp --image myimage:latest 
--command-line "cat /mnt/azfile/myfile"
--azure-file-volume-share-name myshare 
--azure-file-volume-account-name mystorageaccount 
--azure-file-volume-account-key mystoragekey 
--azure-file-volume-mount-path /mnt/azfile
```

**This answer is correct.**

```
az container create -g MyResourceGroup --name myapp --image myimage:latest
--command-line "cat /mnt/azfile/myfile"
--azure-file-volume-share-name myshare
--azure-file-volume-account-name mystorageaccount
--azure-file-volume-account-key mystoragekey
--secrets-mount-path /mnt/azfile
```

```
az container create -g MyResourceGroup –name myapp –image myimage:latest 
--command-line “cat /mnt/azfile/myfile”
--azure-file-volume-account-name mystorageaccount
--azure-file-volume-account-key mystoragekey 
--azure-file-volume-mount-path /mnt/azfile
```

```
az container create -g MyResourceGroup --name myapp --image myimage:latest 
--command-line "cat /mnt/azfile/myfile"
--azure-file-volume-account-name mystorageaccount
--azure-file-volume-account-key mystoragekey
--secrets-mount-path /mnt/azfile
```

This item tests the candidate’s knowledge of running containers by using Azure Container Instances.

The code segment that includes the `–azure-file-volume-mount-path` parameter and the `--azure-file-volume-share-name` parameter creates a container in a container group and mounts an Azure file share as volume.

The code segments that include the `--secrets-mount-path` parameter will not mount an Azure file share as volume. The code segment that does not include the `--azure-file-volume-share-name` is invalid.

[Mount an Azure file share in Azure Container Instances](https://learn.microsoft.com/en-us/training/modules/create-run-container-images-azure-container-instances/6-mount-azure-file-share-azure-container-instances)

Question 3 of 50
You are developing a .NET application that includes multiple container images. The application will be deployed to Azure
Container Instances (ACI).
You need to ensure that an Azure file share can be mapped to each container of the application.
Which configuration should you use?
o
confidential containers
container group
V This answer is correct.
C) virtual network deployment
This item tests the candidate's knowledge of running containers by using Azure Container Instances (ACI). The top-level resource in ACI is the container group. A container group is a collection of containers that get scheduled on the same host machine. You can specify external volumes to mount within a container group. You can map these volumes into specific paths within the individual containers in a group. A pod is a group of one or more containers with shared storage and network resources and specification for how to run the containers. Pods can be used in the Azure Kubernetes Service but not ACI. Confidential containers on ACI are used to ensure hardware-based confidentiality. ACI enables deployment of container instances into an Azure virtual network. A virtual network deployment cannot be used to map an Azure file share to each container in a multiple container scenario. [Explore Azure Container Instances](https://learn.microsoft.com/training/modules/create-run-container-images-azure-container-instances/2-azure-container-instances-overview)


Question 4 of 50

A container group in Azure Container Instances has multiple containers.
The containers must restart when the process executed in the container group terminates due to an error.
You need to define the restart policy for the container group.
Which Azure CLI command should you use?

Select only one answer.

`az container restart \    --name mycontainer \    --resource-group myResourceGroup \    --no-wait`

`az container create \    --resource-group myResourceGroup \    --name mycontainer \    --image mycontainerimage \    --restart-policy Always`

`az container create \    --resource-group myResourceGroup \    --name mycontainer \    --image mycontainerimage \    --restart-policy Never`

`az container create \    --resource-group myResourceGroup \    --name mycontainer \    --image mycontainerimage \    --restart-policy OnFailure`

**This answer is correct.**

This item tests the candidate’s knowledge of running containers by using Azure Container Instances (ACI). Configurable restart policies can be specified for a container group in ACI. A configurable restart policy allows you to specify that containers are stopped when their processes have completed. When you create a container group in ACI, you can specify one of three restart policy settings: Always, Never, and OnFailure.

If the –restart-policy is mentioned as OnFailure, the containers in the container group are restarted only when the process executed in the container fails (when it terminates with a nonzero exit code). If the –restart-policy is mentioned as Always, the containers in the container group are always restarted irrespective of the success or failure of process execution in a container. If the –restart-policy is mentioned as Never, the containers in the container group will only run at most once.

The az container restart command is used to restart all the containers in a container group, not to define a restart policy for a container group.

[Run containerized tasks with restart policies](https://learn.microsoft.com/training/modules/create-run-container-images-azure-container-instances/4-run-containerized-tasks-restart-policies)


Question 5 of 50

You manage the deployment of an Azure Container Registry named registry1 for a company.
You need to ensure that registry1 **** can be shared across multiple groups in the company, enabling group isolation.
What should you use?
Select only one answer.

artifact

tag

namespace

**This answer is correct.**

layer

This item tests the candidate’s knowledge of publishing an image to Azure Container Registry. A repository is a collection of container images or other artifacts in a registry that have the same name but different tags. A namespace enables the identification of related repositories and artifact ownership by using forward slash-delimited names. A tag for an image specifies its version. An artifact can be, for instance, a text file, a docker image, or a Helm chart stored in the registry with one or more tags. Container images consist of layers. Layers are used to avoid transferring redundant information and to skip build steps that have not changed.

[Manage container images in Azure Container Registry](https://learn.microsoft.com/training/modules/publish-container-image-to-azure-container-registry/)

Question 6 of 50

Your company is developing a new web application that will be deployed as a containerized solution on Azure. The application is expected to have fluctuating workloads and needs to be highly available.
You need to create a solution that allows the application to scale based on demand and recover from failures automatically.
Each correct answer presents part of the solution. Which two actions should you perform? (Choose two.)

Select all answers that apply.

Deploy the containerized application to Azure Container Apps.

**This answer is correct.**

Store the application's images in Azure Blob Storage.

Deploy the containerized application to Azure Container Instance.

Publish the application's image to Azure Container Registry.

**This answer is correct.**

Publishing the application's image to Azure Container Registry allows it to be easily accessed and deployed to Azure services. Azure Container Apps is a serverless container service that automatically scales and recovers from failures, making it suitable for applications with fluctuating workloads and high availability requirements. Running containers using Azure Container Instance does not provide automatic scaling or recovery from failures. Azure Blob Storage is not designed for storing container images.  
[Implement Azure Container Apps - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/implement-azure-container-apps/)  
[Manage container images in Azure Container Registry - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/publish-container-image-to-azure-container-registry/)


Question 7 of 50
You develop a web application hosted on the Web Apps feature of Microsoft Azure App Service.
You need to enable and configure Azure Web Service Local Cache with 1.5 GB.
Which two code segments should you use? Each correct answer presents part of the solution.
Select all answers that apply.

`“WEBSITE_LOCAL_CACHE_OPTION”: “Always”`

**This answer is correct.**

`“WEBSITE_LOCAL_CACHE_SIZEINMB”: “1500”`

**This answer is correct.**

`“WEBSITE_LOCAL_CACHE_OPTION”: “Enable”`

`“WEBSITE_LOCAL_CACHE_SIZEINMB”: “1.5”`

This item tests the candidate’s knowledge of configuring the settings of the Web Apps feature of Azure App Service.

By using `WEBSITE_LOCAL_CACHE_OPTION = Always`, local cache will be enabled. `WEBSITE_LOCAL_CACHE_SIZEINMB` will properly configure Local Cache with 1.5 GB of size. `WEBSITE_LOCAL_CACHE_OPTION = Enable` is not a valid value. `1.5` will not configure 1.5 GB for the local cache.

[Configure web app settings - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-web-app-settings/)


Question 8 of 50
You plan to develop an Azure App Service web app named **app1** by using a Windows custom container.
You need to load a TLS/SSL certificate in application code.
Which app setting should you configure?
Select only one answer.

`WEBSITE_LOAD_CERTIFICATES`

**This answer is correct.**

`WEBSITE_ROOT_CERTS_PATH`

`WEBSITE_CORS_ALLOWED_ORIGINS`

`WEBSITE_AUTH_TOKEN_CONTAINER_SASURL`

This item tests the candidate’s knowledge of configuring app settings, which is part of creating Azure App Service Web Apps.

The `WEBSITE_LOAD_CERTIFICATES` app setting makes the specified certificates accessible to Windows or Linux custom containers as files. The `WEBSITE_ROOT_CERTS_PATH` app setting is read-only and does not allow comma-separated thumbprint values to be mentioned to the certificates and then be loaded in the code. The `WEBSITE_AUTH_TOKEN_CONTAINER_SASURL` app setting is used to instruct the auth module to store and load all encrypted tokens to the specified blob storage container. This setting is used for Azure Storage and cannot be used to load certificates inside a Windows custom container.

[Configure web app settings - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-web-app-settings/)

Question 9 of 50
You manage the staging and production deployment slots of an Azure App Service web app named **app1**.
You need to ensure a connection string is not swapped when swapping is performed.
Which configuration should you use?
Select only one answer.

Deployment Center

Deployment slot setting

**This answer is correct.**

Managed identity

Scale up

This item tests the candidate’s knowledge of deploying code to Azure App Service, which is part of creating Azure App Service Web Apps.

Marking a setting as a deployment slot setting keeps it sticky to that deployment slot. For example, an app setting marked as a deployment slot setting on app1 will always stick with app1 and will never move to app1/staging during a swap. The Deployment Center setting is used to configure continuous deployment and manual deployment. Managed identity provides an identity for applications to use when connecting to resources that support Microsoft Entra ID  authentication. Scale up will ensure the web app is entitled to get CPU, memory, disk space, and extra features such as dedicated virtual machines, custom domains and certificates, staging slots, and autoscaling. Deployment Center, Managed Identity, and Scale up cannot be used to ensure a connecting string is not swapped when swapping is performed.

[Host a web application with Azure App Service - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/host-a-web-app-with-azure-app-service/)

Question 10 of 50
You need to configure a web app to allow external requests from https://myapps.com.
Which Azure CLI command should you use?
Select only one answer.

`az webapp cors add -g MyResourceGroup -n MyWebApp --allowed-origins https://myapps.com`

**This answer is correct.**

`az webapp identity add -g MyResourceGroup -n MyWebApp --allowed-origins https://myapps.com`

`az webapp traffic-routing set --distribution myapps=100 --name MyWebApp --resource-group MyResourceGroup`

`az webapp config access-restriction add -g MyResourceGroup -n MyWebApp --rule-name external --action Allow –ids myapps --priority 200`

This item tests the candidate’s knowledge of configuring web app settings.

The code segment that includes the `cors add` will configure CORS to allow requests from  HYPERLINK "https://myapps.com" https://myapps.com. The code segment that includes `identity add` will add a managed identity to a web app. The code segment that includes `traffic-routing-set` will configure a traffic routing to a deployment slot named **myapps**. The code segment that includes `access-restriction add` will add an access restriction on a web app.

[Tutorial: Host a RESTful API with CORS in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-rest-api)

Question 11 of 50
A company plans to implement a Microsoft Defender for Cloud solution.
The company has the following requirements:
- Notifies when DNS domains are not deleted when a new Azure Functions app is deleted.
- Use native alerting.
- Minimize costs.
You need to select a hosting plan.
Which hosting plan should you use?
Select only one answer.

Consumption

Standard

**This answer is correct.**

Premium

Free

This item tests the candidate's knowledge about securing Azure Functions.

The Standard plan supports both custom domains and Microsoft Defender for Cloud, which can automatically alert on dangling DNS domains. The Consumption plan is incorrect because it does not support Microsoft Defender for Cloud. This can automatically alert on dangling DNS domains. The Premium plan supports custom domains and Microsoft Defender for Cloud, which can automatically alert on dangling DNS domains. This, however, is not the lowest cost option. The Free plan does not support custom domains, although it does support Microsoft Defender for Cloud, which can automatically alert on dangling DNS domains.

[Overview of Defender for App Service to protect your Azure App Service web apps and APIs - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-app-service-introduction "Overview of Defender for App Service to protect your Azure App Service web apps and APIs - Training | Microsoft Learn")

A company plans to create an Azure Functions app.
You need to recommend a solution that meets the following requirements:
- Executes multiple functions concurrently.
- Performs aggregation on the results from the functions.
- Avoids cold starts.
- Minimizes costs.
Which two components should you recommend? Each correct answer presents part of the solution
Select all answers that apply.

The Consumption plan

The Premium plan

**This answer is correct.**

Fan-out/fan-in pattern

**This answer is correct.**

Function chaining pattern

This item tests the candidate’s knowledge of Azure Durable Functions and hosting plans.

The Premium plan avoids cold starts and offers unlimited execution duration. The fan-out/fan-in pattern enables multiple functions to be executed in parallel, waiting for all functions to finish. Often, some aggregation work is done on the results that are returned from the functions. The Consumption plan avoids paying for idle time but might face cold starts. Furthermore, each function run is limited to 10 minutes. The function chaining pattern is a sequence of functions that execute in a specific order. In this pattern, the output of one function is applied to the input of another function.

[AZ-204: Implement Azure Functions - Training | Microsoft Learn](https://learn.microsoft.com/training/paths/implement-azure-functions/)

Question 13 of 50
You create a batch routine by using a timer trigger in Azure Functions.
You need to configure the batch routine to execute every 15 minutes, from Monday through Friday.
Which code segment should you use?
Select only one answer.

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("0 */15 * * * 1-5")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

**This answer is correct.**

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("*/15 * * * 0-4")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("0 15 * * * ")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("* 15 * * 1-5")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

This item tests the candidate’s knowledge of working with timer triggers in Azure Functions.

The code segment that includes `Run([TimerTrigger("0 */15 * * * 1-5")` executes the function every 15 minutes from Monday to Friday. The code segment that includes `Run([TimerTrigger("*/15 * * * 0-4")` is missing the second part, and it is not using the proper range for days of the week. The code segment that includes `Run([TimerTrigger("0 15 * * * ")` executes only once at 15:00 (3 PM). The code segment that includes `Run([TimerTrigger("* 15 * * 1-5")` is missing the seconds attribute and the step (‘/’) part for the minutes.

https://learn.microsoft.com/training/modules/execute-azure-function-with-triggers/

[Timer trigger for Azure Functions - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cisolated-process%2Cnodejs-v4&pivots=programming-language-csharp)

Question 14 of 50
You are developing an Azure Functions app that will be deployed to a Consumption plan. The app consumes data from a database server that has limited throughput.
You need to use the `functionAppScaleLimit` property to control the number of instances of the app that will be created.
Which value should you use for the property setting?
Select only one answer.

0

10

**This answer is correct.**

null

This item tests the candidate’s knowledge of configuring an Azure Functions app. Imposing limits on the scaling out capacity of an Azure Functions app can help when the app connects to components that have limited throughput. The `functionAppScaleLimit` property lets you define the number of instances of the Azure Functions app that will be created. Therefore, setting it to a low value, such as 10, is appropriate in this scenario. Azure Functions apps in the Consumption plan can scale out and have 200 instances as a default. A value of 0 or null for the `functionAppScaleLimit` property means that an unrestricted number of instances of the Azure Functions app will be created.

[Scale Azure Functions - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-azure-functions/4-scale-azure-functions)

Question 15 of 50
You are developing an Azure Functions app that will be deployed to a Dedicated plan.
When there is a resource shortage in the app, it must send a “429 Too Busy” response.
You need to apply the appropriate configuration to all functions in a Azure Functions app instance.
Which configuration should you set?
Select only one answer.

`dynamicThrottlesEnabled` in the host.json file

**This answer is correct.**

bindings section in the function.json file

`maxOutstandingRequests` in the host.json file

`maxConcurrentRequests` in the function.json file

This item tests the candidate’s knowledge of controlling scaling of functions. Using the `dynamicThrottlesEnabled` property allows developers to let the system respond dynamically to an increased utilization, returning “429 Too Busy” errors. This property is defined in the host.json file. The bindings section, part of the function.json file, is used to define the bindings and triggers for a function. The `maxConcurrentRequests` property is used to determine the maximum number of function instances to run in parallel. It is defined in the function.json file. The `maxOutstandingRequests` property, defined in the host.json file, defines the maximum number of requests, queued or in progress, held at any given time.

[Create triggers and bindings - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/develop-azure-functions/3-create-triggers-bindings)

Question 16 of 50
You are a developing a serverless API using Azure Functions. The API is expected to handle a large number of HTTP requests and make outbound requests to a third-party service. The third-party service has a rate limit on the number of requests it can handle per minute.
You need to ensure that the Azure Function does not exceed the rate limit of the third-party service and manage resource utilization effectively.
Each correct answer presents part of the solution. Which two actions should you perform?
Select all answers that apply.

Enable 'dynamicThrottlesEnabled' property in the host.json file to reject requests with a 429 'Too Busy' response when system performance counters are over a high threshold.

Enable 'hsts' property in the host.json file to enforce HTTP Strict Transport Security (HSTS) behavior.

Set the 'maxConcurrentRequests' property in the host.json file to limit the number of parallel executions.
**This answer is correct.**

Set the 'maxOutstandingRequests' property in the host.json file to limit the number of outstanding requests at any given time.
**This answer is correct.**

Set the 'routePrefix' property in the host.json file to an empty string to remove the default prefix.

Setting the 'maxConcurrentRequests' property in the host.json file will limit the number of HTTP functions that are executed in parallel, which can help manage resource utilization and avoid exceeding the rate limit of the third-party service. The 'maxOutstandingRequests' property limits the number of outstanding requests that are held at any given time, including queued requests and in-progress executions, which can also help manage resource utilization. Enabling 'dynamicThrottlesEnabled' property would not help in this scenario as it rejects requests based on system performance counters, not based on the rate limit of a third-party service. The 'hsts' property is used to enforce HTTP Strict Transport Security (HSTS) behavior and is not related to managing resource utilization or rate limiting. The 'routePrefix' property is used to set the route prefix for all routes and does not affect resource utilization or rate limiting.

[Azure Functions HTTP triggers and bindings overview - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook?tabs=isolated-process%2Cfunctionsv2&pivots=programming-language-csharp)

Question 1 of 50
You manage a multiregion deployment of an Azure Cosmos DB account named **account1**.
You need to configure the default consistency level for account1. The consistency level must maximize throughput and minimize latency for write operations.
Which cnsistency level should you use?

Select only one answer.

bounded staleness

consistent prefix

eventual

**This answer is correct.**

session

This item tests the candidate’s knowledge of selecting the consistency level, which is part of developing Azure Cosmos DB solutions.

The eventual consistency level maximizes throughput and minimizes latency. The bounded staleness consistency level provides lower throughput and higher latency comparing with the remaining answer choices. The consistent prefix consistency level provides higher throughput and lower latency for write operations than the session consistency level but lower throughput and higher latency than the eventual consistency levels. The session consistency level provides higher throughput and lower latency for write operations than the bounded staleness consistency level but lower throughput and higher latency than the eventual and consistent prefix consistency levels.

[Choose the right consistency level - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-azure-cosmos-db/5-choose-cosmos-db-consistency-level)

Question 2 of 50
You manage an Azure Cosmos DB container named **container1**.
You need to use the `ReadItemAsync` method to read an item from the Azure Cosmos service.
Which two parameters should you provide? Each correct answer presents part of the solution.
Select all answers that apply.

`consistencyLevel`

`eTag`

`partitionKey`

**This answer is correct.**

`sessionToken`

`id`

**This answer is correct.**

This item tests the candidate’s knowledge of setting the partition key, which is part of developing Azure Cosmos DB solutions.
The `ReadItemAsync` method of the container class of .NET SDK for Azure Cosmos DB has two mandatory parameters: `partitionKey` and `itemId`. The `consistencyLevel` parameter is part of the optional `requestOptions` parameter of the `ReadItemAsync`.
The `eTag` and `sessionToken` parameters are part of the optional `requestOptions` parameter of the `ReadItemAsync` method.

[Explore Microsoft .NET SDK v3 for Azure Cosmos DB - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/work-with-cosmos-db/2-cosmos-db-dotnet-overview)

Question 3 of 50
You have an application that writes data to Azure Cosmos DB.
The application must offer monotonic reads, with no guarantee that the value read is the last value written.
You need to configure the consistency level.
Which consistency level should you use?
Select only one answer.

strong

bounded staleness

session

**This answer is correct.**

eventual

This item tests the candidate's knowledge of Azure Cosmos DB consistency levels.
Session consistency offers all the guarantees listed. It provides write latencies, availability, and read throughput comparable to that of eventual consistency. It also provides the consistency guarantees that suit the needs of applications written to operate in the context of a user. Strong consistency has reads guaranteed to return the most recent committed version of an item. A client never sees an uncommitted or partial write. Users are guaranteed to read the latest committed write. It has the highest write latency and lowest read throughput of all consistency levels. In bounded staleness consistency, the reads are guaranteed to honor the consistent-prefix guarantee. It should be used when there is a need for low write latencies but require a total global order guarantee. In eventual consistency, there is no ordering guarantee for reads. In the absence of any further writes, the replicas eventually converge. It is the weakest form of consistency because a client may read values that are older than the ones it had read before. Eventual consistency is ideal when the application does not require any ordering guarantees.

[AZ-204: Develop solutions that use Azure Cosmos DB - Training | Microsoft Learn](https://learn.microsoft.com/training/paths/az-204-develop-solutions-that-use-azure-cosmos-db/)

Question 4 of 50
A company implements a multi-region Azure Cosmos DB account.
You need to configure the default consistency level for the account. The consistency level must ensure that update operations made as a batch within a transaction are always visible together.
Which consistency level should you use?
Select only one answer.

Bounded Staleness

Session

Consistent Prefix

**This answer is correct.**

Eventual

This item tests the candidate’s knowledge of selecting the appropriate consistency level for operations in Azure Cosmos DB. The Consistent Prefix consistency level ensures that updates made as a batch within a transaction are returned consistently with the transaction in which they were committed. Write operations within a transaction of multiple documents are always visible together. The Bounded Staleness consistency level is used to manage the lag of data between any two regions based on an updated version of an item or the time intervals between read and write. The Session consistency level is used to ensure that within a single client session, reads are guaranteed to honor the read-your-writes and write-follows-reads guarantees. The Eventual consistency level is used when no ordering guarantee is required.
[Explore consistency levels](https://learn.microsoft.com/training/modules/explore-azure-cosmos-db/4-cosmos-db-consistency-levels-overview)

Question 1 of 50
A company uses Azure Container Instances for an application.
You need to ensure that the containers are restarted when the process terminates with a nonzero exit code.
What should you do?
Select only one answer.

Define a container restart policy of `Always`.

**This answer is correct.**

Run the containers using a managed identity.

Define a container restart policy of `Never`.

Run an init container.

This item tests the candidate's knowledge of restart policies in Azure Container Instances.

Containers in the container group are always restarted with an `Always` policy in effect, regardless of their exit code. Running containers using a managed identity would simplify the access to external Azure resources but doing so has no effect on when a container restarts. When the processes in the container fail (terminating with a nonzero exit code), they will not restart and will only run once at most. Init containers are meant to perform initialization logic for app containers, running to completion before the application containers start.

[Run container images in Azure Container Instances - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/create-run-container-images-azure-container-instances/)

Question 2 of 50

You need to deploy an Azure Files share along with a container group to Azure Container Instances (ACI).
Which deployment method should you use?
Select only one answer.
YAML file

Azure Resource Manager template

**This answer is correct.**

Docker Compose

Azure CLI

This item tests the candidate’s knowledge of running containers by using Azure Container Instances (ACI). There are two common ways to deploy a multi-container group: use an Azure Resource Manager template or a YAML file. An Azure Resource Manager template is recommended when you need to deploy additional Azure service resources (for example, an Azure Files share) when you deploy the container instances. However, a YAML file does not support the deployment of additional Azure service resources along with container groups in ACI. Docker Compose and Azure CLI do not support the deployment of an Azure Files share along with a container group to ACI.

[Explore Azure Container Instances](https://learn.microsoft.com/training/modules/create-run-container-images-azure-container-instances/2-azure-container-instances-overview)

Question 3 of 50
You manage the deployment of an Azure Container Registry named registry1 for a company.
You need to ensure that registry1 **** can be shared across multiple groups in the company, enabling group isolation.
What should you use?
Select only one answer.
artifact

tag

namespace

**This answer is correct.**

layer

This item tests the candidate’s knowledge of publishing an image to Azure Container Registry. A repository is a collection of container images or other artifacts in a registry that have the same name but different tags. A namespace enables the identification of related repositories and artifact ownership by using forward slash-delimited names. A tag for an image specifies its version. An artifact can be, for instance, a text file, a docker image, or a Helm chart stored in the registry with one or more tags. Container images consist of layers. Layers are used to avoid transferring redundant information and to skip build steps that have not changed.

[Manage container images in Azure Container Registry](https://learn.microsoft.com/training/modules/publish-container-image-to-azure-container-registry/)

Question 4 of 50
Your company is developing an application that includes a backend web API service. The development team has decided to use Azure Container Apps to host the API. They have a Dockerfile in the root of their repository that defines the containerized app.
You need to deploy the container app using the Dockerfile.
What should you do?
Select only one answer.
Use the `az containerapp env create` command with the `--name` parameter.

Use the `az containerapp create` command with the `--image` parameter.

**This answer is incorrect.**

Use the `az containerapp create` command with the `--containername` parameter.

Use the `az containerapp up` command with the `--source .` parameter.

**This answer is correct.**

The `az containerapp up` command with the `--source .` parameter builds and deploys the container app using the Dockerfile in the root of the repository. The other options either do not exist or do not fulfill the requirement.

[Quickstart: Build and deploy from local source code to Azure Container Apps - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-apps/quickstart-code-to-cloud?tabs=bash%2Ccsharp)

Question 5 of 50
You deploy a Linux-based web app container to an Azure container instance.
You need to meet the following requirements:
- Expose the app publicly over HTTP.
- Verify that the container runs and generates logs.
- Ensure that the container restarts automatically if the process fails.
Which two actions should you perform? Each correct answer presents part of the solution.
Select only one answer.
Configure the container group to use a public IP address.

**This answer is correct.**

Enable a system-assigned managed identity for the container group.

Enable diagnostic settings for the container group.

Publish the container image to Azure Container Registry.

Set the container restart policy to Always.

**This answer is incorrect.**

**Objective:**

1.1 Implement containerized solutions

**What This Item Tests:**

Run containers by using Azure Container Instances

**Additional Reading:**

[Run containerized tasks with restart policies - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-restart-policy)

**Rationale:**

Assigning a public IP address is required to make a web app that runs in Azure Container Instances accessible over HTTP, and configuring the container restart policy to Always ensures that the container restarts automatically if the app process stops. Both of these are fundamental aspects of running containers in Azure Container Instances. The other options are incorrect because diagnostic settings only control log export and monitoring, managed identities are used for authenticating to Azure services rather than controlling container availability or networking, and publishing an image to Azure Container Registry is not required since Azure Container Instances can run container images without relying on a private registry.

Question 6 of 50
You plan to develop an Azure App Service web app named **app1** by using a Windows custom container.
You need to load a TLS/SSL certificate in application code.
Which app setting should you configure?
Select only one answer.
`WEBSITE_LOAD_CERTIFICATES`

**This answer is correct.**

`WEBSITE_ROOT_CERTS_PATH`

`WEBSITE_CORS_ALLOWED_ORIGINS`

`WEBSITE_AUTH_TOKEN_CONTAINER_SASURL`

This item tests the candidate’s knowledge of configuring app settings, which is part of creating Azure App Service Web Apps.

The `WEBSITE_LOAD_CERTIFICATES` app setting makes the specified certificates accessible to Windows or Linux custom containers as files. The `WEBSITE_ROOT_CERTS_PATH` app setting is read-only and does not allow comma-separated thumbprint values to be mentioned to the certificates and then be loaded in the code. The `WEBSITE_AUTH_TOKEN_CONTAINER_SASURL` app setting is used to instruct the auth module to store and load all encrypted tokens to the specified blob storage container. This setting is used for Azure Storage and cannot be used to load certificates inside a Windows custom container.

[Configure web app settings - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-web-app-settings/)

Question 7 of 50
You need to configure a web app to allow external requests from https://myapps.com.
Which Azure CLI command should you use?
Select only one answer.

`az webapp cors add -g MyResourceGroup -n MyWebApp --allowed-origins https://myapps.com`

**This answer is correct.**

`az webapp identity add -g MyResourceGroup -n MyWebApp --allowed-origins https://myapps.com`

`az webapp traffic-routing set --distribution myapps=100 --name MyWebApp --resource-group MyResourceGroup`

`az webapp config access-restriction add -g MyResourceGroup -n MyWebApp --rule-name external --action Allow –ids myapps --priority 200`

This item tests the candidate’s knowledge of configuring web app settings.

The code segment that includes the `cors add` will configure CORS to allow requests from  HYPERLINK "https://myapps.com" https://myapps.com. The code segment that includes `identity add` will add a managed identity to a web app. The code segment that includes `traffic-routing-set` will configure a traffic routing to a deployment slot named **myapps**. The code segment that includes `access-restriction add` will add an access restriction on a web app.

[Tutorial: Host a RESTful API with CORS in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-rest-api)

Question 8 of 50
You manage a multi-instance deployment of an Azure App Service web app named **app1**.
You need to ensure a client application is routed to the same instance for the life of the session.
Which platform setting should you use?
Select only one answer.

WebSocket

**This answer is incorrect.**

Always on

HTTP version

ARR Affinity

**This answer is correct.**

This item tests the candidate’s knowledge of configuring web app settings, which is part of creating Azure App Service Web Apps.

In a multi-instance deployment, the ARR Affinity setting ensures a client application is routed to the same instance for the life of the session. WebSocket is a standardized protocol that provides full-duplex communication. Always on keeps the app loaded even when there is no traffic. In HTTP/2, a persistent connection can be used to service multiple simultaneous requests. WebSocket, Always on, and HTTP version are not used to ensure a client application is routed to the same instance for the life of the session.

[Configure web app settings - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-web-app-settings/)


Question 9 of 50
You are developing a Linux web app on Azure App Service.
You need to deploy the web app to the production environment based on the following requirements:
- App changes must be validated in an environment identical to the production environment before moving the app to the production environment.
- Downtime must be eliminated when the app is deployed to the production environment.
What should you use?
Select only one answer.
Deployment slots

**This answer is correct.**

Auto-scaling

Hybrid connection

App cloning

This item tests the candidate’s knowledge of when to use deployment slots. Deployment slots are live apps with unique host names, which allow swapping configuration and content between them. Auto-scaling is a feature that allows adding more capacity to an Azure Functions app hosting environment. This capacity can be added to an individual hosting environment (for example, scaling up or adding memory or CPU), or adding more hosts (scaling out). The scaling can be triggered based on a schedule or when breaching thresholds defined for certain metrics. Hybrid connections are available for consuming on-premises apps without needing to expose them to the internet. App cloning is a process to obtain an existing app and copy it to another destination, which can be a new app or a deployment slot, for example. However, this is not supported on Linux apps.

[Explore staging environments - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/understand-app-service-deployment-slots/2-app-service-staging-environments)

[Discover App Service networking features - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/introduction-to-azure-app-service/6-network-features)

[Examine Azure App Service plans - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/introduction-to-azure-app-service/3-azure-app-service-plans)

Question 10 of 50
You develop an App Service app hosted on Windows Platform. Users report that the app is failing.
You need to begin troubleshooting the app by inspecting a copy of the page that is returned when the HTTP return code is greater than 400.
Which type of log should you review?
Select only one answer.

application

web server

detailed error

**This answer is correct.**

deployment

This item tests the candidate’s knowledge of using logs to troubleshoot web apps. The detailed error log contains copies of the error pages, produced in response to HTTP codes greater than 400, that would have been sent to clients. These pages are not sent due to security reasons. The web server log shows information about the raw HTTP request, such as method, bytes, and client user agent. The application log is application specific, logging information that your application code or components that are used by your application writes. The deployment log stores information to diagnose the reasons for a failed deployment.

[Enable diagnostic logging - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-web-app-settings/5-enable-diagnostic-logging)


Question 11 of 50
You plan to create an Azure Functions app named **app1**.
You need to ensure that app1 will satisfy the following requirements:
- Supports automatic scaling.
- Has event-based scaling behavior.
- Provides a serverless pricing model.
Which hosting plan should you use?
Select only one answer.
App Service

App Service Environment

Consumption

**This answer is correct.**

Functions Premium

This item tests the candidate’s knowledge of selecting the appropriate hosting plan, which is part of the implementation of Azure Functions.

The Consumption hosting plan satisfies all requirements. It supports autoscaling, has event-based scaling behavior, and provides a serverless pricing model. The App Service, App Service Environment, and Functions Premium hosting plans support autoscaling but does not provide the serverless pricing model. Its scaling behavior is not event based but performance based.

[Compare Azure Functions hosting options - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-azure-functions/3-compare-azure-functions-hosting-options)

Question 12 of 50
A company plans to implement a Microsoft Defender for Cloud solution.
The company has the following requirements:
- Notifies when DNS domains are not deleted when a new Azure Functions app is deleted.
- Use native alerting.
- Minimize costs.
You need to select a hosting plan.

Which hosting plan should you use?

Select only one answer.

Consumption

Standard

**This answer is correct.**

Premium

Free

This item tests the candidate's knowledge about securing Azure Functions.

The Standard plan supports both custom domains and Microsoft Defender for Cloud, which can automatically alert on dangling DNS domains. The Consumption plan is incorrect because it does not support Microsoft Defender for Cloud. This can automatically alert on dangling DNS domains. The Premium plan supports custom domains and Microsoft Defender for Cloud, which can automatically alert on dangling DNS domains. This, however, is not the lowest cost option. The Free plan does not support custom domains, although it does support Microsoft Defender for Cloud, which can automatically alert on dangling DNS domains.

[Overview of Defender for App Service to protect your Azure App Service web apps and APIs - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-app-service-introduction "Overview of Defender for App Service to protect your Azure App Service web apps and APIs - Training | Microsoft Learn")

Question 13 of 50
A company plans to create an Azure Functions app.
You need to recommend a solution that meets the following requirements:
- Executes multiple functions concurrently.
- Performs aggregation on the results from the functions.
- Avoids cold starts.
- Minimizes costs.
Which two components should you recommend? Each correct answer presents part of the solution
Select all answers that apply.
The Consumption plan

The Premium plan

**This answer is correct.**

Fan-out/fan-in pattern

**This answer is correct.**

Function chaining pattern

This item tests the candidate’s knowledge of Azure Durable Functions and hosting plans.

The Premium plan avoids cold starts and offers unlimited execution duration. The fan-out/fan-in pattern enables multiple functions to be executed in parallel, waiting for all functions to finish. Often, some aggregation work is done on the results that are returned from the functions. The Consumption plan avoids paying for idle time but might face cold starts. Furthermore, each function run is limited to 10 minutes. The function chaining pattern is a sequence of functions that execute in a specific order. In this pattern, the output of one function is applied to the input of another function.

[AZ-204: Implement Azure Functions - Training | Microsoft Learn](https://learn.microsoft.com/training/paths/implement-azure-functions/)

Question 14 of 50
You create a batch routine by using a timer trigger in Azure Functions.
You need to configure the batch routine to execute every 15 minutes, from Monday through Friday.
Which code segment should you use?
Select only one answer.
[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("0 */15 * * * 1-5")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

**This answer is correct.**

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("*/15 * * * 0-4")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("0 15 * * * ")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

[Function(nameof(TimerTriggerCSharp))]  
[FixedDelayRetry(5, "00:00:10")]  
public static void Run([TimerTrigger("* 15 * * 1-5")] TimerInfo myTimer,  
  FunctionContext context)  
{  
  var log = context.GetLogger(nameof(TimerFunction));  
  if (myTimer.IsPastDue)  
  {  
    log.LogInformation("Timer is running late!");  
  }  
  log.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");  
}

This item tests the candidate’s knowledge of working with timer triggers in Azure Functions.

The code segment that includes `Run([TimerTrigger("0 */15 * * * 1-5")` executes the function every 15 minutes from Monday to Friday. The code segment that includes `Run([TimerTrigger("*/15 * * * 0-4")` is missing the second part, and it is not using the proper range for days of the week. The code segment that includes `Run([TimerTrigger("0 15 * * * ")` executes only once at 15:00 (3 PM). The code segment that includes `Run([TimerTrigger("* 15 * * 1-5")` is missing the seconds attribute and the step (‘/’) part for the minutes.

https://learn.microsoft.com/training/modules/execute-azure-function-with-triggers/

[Timer trigger for Azure Functions - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cisolated-process%2Cnodejs-v4&pivots=programming-language-csharp)

Question 15 of 50
You are developing an Azure Functions app that will be deployed to a Consumption plan. The app consumes data from a database server that has limited throughput.
You need to use the `functionAppScaleLimit` property to control the number of instances of the app that will be created.
Which value should you use for the property setting?
Select only one answer.
0

10

**This answer is correct.**

null

This item tests the candidate’s knowledge of configuring an Azure Functions app. Imposing limits on the scaling out capacity of an Azure Functions app can help when the app connects to components that have limited throughput. The `functionAppScaleLimit` property lets you define the number of instances of the Azure Functions app that will be created. Therefore, setting it to a low value, such as 10, is appropriate in this scenario. Azure Functions apps in the Consumption plan can scale out and have 200 instances as a default. A value of 0 or null for the `functionAppScaleLimit` property means that an unrestricted number of instances of the Azure Functions app will be created.

[Scale Azure Functions - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-azure-functions/4-scale-azure-functions)

Question 16 of 50
You are developing an Azure Functions app that will be deployed to a Dedicated plan.
When there is a resource shortage in the app, it must send a “429 Too Busy” response.
You need to apply the appropriate configuration to all functions in a Azure Functions app instance.
Which configuration should you set?
Select only one answer.

`dynamicThrottlesEnabled` in the host.json file

**This answer is correct.**

bindings section in the function.json file

`maxOutstandingRequests` in the host.json file

`maxConcurrentRequests` in the function.json file

This item tests the candidate’s knowledge of controlling scaling of functions. Using the `dynamicThrottlesEnabled` property allows developers to let the system respond dynamically to an increased utilization, returning “429 Too Busy” errors. This property is defined in the host.json file. The bindings section, part of the function.json file, is used to define the bindings and triggers for a function. The `maxConcurrentRequests` property is used to determine the maximum number of function instances to run in parallel. It is defined in the function.json file. The `maxOutstandingRequests` property, defined in the host.json file, defines the maximum number of requests, queued or in progress, held at any given time.

[Create triggers and bindings - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/develop-azure-functions/3-create-triggers-bindings)

Question 17 of 50
You are a developing a serverless API using Azure Functions. The API is expected to handle a large number of HTTP requests and make outbound requests to a third-party service. The third-party service has a rate limit on the number of requests it can handle per minute.
You need to ensure that the Azure Function does not exceed the rate limit of the third-party service and manage resource utilization effectively.
Each correct answer presents part of the solution. Which two actions should you perform?
Select all answers that apply.

Enable 'dynamicThrottlesEnabled' property in the host.json file to reject requests with a 429 'Too Busy' response when system performance counters are over a high threshold.

Enable 'hsts' property in the host.json file to enforce HTTP Strict Transport Security (HSTS) behavior.

Set the 'maxConcurrentRequests' property in the host.json file to limit the number of parallel executions.

**This answer is correct.**

Set the 'maxOutstandingRequests' property in the host.json file to limit the number of outstanding requests at any given time.

**This answer is correct.**

Set the 'routePrefix' property in the host.json file to an empty string to remove the default prefix.

Setting the 'maxConcurrentRequests' property in the host.json file will limit the number of HTTP functions that are executed in parallel, which can help manage resource utilization and avoid exceeding the rate limit of the third-party service. The 'maxOutstandingRequests' property limits the number of outstanding requests that are held at any given time, including queued requests and in-progress executions, which can also help manage resource utilization. Enabling 'dynamicThrottlesEnabled' property would not help in this scenario as it rejects requests based on system performance counters, not based on the rate limit of a third-party service. The 'hsts' property is used to enforce HTTP Strict Transport Security (HSTS) behavior and is not related to managing resource utilization or rate limiting. The 'routePrefix' property is used to set the route prefix for all routes and does not affect resource utilization or rate limiting.

[Azure Functions HTTP triggers and bindings overview - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook?tabs=isolated-process%2Cfunctionsv2&pivots=programming-language-csharp)

Question 18 of 50
A company uses Azure API Management to expose some of its services.
Each developer consuming APIs must use a single key to obtain access to various APIs without requiring approval from the API publisher.
You need to recommend a solution.
Which solution should you recommend?
Select only one answer.
Define a subscription with all APIs scope.

Define a subscription with product scope.

**This answer is correct.**

Restrict access based on caller IPs.

Restrict APIs based on client certificate.

This item tests the candidate's knowledge of Azure API Management subscriptions.

When creating a product, several APIs can be added to the product and a subscription can be associated with it. Access should not be granted to all APIs. Developer access should be granted regardless of the caller IP. A client certificate would require a policy to validate the certificate and specific logic to map the client to specific APIs.

[Secure APIs by using subscriptions - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-api-management/6-secure-access-api-subscriptions)

Question 19 of 50
You manage APIs in production by using Azure API Management.
You need to remove X-Powered-By and X-AspNet-Version headers from a response.
Which code segment should you use?
Select only one answer.
```
<policies>&#60;policies&#62;<br><br>&#160;&#160; &#60;inbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/inbound&#62;<br><br>&#160;&#160; &#60;backend&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/backend&#62;<br><br>&#160;&#160; &#60;outbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-Powered-By" exists-action="append" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-AspNet-Version" exists-action="append" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/outbound&#62;<br><br>&#160;&#160; &#60;on-error&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/on-error&#62;<br><br>&#60;/policies&#62;</policies> <inbound></inbound>

   <backend></backend>

   <outbound></outbound>
     <set-header name="X-Powered-By" exists-action="append"></set-header>
     <set-header name="X-&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;AspNet&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;-Version" exists-action="append"></set-header>

   <on-error></on-error>

```

```
<policies>&#60;policies&#62;<br><br>&#160;&#160; &#60;inbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/inbound&#62;<br><br>&#160;&#160; &#60;backend&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-Powered-By" exists-action="delete" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-AspNet-Version" exists-action="delete" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/backend&#62;<br><br>&#160;&#160; &#60;outbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/outbound&#62;<br><br>&#160;&#160; &#60;on-error&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/on-error&#62;<br><br>&#60;/policies&#62;</policies>   <inbound></inbound>

   <backend></backend>
     <set-header name="X-Powered-By" exists-action="delete"></set-header>
     <set-header name="X-&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;AspNet&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;-Version" exists-action="delete"></set-header>

   <outbound></outbound>

   <on-error></on-error>

```

```
<policies>&#60;policies&#62;<br><br>&#160;&#160; &#60;inbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/inbound&#62;<br><br>&#160;&#160; &#60;backend&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/backend&#62;<br><br>&#160;&#160; &#60;outbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-Powered-By" exists-action="delete" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-AspNet-Version" exists-action="delete" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/outbound&#62;<br><br>&#160;&#160; &#60;on-error&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/on-error&#62;<br><br>&#60;/policies&#62;</policies>   <inbound></inbound>

   <backend></backend>

   <outbound></outbound>
     <set-header name="X-Powered-By" exists-action="delete"></set-header>
     <set-header name="X-&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;AspNet&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;-Version" exists-action="delete"></set-header>

   <on-error></on-error>

```

**This answer is correct.**

```
<policies>&#60;policies&#62;<br><br>&#160;&#160; &#60;inbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/inbound&#62;<br><br>&#160;&#160; &#60;backend&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-Powered-By" exists-action="append" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;set-header name="X-AspNet-Version" exists-action="append" /&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/backend&#62;<br><br>&#160;&#160; &#60;outbound&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/outbound&#62;<br><br>&#160;&#160; &#60;on-error&#62;<br><br>&#160;&#160;&#160;&#160; &#60;base /&#62;<br><br>&#160;&#160; &#60;/on-error&#62;<br><br>&#60;/policies&#62;</policies>   <inbound></inbound>

   <backend></backend>
     <set-header name="X-Powered-By" exists-action="append"></set-header>
     <set-header name="X-&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;AspNet&#60;/span&#62;&#60;span class='consolas-monospace-font'&#62;-Version" exists-action="append"></set-header>

   <outbound></outbound>

   <on-error></on-error>

```

This item tests the candidate’s knowledge of defining policies for APIs using Azure API Management.

The code segment that includes the `set-header policy` element in the outbound section and `exists-action="delete"` will remove a header from the HTTP response. The code segment that includes the `exists-action` with append value will not remove the specified headers. The code segments that do not include the `set-header policy` element in the outbound section will not remove a header from the HTTP response.

[Introduction to Azure API Management - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/introduction-to-azure-api-management/)

Question 20 of 50
You manage an Azure API Management instance.
You need to limit the maximum number of API calls allowed from a single source for a specific time interval.
What should you configure?
Select only one answer.
Product

Policy

**This answer is correct.**

Subscription

API

This item tests the candidate’s knowledge of polices in Azure API Management, which is part of implementing API Management.

API publishers can change API behavior through configuration using policies. Policies are a collection of statements that run sequentially on the request or response of an API. A product has one or more APIs, a usage quota, and the terms of use and cannot be used to restrict the number of API calls. Subscriptions are the most common way for API consumers to access APIs published through an API Management instance. API is a representation of a back-end API and needs to be configured with a policy to implement a rate limit.

[How Azure API Management Works - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/introduction-to-azure-api-management/3-how-azure-api-management-works)

Question 21 of 50
A company is using Azure API Management to expose their APIs to external partners. The company wants to ensure that the APIs are accessible only to users authenticated with OAuth 2.0, and that usage quotas are enforced to prevent abuse.
You need to configure the API Management instance to meet the security and usage requirements.
Which two actions should you perform?
Select all answers that apply.
Configure a validate-jwt policy to authenticate incoming requests.

**This answer is correct.**

Deploy an Azure Application Gateway in front of the API Management instance.

Implement IP filtering by defining access restriction policies.

Set up a rate limit by key policy to enforce call quotas.

**This answer is correct.**

Configuring a validate-jwt policy is necessary to authenticate users with OAuth 2.0. Setting up a rate limit by key policy helps enforce usage quotas. IP filtering does not address the authentication and quota requirements. Deploying an Azure Application Gateway is not required for these specific needs.

[Quickstart: Create a new Azure API Management instance by using the Azure CLI](https://learn.microsoft.com/en-us/azure/api-management/get-started-create-service-instance-cli)  
[Authentication and authorization to APIs in Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/authentication-authorization-overview)

Question 22 of 50
You have an Azure event hub.
You need to add partitions to the event hub.
Which code segment should you use?
Select only one answer.
`az eventhubs eventhub consumer-group update --resource-group MyResourceGroupName --namespace-name MyNamespaceName --eventhub-name MyEventHubName --set partitioncount=12`

`az eventhubs eventhub consumer-group create --resource-group MyResourceGroupName --namespace-name MyNamespaceName --eventhub-name MyEventHubName --set partitioncount=12`

**This answer is incorrect.**

`az eventhubs eventhub update --resource-group MyResourceGroupName --namespace-name MyNamespaceName --name MyEventHubName --partition-count 12`

**This answer is correct.**

`az eventhubs eventhub create --resource-group MyResourceGroupName --namespace-name MyNamespaceName --name MyEventHubName --partition-count 12`

This item tests the candidate’s knowledge of developing event-based solutions.

The code segment that includes `az eventhubs eventhub update` adds partitions to an existing event hub. The code segment that includes `az eventhubs eventhub consumer-group update` updates the event hub consumer group. The code segment that includes `az eventhubs eventhub consumer-group create` will create an event hub consumer group. The code segment that includes `az eventhubs eventhub create --resource-group` segment will create an event hub with partitions, not change an existing one

[Tutorial: Host a RESTful API with CORS in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-rest-api)

Question 23 of 50
You manage an Azure event hub.
You need to ensure that multiple load-balanced instances of a .NET application (version 5.0) can be used to scale event processing.
Which event processor client should you use?
Select only one answer.

`EventHubConsumerClient`

`EventProcessorHost`

`EventHubProducerClient`

`EventProcessorClient`

**This answer is correct.**

This item tests the candidate’s knowledge of scaling event processing applications, which is part of developing event-based solutions.

`EventProcessorClient` balances the load between multiple instances of a program in newer .NET versions (version 5.0). `EventHubConsumerClient` balances the load between multiple instances of a program in Python and JavaScript. `EventProcessorHost` balances the load between multiple instances of a program in earlier .NET versions. The `EventHubProducerClient` class is used to send events to an event hub.

[Explore Azure Event Hubs - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/azure-event-hubs/)

[Scale your processing application - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/azure-event-hubs/4-event-processing)

Question 24 of 50
You need to capture events streaming from Azure Event Hubs.
To which three locations can you capture data? Each correct answer presents a complete solution.
Select all answers that apply.
Azure Blob storage

**This answer is correct.**

Azure Data Lake Storage Gen1

**This answer is correct.**

Azure Functions

Azure Stream Analytics

Azure Data Lake Storage Gen2

**This answer is correct.**

This item tests the candidate’s knowledge of implementing solutions that use Azure Event Hubs.

Azure Event Hubs Capture can automatically deliver the streaming data in Event Hubs to Azure Blob storage. Azure Event Hubs Capture can automatically deliver the streaming data in Event Hubs to Azure Data Lake Storage Gen1. Azure Event Hubs Capture can automatically deliver the streaming data in Event Hubs to Azure Data Lake Storage Gen2. Azure Functions and Azure Stream Analytics cannot be used to capture events from Azure Event Hubs.

[Explore Azure Event Hubs - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/azure-event-hubs/)

Question 25 of 50
A company is developing an IoT solution for smart buildings that collects telemetry data from various sensors. The data is sent to Azure for real-time analysis and storage.
You need to implement a solution that allows the ingestion of high volumes of events and provides reliable delivery to downstream processing services with minimal latency.
Which service should you use?
Select only one answer.
Azure Blob Storage

Azure Event Grid

Azure Event Hubs

**This answer is correct.**

Azure Service Bus

Azure Event Hubs is designed for high-throughput, real-time event streaming and is compatible with Apache Kafka, making it suitable for IoT scenarios. Azure Event Grid is more suited for event routing and serverless applications. Azure Service Bus is better for traditional enterprise messaging patterns, and Azure Blob Storage is not optimized for real-time event ingestion.

[Explore Azure Event Grid - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/azure-event-grid/2-event-grid-overview)  
[Discover Azure Event Hubs - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/azure-event-hubs/2-event-hubs-overview)  
[What is Azure Event Grid? - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/event-grid/overview)

Question 26 of 50
You have an Azure Service Bus instance.
You need to provide first-in, first-out (FIFO) guarantee for message processing.
What should you configure?
Select only one answer.

dead-letter queue

message deferral

message sessions

**This answer is correct.**

scheduled delivery

This item tests the candidate’s knowledge of setting up FIFO guarantees in Azure Service Bus, which is a common task when implementing solutions by using Azure Service Bus.

To provide FIFO guarantees in Service Bus, sessions must be configured. Message sessions enable exclusive, ordered handling of unbounded sequences of related messages. A dead-letter queue holds messages that cannot be delivered to any receiver. Message deferral makes it possible to defer retrieval of a message until a later time. Scheduled delivery allows submitting messages to a queue or topic for delayed processing. A dead-letter queue, message deferral, and scheduled delivery do not provide FIFO guarantees.

[Explore Azure Service Bus - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/discover-azure-message-queue/3-azure-service-bus-overview)

Question 27 of 50
You need to write a filter condition for an Azure Service Bus topic.
Which three filters can you use? Each correct answer presents a complete solution.
Select all answers that apply.
SQL

**This answer is correct.**

Boolean

**This answer is correct.**

Size

Correlation

**This answer is correct.**

Content

This item tests the candidate’s knowledge of implementing solutions that use Azure Service Bus.

A SqlFilter holds a SQL-like conditional expression that is evaluated in the broker against the arriving message’s user-defined properties and system properties. The TrueFilter and FalseFilter either cause all arriving messages (true) or none of the arriving messages (false) to be selected for the subscription. A CorrelationFilter holds a set of conditions that are matched against one or more of an arriving message's user and system properties. Size Filter and Content are not valid options for Service Bus topic filtering.

[Implement message-based communication workflows with Azure Service Bus - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/implement-message-workflows-with-service-bus/)


Question 28 of 50
You have an application that requires message queuing.
You need to recommend a solution that meets the following requirements:
- automatic duplicate message detection.
- ability to send 2 MB messages.
Which message queuing solution should you recommend?
Select only one answer.
Azure Service Bus Premium tier

**This answer is correct.**

Azure Service Bus Standard tier

Azure Storage queues with locally redundant storage (LRS)

Azure Storage queues with zone-redundant storage (ZRS)

This item tests the candidate's knowledge of Azure Service Bus.

Service Bus detects duplicate messages. The Premium tier is required to send messages larger than 256 KB. Although Service Bus detects duplicate messages, the Standard tier only supports messages that are up to 256 KB in size. Azure Storage queues do not support duplicate message detection. Azure Storage queues do not support duplicate message detection.

[Explore Azure Service Bus - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/discover-azure-message-queue/3-azure-service-bus-overview)

Question 29 of 50
A logistics company requires a messaging system that can automatically handle messages that cannot be processed after several attempts, moving them to a separate storage for later analysis.
You need to choose a queue service that supports automatic handling of non-processable messages.
What should you use?
Select only one answer.

Azure Event Grid with advanced filtering

Azure Queue Storage with message expiration

Azure Service Bus dead-letter queue

**This answer is correct.**

Azure Storage queues with visibility timeout

Azure Service Bus dead-letter queue is designed to hold messages that cannot be delivered to any receiver or are not processed successfully, which is suitable for the company's requirement. Azure Storage queues with visibility timeout only hide messages temporarily and do not move them to separate storage. Azure Event Grid with advanced filtering is for event routing, not for handling failed message processing. Azure Queue Storage with message expiration simply deletes expired messages rather than moving them for analysis.

[Discover Azure message queues - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/discover-azure-message-queue)  
[Storage queues and Service Bus queues - compared and contrasted - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-azure-and-service-bus-queues-compared-contrasted)


Question 30 of 50
You manage an Azure App Service web app named **app1**. App1 is registered as an application in Microsoft Entra ID.
You need to ensure that Microsoft Entra ID signed-in user information can be retrieved by app1 by using Microsoft Graph.
What should you configure?
Select only one answer.
appRoles

application permissions

groupMembershipClaims

delegated permissions

**This answer is correct.**

This item tests the candidate’s knowledge of accessing user data from Microsoft Graph, which is part of implementing user authentication and authorization.

Delegated permissions are used by apps that have a signed-in user present. For these apps, either the user or an administrator consents to the permissions that the app requests and the app can function as the signed-in user when making calls to Microsoft Graph. appRoles is an attribute in the application manifest of the registered application that specifies the collection of roles that an app may declare. These roles can be assigned to users, groups, or service principals. Application permissions are used by apps that run without a signed-in user present. For example, apps that run as background services or daemons. An administrator can only permit application permissions. groupMembershipClaims is an attribute in the application manifest of the registered application that configures the groups claim issued in a user or OAuth 2.0 access token that the app expects. AppRoles, application permissions, and groupMembershipClaims will not allow signed-in user information to be retrieved in the code.

[Access user photo information by using Microsoft Graph - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/msgraph-user-photo-information/)


Question 31 of 50
You manage an Azure App Service web app named **app1**. App1 is registered as a multi-tenant application in a Microsoft Entra ID tenant named **tenant1**.
You need to grant app1 the permission to access the Microsoft Graph API in tenant1.
Which service principal should you use?
Select only one answer.
legacy

system-assigned managed identity

application

**This answer is correct.**

user-assigned managed identity

This item tests the candidate’s knowledge of accessing user data from Microsoft Graph, which is part of implementing user authentication and authorization.

A Microsoft Entra ID application is defined by its one and only application object, which resides in the Microsoft Entra ID tenant where the application was registered (known as the application's home tenant). The application service principal is used to configure permission for app1 in tenant1 to access the Microsoft Graph API. The legacy service principal is a legacy app, which is an app created before app registrations were introduced or an app created through legacy experiences. Managed identities eliminate the need to manage credentials in code. A system-assigned managed identity is restricted to one per resource and is tied to the lifecycle of the resource. Managed identities for Azure resources eliminate the need to manage credentials in code. A user-assigned managed identity can be created and assigned to one or more instances of an Azure service. The legacy, system-assigned managed identity, and user-assigned managed identity cannot be used to assign permission for app1 in tenant1 to access the Microsoft Graph API.

[Explore the Microsoft identity platform - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-microsoft-identity-platform/)

[Explore service principals - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/explore-microsoft-identity-platform/3-app-service-principals)

Question 32 of 50
You have blobs in an Azure storage account.
You need to implement a stored access policy that will apply to shared access signatures generated for the blobs.
To which type of storage resource should you associate the policy?
Select only one answer.
the storage account

the blob service of the storage account

the container that is hosting blobs

**This answer is correct.**

each individual blob

This item tests the candidate’s knowledge of configuring stored access policy, which is part of implementing authorization.

The container that is hosting blobs is used for associating the corresponding stored access policies. The storage account can be associated with shared access signatures keys but not stored access policies. The blob service of the storage account can be associated with shared access signatures keys but not stored access policies. Each individual blob can be associated with shared access signatures keys but not stored access policies.

[Define a stored access policy](https://learn.microsoft.com/en-us/rest/api/storageservices/define-stored-access-policy)

Question 33 of 50
You develop an application. The application will be accessed by a supplier.
The supplier requires a shared access signature (SAS) to access Azure services in your company’s subscription.
You need to secure the SAS.
Which three actions should you take? Each correct answer presents a complete solution.
Select all answers that apply.
Always use HTTPS.

**This answer is correct.**

Grant permission to multiple resources.

Use Azure Monitor and Azure Storage logs to monitor the application.

**This answer is correct.**

Define a stored access policy for a service SAS.

**This answer is correct.**

Set a long expiration time.

This item tests the candidate’s knowledge of creating and implementing shared access signatures (SAS).

The recommendation of always using HTTPS is valid and should be followed. Azure Monitor and storage analytics logging should be used to observe any spike in these types of authorization failures. Stored access policies will give the option to revoke permissions for a service SAS without having to regenerate the storage account keys. A security best practice is to provide a user with the minimum required privileges. It is best to use near-term expiration times on an ad-hoc SAS service or account SAS so that even if a SAS is compromised it is valid only for a short time.

[Grant limited access to Azure Storage resources using shared access signatures (SAS)](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview)

Question 34 of 50
You plan to generate a shared access signature (SAS) token for read access to a blob in a storage account.
You need to secure the token from being compromised.
What should you use?
Select only one answer.
Primary account key

Secondary account key

Microsoft Entra ID credentials assigned the Contributor role

**This answer is correct.**

Microsoft Entra ID credentials assigned the Reader role

This item tests the candidate's knowledge of Azure Storage shared access signatures (SAS).

Microsoft Entra ID credentials are required to generate the SAS token. The account used must have the Microsoft.Storage/storageAccounts/blobServices/generateUserDelegationKey permission, which is present in the following built-in roles: Contributor, Storage Account Contributor, Storage Blob Data Contributor, Storage Blob Data Owner, Storage Blob Data Reader, and Storage Blob Delegator. The account key can be used to generate the SAS token, but it can be more easily compromised.

[Discover shared access signatures - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/implement-shared-access-signatures/2-shared-access-signatures-overview)


Question 35 of 50
You need to generate a shared access signature token that grants the Read permission to a blob container.
Which code segment should you use?
Select only one answer.

```
BlobSasBuilder sasBuilder = new BlobSasBuilder()
{
BlobContainerName = containerClient.Name,
Resource = "b"
};
sasBuilder.ExpiresOn = DateTimeOffset.UtcNow.AddHours(1);
sasBuilder.SetPermissions(BlobContainerSasPermissions.Read);
Uri sasUri = containerClient.GenerateSasUri(sasBuilder);
```


```
BlobSasBuilder sasBuilder = new BlobSasBuilder()
{
BlobContainerName = containerClient.Name,
Resource = "c"
};
sasBuilder.ExpiresOn = DateTimeOffset.UtcNow.AddHours(1);
sasBuilder.SetPermissions(BlobContainerSasPermissions.Read);
Uri sasUri = containerClient.GenerateSasUri(sasBuilder);
```

**This answer is correct.**

```
BlobSasBuilder sasBuilder = new BlobSasBuilder()
{
BlobContainerName = containerClient.Name,
Resource = “c”
};
sasBuilder.ExpiresOn = DateTimeOffset.UtcNow.AddHours(1);
sasBuilder.SetPermissions(BlobContainerSasPermissions.Create);
Uri sasUri = containerClient.GenerateSasUri(sasBuilder);
```

```
BlobSasBuilder sasBuilder = new BlobSasBuilder()
{
BlobContainerName = containerClient.Name,
Resource = "b"
};
sasBuilder.ExpiresOn = DateTimeOffset.UtcNow.AddHours(1);
sasBuilder.SetPermissions(BlobContainerSasPermissions.Create);
Uri sasUri = containerClient.GenerateSasUri(sasBuilder);
```

This item tests the candidate’s knowledge of creating and implementing shared access signatures.

The code segment that includes `Resource = "c"` and `sasBuilder.SetPermissions(BlobContainerSasPermissions.Read); will generate the shared access signatures token that grants the Read permission to a blob container. The code segment that includes resource = ‘b’ will generate a shared access signatures token at the blob level. The code segments that include sasBuilder.SetPermissions(BlobContainerSasPermissions.Create); will generate a shared access signatures token with the Create permission at the blob level.`

[Store data in Azure learning path - Training | Microsoft Learn](https://learn.microsoft.com/training/paths/store-data-in-azure/)

Question 36 of 50
You plan to create a key namespace hierarchy in Azure App Configuration.
You need to separate individual key names.
Which character should you use?
Select only one answer.
:

**This answer is correct.**

*

,

\

This item tests the candidate’s knowledge of configuring key namespace hierarchy of App Configuration, which is part of implementing secure cloud solutions.

The colon character (:) is used to separate names of individual keys when creating a namespace hierarchy in Azure App Configuration. The asterisk character (*) is one of reserved characters in Azure App Configuration, so it cannot be used to separate names of individual keys when creating a namespace hierarchy in Azure App Configuration. The comma character (,) is one of reserved characters in Azure App Configuration, so it cannot be used to separate names of individual keys when creating a namespace hierarchy in Azure App Configuration. The backslash character () is one of reserved characters in Azure App Configuration, so it cannot be used to separate names of individual keys when creating a namespace hierarchy in Azure App Configuration.

[Create paired keys and values - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/implement-azure-app-configuration/3-keys-values)


Question 37 of 50
You are developing a solution that stores secrets in an Azure Key Vault named myvault.
You need to retrieve the value for a secret named mysecret that is stored in myvault.
Which CLI command should you use?
Select only one answer.

`az keyvault secret recover --name mysecret --vault-name myvault`

`az keyvault secret recover --id myvault/mysecret`

`az keyvault secret show --id myvault/mysecret`

`az keyvault secret show --name mysecret --vault-name myvault`

**This answer is correct.**

This item tests the candidate’s knowledge of developing code that uses keys, secrets, and certificates stored in Azure Key Vault. The CLI command `az keyvault` offers several commands to work with secrets. The most commonly used commands are `set` for storing a secret and `show` to get the secret’s value. When using these commands, either an id specifying the full secret identification (in the format https://keyvaultname.vault.azure.net/secrets/secret-name/secret-version) or the secret and the vault name must be specified.

[Exercise: Set and retrieve a secret from Azure Key Vault by using Azure CLI](https://learn.microsoft.com/training/modules/implement-azure-key-vault/5-set-retrieve-secret-azure-key-vault)

Question 38 of 50
You are tasked with enhancing the security of an existing Azure web application. The application currently stores sensitive configuration data such as connection strings and API keys in its code, which has led to security concerns.
You need to secure the app configuration data to prevent unauthorized access and potential data breaches, while ensuring seamless access for the application itself.
Which two options can achieve this goal? (Choose two.)
Select all answers that apply.
Encrypt the sensitive data and store it within the application code, providing decryption keys to authorized personnel only.

Migrate the sensitive configuration data to Azure Key Vault and utilize Managed Identities to securely access the secrets.

**This answer is correct.**

Move the sensitive configuration data to a private GitHub repository and access it using GitHub credentials stored in the application settings.

Store the sensitive configuration data in Azure App Configuration and restrict access using Azure role-based access control (RBAC).

**This answer is correct.**

Storing sensitive configuration data in Azure App Configuration and restricting access with Azure RBAC is a secure method to manage app settings while maintaining control over who can access the data. Migrating sensitive data to Azure Key Vault and using Managed Identities allows the application to authenticate to services that support Azure AD authentication without needing credentials in the code, which enhances security. Encrypting the data and storing it within the application code does not follow security best practices as it still resides within the codebase and could be exposed. Storing sensitive data in a private GitHub repository is not secure as it relies on GitHub credentials, which if compromised, could lead to unauthorized access.  
[Implement Azure Key Vault - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/implement-azure-key-vault/)  
[Implement Azure App Configuration - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/implement-azure-app-configuration/)


Question 39 of 50
A development team is using Application Insights to monitor their web application deployed on Azure. They have noticed discrepancies in the reported metrics due to high telemetry volume.
You need to ensure that the reported metrics accurately reflect the application's performance without being affected by telemetry sampling.
What should you implement to achieve this goal?
Select only one answer.
Configure Application Insights to use preaggregated standard metrics for dashboarding and real-time alerting.

**This answer is correct.**

Create a custom Kusto query in Application Insights to manually aggregate log-based metrics.

Disable all telemetry sampling in Application Insights to ensure all events are collected.

Increase the sampling rate in Application Insights to collect more data points for log-based metrics.

Preaggregated standard metrics are not affected by telemetry sampling and provide accurate real-time data, which makes them suitable for dashboarding and alerting. Increasing the sampling rate or disabling sampling altogether would increase costs and may still not provide accurate metrics due to the volume of data. Creating a custom Kusto query would require manual effort and does not address the issue of sampling affecting the metrics.

[Metrics in Application Insights - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/app-insights-metrics "Metrics in Application Insights - Training | Microsoft Learn")

[Discover log-based metrics - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/monitor-app-performance/3-logs-based-metrics "Discover log-based metrics - Training | Microsoft Learn")

Question 40 of 50
You have an Azure App Service web app.
You enable Application Insights for the app.
You need to view detailed information about each user who signs in to the app, including what the user does while signed in.
Which type of telemetry data should you filter by using Application Insights?
Select only one answer.
dependencies

events

**This answer is correct.**

requests

traces

The correct solution is to filter by **events**, because Application Insights events are custom telemetry designed to track user actions and behaviors inside the app, such as button clicks, page navigation, or other activities performed while signed in. **Requests** represent incoming HTTP calls to the app and provide details about performance and response codes, but they don’t capture what a user does within the app. **Dependencies** track calls to external resources like databases or APIs, and **traces** log diagnostic information from the application. To understand **per-user activity** inside the application, events are the appropriate telemetry type.

[Summary](https://learn.microsoft.com/en-us/training/modules/route-system-feedback/5-summary)  
[Implement Application Insights](https://learn.microsoft.com/en-us/training/modules/implement-tools-track-usage-flow/7-implement-application-insights)  
[Use Azure Application Insights](https://learn.microsoft.com/en-us/training/modules/configure-azure-app-services/10-use-application-insights)  
[Monitor Azure resources with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/monitor-azure-resource)

Question 41 of 50
You have a web service in Azure that uses an Azure SQL Database instance and is instrumented by using Application Insights.
You need to write a query to identify how long it takes for a specific web service call to retrieve data from the database.
Which type of data should you query in Application Insights?
Select only one answer.
customEvents

dependencies

**This answer is correct.**

performanceCounters

requests

The correct solution is to query **dependencies**, because Application Insights tracks external calls made by your service, including SQL Database queries, REST APIs, and storage operations. Dependency telemetry includes duration, success/failure, and target resource, making it ideal for measuring how long a web service call takes to retrieve data from the database. **customEvents** capture user-defined actions in the application but do not include database timings. **performanceCounters** provide system-level metrics such as CPU or memory usage, and **requests** represent incoming calls to the web service, not outbound database calls. Therefore, dependency data is the right source for identifying query durations to Azure SQL Database.

[Use Azure Application Insights](https://learn.microsoft.com/en-us/training/modules/configure-azure-app-services/10-use-application-insights)  
[Monitor Azure resources with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/monitor-azure-resource)  
[Describe Azure Monitor](https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/4-describe-azure-monitor)  
[Monitor your networks using Azure Monitor](https://learn.microsoft.com/en-us/training/modules/design-implement-network-monitoring/2-monitor-networks-using-azure-monitor)

Question 42 of 50
You deploy a web app named App1 by using Azure DevOps. App1 includes releases for a mobile app and a desktop app.
You need to perform a root cause analysis (RCA) to monitor the performance of App1. The solution must meet the following requirements:
- Identify related code that causes load.
- Ensure that you can view logs and identify any failures that cause issues with the desktop app.
- Minimize administrative effort.
What should you use?
Select only one answer.
Application Insights

**This answer is correct.**

Azure Analytics

Azure Monitor

Log Analytics

The correct solution is **Application Insights**, because it is designed to provide deep application performance monitoring, transaction traces, exception logging, and telemetry that links failures directly to code, making it ideal for root cause analysis of both web and desktop components. It integrates easily with DevOps pipelines and requires minimal setup once enabled. **Azure Monitor** provides high-level observability across Azure resources but lacks the detailed code-level diagnostics needed for RCA. **Log Analytics** is used to query and analyze log data, often from Application Insights or Azure Monitor, but by itself it does not capture application telemetry. **Azure Analytics** is not a valid Azure monitoring service. Therefore, Application Insights best satisfies the requirements with the least administrative effort.

[Explore Application Insights](https://learn.microsoft.com/en-us/training/modules/implement-tools-track-usage-flow/6-explore-application-insights)  
[Monitor Azure Functions and Event Hubs](https://learn.microsoft.com/en-us/azure/architecture/serverless/event-hubs-functions/observability)  
[Monitor Azure resources with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/monitor-azure-resource)  
[Use Azure Application Insights](https://learn.microsoft.com/en-us/training/modules/configure-azure-app-services/10-use-application-insights)   
[Implement Application Insights](https://learn.microsoft.com/en-us/training/modules/implement-tools-track-usage-flow/7-implement-application-insights)  
[Summary](https://learn.microsoft.com/en-us/training/modules/route-system-feedback/5-summary)

Question 43 of 50
You manage an Azure Cosmos DB database named **database1**.
You need to read items from the database without any ordering guarantee and ensure the highest availability.
Which consistency level should you use?
Select only one answer.
strong

bounded staleness

session

eventual

**This answer is correct.**

This item tests the candidate’s knowledge of consistency levels in Azure Cosmos DB, which is part of developing solutions that use Azure Cosmos DB storage.

Eventual consistency has the loosest consistency and commits any write operation against the primary immediately. This will provide the highest availability and lowest consistency. Strong consistency offers a linearizability guarantee. Linearizability refers to serving requests concurrently. Users are always guaranteed to read the latest committed write. Strong consistency suffers from reduced availability. Bounded staleness consistency will not provide the highest availability. When a client performs read operations within a region that accepts writes, the guarantees provided by bounded staleness consistency and strong consistency are identical. Session consistency guarantees that all read and write operations are consistent within a user session. Because the application does not require consistency guarantee, this consistency level is not appropriate.

[AZ-204: Develop solutions that use Azure Cosmos DB - Training | Microsoft Learn](https://learn.microsoft.com/training/paths/az-204-develop-solutions-that-use-azure-cosmos-db/)


Question 44 of 50
You manage an Azure Cosmos DB container named **container1**.
You need to use the `ReadItemAsync` method to read an item from the Azure Cosmos service.
Which two parameters should you provide? Each correct answer presents part of the solution.
Select all answers that apply.
`consistencyLevel`

`eTag`

`partitionKey`

**This answer is correct.**

`sessionToken`

`id`

**This answer is correct.**

This item tests the candidate’s knowledge of setting the partition key, which is part of developing Azure Cosmos DB solutions.

The `ReadItemAsync` method of the container class of .NET SDK for Azure Cosmos DB has two mandatory parameters: `partitionKey` and `itemId`. The `consistencyLevel` parameter is part of the optional `requestOptions` parameter of the `ReadItemAsync`.

The `eTag` and `sessionToken` parameters are part of the optional `requestOptions` parameter of the `ReadItemAsync` method.

[Explore Microsoft .NET SDK v3 for Azure Cosmos DB - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/work-with-cosmos-db/2-cosmos-db-dotnet-overview)

Question 45 of 50
You plan to implement a storage mechanism for managing state across multiple change feed consumers.
You need to configure the change feed processor in the .NET SDK for Azure Cosmos DB for NoSQL API.
Which component should you use?
Select only one answer.
Delegate

Compute instance

Lease container

**This answer is correct.**

Monitored container

**This answer is incorrect.**

This item tests the candidate’s knowledge of configuring change feed processor as part of developing solutions that use Azure Cosmos DB.

The lease container component serves as a storage mechanism to manage state across multiple change feed consumers. The delegate component is the code within the client application that implements business logic for each batch of changes. The compute instance is a client application instance that listens for changes from the change feed. The monitored container component is monitored for any insert or update operations. It does not serve as a storage mechanism to manage state across multiple change feed consumers.

[Understand change feed features in the SDK - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/consume-azure-cosmos-db-sql-api-change-feed-use-sdk/2-understand-features-sdk)

Question 46 of 50
A company implements a multi-region Azure Cosmos DB account.
You need to configure the default consistency level for the account. The consistency level must ensure that update operations made as a batch within a transaction are always visible together.
Which consistency level should you use?
Select only one answer.
Bounded Staleness

Session

**This answer is incorrect.**

Consistent Prefix

**This answer is correct.**

Eventual

This item tests the candidate’s knowledge of selecting the appropriate consistency level for operations in Azure Cosmos DB. The Consistent Prefix consistency level ensures that updates made as a batch within a transaction are returned consistently with the transaction in which they were committed. Write operations within a transaction of multiple documents are always visible together. The Bounded Staleness consistency level is used to manage the lag of data between any two regions based on an updated version of an item or the time intervals between read and write. The Session consistency level is used to ensure that within a single client session, reads are guaranteed to honor the read-your-writes and write-follows-reads guarantees. The Eventual consistency level is used when no ordering guarantee is required.

[Explore consistency levels](https://learn.microsoft.com/training/modules/explore-azure-cosmos-db/4-cosmos-db-consistency-levels-overview)

Question 47 of 50
You have an Azure storage lifecycle policy for block blobs.
You need to create a prefixMatch filter rule that will contain an array of strings for prefixes to be matched.
What should be the first element of the prefix string?
Select only one answer.
a block blob index tag

a block blob name

a container name

**This answer is correct.**

a storage account name

This item tests the candidate’s knowledge of configuring prefixMatch filter, which is an essential part of setting up storage policy and is part of solution development for blob storage.

When creating a prefixMatch filter rule for an Azure storage lifecycle policy for block blobs, the first element of the prefix string must be a container name not a block blob index tag, block blob name, or storage account name.

[Discover Blob storage lifecycle policies - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/manage-azure-blob-storage-lifecycle/3-blob-storage-lifecycle-policies)

Question 48 of 50
You need to implement an Azure Storage lifecycle policy for append blobs.
Which rule action should you use?
Select only one answer.
delete

**This answer is correct.**

enableAutoTierToHotFromCool

tierToArchive

tierToCool

This item tests the candidate’s knowledge of configuring Azure Storage lifecycle policy for blobs, which is an essential part of developing solutions for blob storage.

The delete rule action supports both block blobs and append blobs. The enableAutoTierToHotFromCool, tierToArchive, and tierToCool rule actions only supports block blobs.

[Discover Blob storage lifecycle policies - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/manage-azure-blob-storage-lifecycle/3-blob-storage-lifecycle-policies)

Question 49 of 50
You need to rehydrate a blob stored in the Archive tier by changing the access tier.
Which destination blob should you use?
Select only one answer.

A blob in the Archive tier in the same region.

A blob in the Archive tier in a different region.

A blob in the Cool tier in a different region.

A blob in the Cool tier in the same region.

**This answer is correct.**

This item tests the candidate’s knowledge of rehydrating blobs.

Blobs in the Archive tier can be rehydrated only to online tiers (that is, Cool or Hot). The destination can be any storage account in the same region.

[Rehydrate blob data from the archive tier - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/manage-azure-blob-storage-lifecycle/5-rehydrate-blob-data)

Question 50 of 50
You are developing an application.
You need to set the standard HTTP properties of containers in Azure Blob Storage.
Which two HTTP properties can you set? Each correct answer presents part of the solution.
Select all answers that apply.
ETag

**This answer is correct.**

Last-Modified

**This answer is correct.**

Cache-Control

Origin

Range

This item tests the candidate’s knowledge of setting and retrieving properties and metadata. Metadata in Azure Storage objects is defined through headers starting with x-ms-meta-. Some standard HTTP properties are also available for both objects and containers. The only two HTTP properties that are available for containers are ETag and Last-Modified.

Last-Modified, Cache-Control, Origin and Range are properties only available for blobs.

[Set and retrieve properties and metadata for blob resources by using REST](https://learn.microsoft.com/training/modules/work-azure-blob-storage/5-set-retrieve-properties-metadata-rest)
