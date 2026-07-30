#azure #az104 
# Review Azure Container Instances

Containers are becoming the preferred way to package, deploy, and manage cloud applications. There are many options for teams to build and deploy cloud native and containerized applications on Azure. In this unit, we review Azure Container Instances (ACI).

Azure Container Instances offers the fastest and simplest way to run a container in Azure, without having to manage any virtual machines and without having to adopt a higher-level service. Azure Container Instances is a great solution for any scenario that can operate in isolated containers.

### Understand container images

All containers are created from container images. A container image is a lightweight, standalone, executable package of software that encapsulates everything needed to run an application. It includes the following components:

- **Code**: The application’s source code.
- **Runtime**: The environment required to execute the application.
- **System tools**: Utilities necessary for the application to function.
- **System libraries**: Shared libraries used by the application.
- **Settings**: Configuration parameters specific to the application.

When you create a container image, it becomes a portable unit that can run consistently across different computing environments. These images are the building blocks for containers, which are instances of these images running at runtime.

The following illustration shows a web server container built with Azure Container Instances. The container is running on a virtual machine in a virtual network.

![Diagram that shows a web server container running on a virtual machine in a virtual network.](https://learn.microsoft.com/en-us/training/wwl-azure/configure-azure-container-instances/media/container-overview-0e72c2ba.png)

### Things to know about Azure Container Instances

Let's review some of the [benefits of using Azure Container Instances](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-overview). As you review these points, think about how you can implement Container Instances for your internal applications.

- **Fast startup times**. Containers can start in seconds without the need to deploy and manage virtual machines.
    
- **Public IP connectivity and DNS names**. Containers can be directly exposed to the internet with an IP address and FQDN (fully qualified domain name).
    
- **Custom sizes**. You specify CPU cores (from 0.1 to 4 vCPU) and memory (from 0.1 to 16 GB) for each container at deployment time. Resource allocation is fixed for the lifetime of the container group.
    
- **Persistent storage**. Containers support direct mounting of Azure Files file shares.
    
- **Linux and Windows containers**. Container Instances can schedule both Windows and Linux containers. Specify the operating system type when you create your container groups.
    
- **Coscheduled groups**. Container Instances supports scheduling of multi-container groups that share host machine resources.
    
- **Virtual network deployment**. Linux container groups can be deployed into an Azure virtual network for private communication with other Azure resources. Virtual network deployed containers receive no public IP address and communicate only within the virtual network or peered networks.

# Implement container groups

The top-level resource in Azure Container Instances is the **container group**. A [container group](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-container-groups) is a collection of containers that get scheduled on the same host machine. The containers share a lifecycle, resources, local network, and storage volumes.

### Things to know about container groups

Let's review some of details about container groups for Azure Container Instances.

- A container group is similar to a pod in Kubernetes. A pod typically has a 1:1 mapping with a container, but a pod can contain multiple containers. The containers in a multi-container pod can share related resources.
    
- Azure Container Instances allocates resources to a multi-container group by adding together the resource requests of all containers in the group. Resources can include items such as CPUs, memory, and GPUs.
    
- There are three common ways to deploy a multi-container group.
    
    - **Azure Resource Manager template**. JSON-based infrastructure as code, ideal when deploying alongside other Azure resources.
        
    - **Bicep**. Microsoft's recommended infrastructure as code language, more concise than Azure Resource Manager templates. Bicep includes full IntelliSense support.
        
    - **YAML files**. Container-focused format, ideal for deployments that include only container instances.
        
- Container groups can share an external-facing IP address, one or more ports on the IP address, and a DNS label with an FQDN.
    
    - **External client access**. You must expose the port on the IP address and from the container to enable external clients to reach a container in your group.
        
    - **Port mapping**. Port mapping isn't supported because containers in a group share a port namespace.
        
    - **Deleted groups**. When a container group is deleted, its IP address and FQDN are released.
        

#### Configuration example

Consider the following example of a multi-container group with two containers.

![Diagram that depicts an Azure Container Instances multi-container group that has two containers.](https://learn.microsoft.com/en-us/training/wwl-azure/configure-azure-container-instances/media/container-groups-ea19ee6b.png)

The multi-container group has the following characteristics and configuration:

- The container group is scheduled on a single host machine, and is assigned a DNS name label.
- The container group exposes a single public IP address with one exposed port.
- One container in the group listens on port 80. The other container listens on port 1433.
- The group includes two Azure Files file shares as volume mounts. Each container in the group mounts one of the file shares locally.

### Things to consider when using container groups

Multi-container groups are useful when you want to divide a single functional task into a few container images. Different teams can deliver the images, and the images can have separate resource requirements.

Consider the following scenarios for working with multi-container groups. Think about what options can support your internal apps for the online retailer.

- **Consider web app updates**. Support updates to your web apps by implementing a multi-container group. One container in the group serves the web app and another container pulls the latest content from source control.
    
- **Consider log data collection**. Use a multi-container group to capture logging and metrics data about your app. Your application container outputs logs and metrics. A logging container collects the output data and writes the data to long-term storage.
    
- **Consider app monitoring**. Enable monitoring for your app with a multi-container group. A monitoring container periodically makes a request to your application container to ensure your app is running and responding correctly. The monitoring container raises an alert if it identifies possible issues with your app.
    
- **Consider front-end and back-end support**. Create a multi-container group to hold your front-end container and back-end container. The front-end container can serve a web app. The back-end container can run a service to retrieve data.

# Review Azure Container Apps

There are many options for teams to build and deploy cloud native and containerized applications on Azure. Let's understand which scenarios and use cases are best suited for Azure Container Apps and how it compares to other container options on Azure. Listen to a developer's view of Azure Container Instances.

### Things to know about Azure Container Apps

[Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview) is a serverless platform that allows you to maintain less infrastructure and save costs while running containerized applications. Instead of worrying about server configuration, container orchestration, and deployment details, Container Apps provides all the up-to-date server resources required to keep your applications stable and secure.

Common uses of Azure Container Apps include:

- Deploying API endpoints
- Hosting background processing jobs
- Handling event-driven processing
- Running microservices

Applications built on Azure Container Apps can dynamically scale based on the following characteristics:

- HTTP traffic
- Event-driven processing
- CPU or memory load
- Any KEDA-supported scaler

### Things to consider when using Azure Container Apps

Azure Container Apps enables you to build serverless microservices and jobs based on containers. Distinctive features of Container Apps include:

- Optimized for running general purpose containers, especially for applications that span many microservices deployed in containers.
- Powered by Kubernetes and open-source technologies like Dapr, KEDA, and envoy.
- Supports Kubernetes-style apps and microservices with features like service discovery and traffic splitting.
- Enables event-driven application architectures by supporting scale based on traffic and pulling from event sources like queues, including scale to zero.
- Supports running on demand, scheduled, and event-driven jobs.

Azure Container Apps doesn't provide direct access to the underlying Kubernetes APIs. If you would like to build Kubernetes-style applications and don't require direct access to all the native Kubernetes APIs and cluster management, Container Apps provides a fully managed experience based on best-practices. For these reasons, many teams prefer to start building container microservices with Azure Container Apps.

#### Compare container management solutions

Azure offers several container platforms for different scenarios. Azure Container Instances (ACI) is best for isolated, short-lived tasks. Azure Container Apps (ACA) serves serverless microservices. Azure Kubernetes Service (AKS) provides full Kubernetes control for complex orchestration needs.

|Feature|Azure Container Apps (ACA)|Azure Kubernetes Service (AKS)|
|---|---|---|
|Overview|ACA is a serverless container platform that simplifies the deployment and management of microservices-based applications by abstracting away the underlying infrastructure.|AKS simplifies deploying a managed Kubernetes cluster in Azure by offloading the operational overhead to Azure. It’s suitable for complex applications that require orchestration.|
|Deployment|ACA provides a PaaS experience with quick deployment and management capabilities.|AKS offers more control and customization options for Kubernetes environments, making it suitable for complex applications and microservices.|
|Management|ACA builds upon AKS and offers a simplified PaaS experience for running containers.|AKS provides a more granular control over the Kubernetes environment, suitable for teams with Kubernetes expertise.|
|Scalability|ACA supports both HTTP-based autoscaling and event-driven scaling, making it ideal for applications that need to respond quickly to changes in demand.|AKS offers horizontal pod autoscaling and cluster autoscaling, providing robust scalability options for containerized applications.|
|Use Cases|ACA is designed for microservices and serverless applications that benefit from rapid scaling and simplified management.|AKS is best for complex, long-running applications. These applications require full Kubernetes features and tight integration with other Azure services.|


