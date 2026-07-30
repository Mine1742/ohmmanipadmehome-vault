# 

This study guide provides a structured review of the core concepts, services, and architectures required for the AZ-204 Azure Developer Associate certification, based on the updated 2026 exam requirements.

## Section 1: Review Quiz

**Instructions:** Answer the following questions in 2–3 sentences based on the provided technical documentation.

1. **What is the fundamental distinction between an Azure App and an Azure App Service Plan?**
2. **How do Vertical Scaling (Scale Up) and Horizontal Scaling (Scale Out) differ in the context of Azure App Service?**
3. **In Azure Cosmos DB, which consistency level should be selected if a user must immediately see their own profile updates, while other global users can tolerate a brief delay?**
4. **What are the primary differences between System-Assigned and User-Assigned Managed Identities?**
5. **How does Azure Key Vault utilize "Soft Delete" and "Purge Protection" to secure sensitive data?**
6. **When should a developer choose Azure Service Bus over Azure Storage Queues for a messaging solution?**
7. **What is the purpose of the "Orchestrator" function in Azure Durable Functions, and what is its most critical constraint?**
8. **Describe the primary function of an API Gateway within Azure API Management (APIM).**
9. **What is "Event Hubs Capture," and how does it benefit data processing workflows?**
10. **What is the "Instance Metadata Service (IMDS)," and why is it essential for Managed Identities?**

--------------------------------------------------------------------------------

## Section 2: Quiz Answer Key

1. **What is the fundamental distinction between an Azure App and an Azure App Service Plan?** An App Service Plan represents the physical compute resources (CPU, memory, and instances) of a managed farm, essentially acting as the "gym membership." In contrast, the App is the actual code and configuration—the "workout"—that runs inside that allocated capacity.
2. **How do Vertical Scaling (Scale Up) and Horizontal Scaling (Scale Out) differ in the context of Azure App Service?** Vertical scaling involves increasing the capacity of a single instance by adding more CPU, RAM, or faster storage (making the machine "bigger"). Horizontal scaling involves adding more instances of the same size to distribute the workload across multiple machines (adding "more" machines).
3. **In Azure Cosmos DB, which consistency level should be selected if a user must immediately see their own profile updates, while other global users can tolerate a brief delay?** Session consistency is the most appropriate choice because it guarantees that a user can always read their own writes within their specific session. While the individual user sees changes immediately, the rest of the world catches up later, providing a balance of high availability and low latency.
4. **What are the primary differences between System-Assigned and User-Assigned Managed Identities?** A System-Assigned identity is tied to the lifecycle of a specific Azure resource and is deleted when that resource is deleted. A User-Assigned identity is a standalone Azure resource that can be assigned to multiple resources and persists even if the associated resources are removed.
5. **How does Azure Key Vault utilize "Soft Delete" and "Purge Protection" to secure sensitive data?** Soft Delete ensures that deleted vaults or objects are recoverable for a retention period of 7–90 days rather than being immediately destroyed. Purge Protection adds a layer of security by preventing even administrators from permanently deleting those soft-deleted items until the retention period expires.
6. **When should a developer choose Azure Service Bus over Azure Storage Queues for a messaging solution?** Service Bus should be chosen when the solution requires guaranteed First-In-First-Out (FIFO) ordering, automatic duplicate detection, or support for messages exceeding 64 KB. It is also preferred for complex patterns like transactional behavior or long-running parallel streams.
7. **What is the purpose of the "Orchestrator" function in Azure Durable Functions, and what is its most critical constraint?** The Orchestrator defines the stateful workflow by sequencing activity functions and checkpointing progress after every await call. Its most critical constraint is that it must be deterministic; it cannot use direct I/O, random numbers, or volatile data like current timestamps.
8. **Describe the primary function of an API Gateway within Azure API Management (APIM).** The API Gateway acts as a reverse proxy that routes requests from clients to backend services while collecting telemetry. It also enforces policies such as authentication, rate limiting, and SSL termination to protect and optimize the API.
9. **What is "Event Hubs Capture," and how does it benefit data processing workflows?** Event Hubs Capture is a built-in feature that automatically archives streaming data to Azure Blob Storage or Data Lake at specified time or size intervals. It allows for long-term storage and batch analytics without requiring additional custom code to move the data.
10. **What is the "Instance Metadata Service (IMDS)," and why is it essential for Managed Identities?** The IMDS is a special HTTP endpoint (accessible only from within the Azure resource) that provides metadata about the running instance. Managed Identities use this endpoint to request and receive security tokens from Microsoft Entra ID without the application ever seeing or managing credentials.

--------------------------------------------------------------------------------

## Section 3: Essay Questions

**Instructions:** These questions are designed to test deep architectural understanding. No answers are provided.

1. **The Evolution of the AZ-204 Exam Philosophy:** Analyze the shift in the 2026 exam update from "service recognition" to "production readiness." Discuss how this change impacts the way a developer must approach monitoring, troubleshooting, and securing an Azure application.
2. **Architecting for Global Consistency:** Compare and contrast the five consistency levels of Azure Cosmos DB. Under what specific business scenarios would "Bounded Staleness" be a superior architectural choice over "Strong" or "Eventual" consistency?
3. **Messaging vs. Eventing:** Evaluate the technical trade-offs between using Azure Event Grid, Azure Event Hubs, and Azure Service Bus. Create a hypothetical scenario involving a high-volume IoT telemetry system and determine which service (or combination of services) provides the most scalable solution.
4. **Zero-Credential Architecture:** Explain how the integration of Azure Key Vault and Managed Identity facilitates a "Zero-Credential" security model. Detail the flow of an application fetching a secret from Key Vault using the `DefaultAzureCredential` class.
5. **Serverless Scaling and Cold Starts:** Compare the Consumption, Premium, and Dedicated hosting plans for Azure Functions. Discuss the technical "cold start" phenomenon and how a developer can utilize the Premium plan or "Always On" settings to mitigate its impact on latency-sensitive applications.

--------------------------------------------------------------------------------

## Section 4: Comprehensive Glossary

|                                      |                                                                                                                                                                 |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Term                                 | Definition                                                                                                                                                      |
| **ACR (Azure Container Registry)**   | A managed, private Docker registry service based on the open-source Docker Registry 2.0 for storing and managing container images.                              |
| **ACI (Azure Container Instances)**  | A service that allows for the launching of containers without managing the underlying virtual machines; billed per second.                                      |
| **AMQP 1.0**                         | The standard protocol used for communication with Azure Service Bus and Event Hubs.                                                                             |
| **API Management (APIM)**            | A platform for publishing, securing, and analyzing APIs through gateways, developer portals, and policy enforcement.                                            |
| **App Service Plan**                 | The compute infrastructure (CPU, memory, instances) that hosts one or more App Service web apps.                                                                |
| **ARM Template**                     | A declarative JSON file used for Infrastructure as Code (IaC) to define and deploy Azure resources.                                                             |
| **Azure Functions**                  | A serverless, event-driven compute service that executes code in response to triggers like HTTP requests or timers.                                             |
| **Bounded Staleness**                | A Cosmos DB consistency level where reads lag behind writes by a user-defined period of time or number of versions.                                             |
| **Change Feed**                      | A feature in Cosmos DB that provides a sorted list of documents in the order they were modified, enabling near real-time response to changes.                   |
| **Consistent Prefix**                | A consistency level guaranteeing that reads never see out-of-order writes, though they may lag behind the latest committed data.                                |
| **Consumer Group**                   | A named "view" of an Event Hub that maintains its own read position (offset), allowing multiple apps to read the same stream independently.                     |
| **DefaultAzureCredential**           | A class in the Azure Identity SDK that automatically attempts several authentication methods (e.g., Managed Identity, environment variables) to secure a token. |
| **Deployment Slots**                 | Live apps with their own hostnames that allow for staging, testing, and zero-downtime swaps with the production environment.                                    |
| **Durable Functions**                | An extension of Azure Functions that allows for stateful, long-running workflows and orchestration patterns like fan-out/fan-in.                                |
| **Event Grid**                       | A serverless eventing backplane that routes events from various sources to subscribers using a push-push model.                                                 |
| **Event Hubs**                       | A massive-scale data streaming platform and ingestion service capable of receiving millions of events per second.                                               |
| **Kusto (KQL)**                      | The query language used in Log Analytics and Azure Monitor to analyze large volumes of telemetry data.                                                          |
| **Managed Identity**                 | An identity automatically managed by Microsoft Entra ID that allows resources to authenticate to other services without stored credentials.                     |
| **Microsoft Entra ID**               | Formerly Azure Active Directory (AAD); a cloud-based identity and access management service.                                                                    |
| **Partition Key**                    | A property used in Cosmos DB or Event Hubs to group data into logical partitions for performance and horizontal scaling.                                        |
| **Policy (APIM)**                    | A collection of XML-based statements that change the behavior of an API (e.g., converting JSON to XML or enforcing rate limits).                                |
| **RBAC (Role-Based Access Control)** | A system that manages access to Azure resources by assigning specific roles to identities at various scopes.                                                    |
| **SAS (Shared Access Signature)**    | A signed URI that grants restricted access rights to Azure Storage resources for a specified period of time.                                                    |
| **Service Bus**                      | A fully managed enterprise message broker with queues and publish-subscribe topics designed for reliable messaging.                                             |
| **Strong Consistency**               | The strictest Cosmos DB consistency level; reads are guaranteed to see the latest committed write but at the cost of higher latency.                            |
| **Throughput Unit (TU)**             | A pre-purchased unit of capacity used to control the ingress and egress limits of an Azure Event Hub.                                                           |
| **Trigger**                          | The specific event that causes an Azure Function to execute (e.g., an HTTP request, a message in a queue, or a timer).                                          |
| **WebJob**                           | A feature of Azure App Service that allows for the running of background tasks (scripts or programs) within the same context as a web app.                      |
![[Pasted image 20260306125500.png]]
In architecting cloud-native solutions, the choice between **Azure Event Grid**, **Azure Event Hubs**, and **Azure Service Bus** depends on whether you are managing **discrete events**, **data streams**, or **reliable messages**.

**Technical Trade-offs and Comparison**
![[Pasted image 20260306130533.png]]


