# 1
You have an Azure subscription that contains a virtual network named VNet1 and a virtual machine named VM1.

VM1 can only be accessed from the internal network.

An external contractor needs access to VM1. The solution must minimize administrative effort.

What should you configure?

Select only one answer.

a public IP address

**This answer is correct.**

a second private IP address

a Site-to-Site (S2S) VPN

Azure Firewall

To share a virtual machine with an external user, you must add a public IP address to the virtual machine. An additional IP address or firewall configuration will not help in this case. Configuring a S2S VPN does not have minimal administrative effort.

[Virtual networks and virtual machines in Azure | Microsoft Learn](https://learn.microsoft.com/azure/virtual-network/network-overview)

[Quickstart - Create a Windows VM in the Azure portal - Azure Virtual Machines | Microsoft Learn](https://learn.microsoft.com/azure/virtual-machines/windows/quick-create-portal)

# 2
You have an Azure subscription that contains the following virtual networks:

- VNet1 has an IP address range of 192.168.0.0/24.
- VNet2 has an IP address range of 10.10.0.0/24.
- VNet3 has an IP address range of 192.168.0.0/16.

You need configure virtual network peering.

Which two peerings can you create? Each correct answer presents complete solution.

Select all answers that apply.

VNet1 can be peered with VNet2.

**This answer is correct.**

VNet1 can be peered with VNet3.

VNet2 can be peered with VNet3.

**This answer is correct.**

VNet3 can be peered with VNet1.

VNet1 and VNet2 have non-overlapping IP addresses. For virtual network peering, both virtual networks must have non-overlapping IP addresses.

[Azure Virtual Network peering | Microsoft Learn](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview)

[Configure virtual network peering - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-vnet-peering/)

# 3
You have an Azure subscription that contains the following virtual networks:

- VNet1: Has an IP address space of 10.10.0.0/16 and contains a subnet named Subnet1 (10.10.1.0/24) that hosts a virtual machine named VM1 that runs Windows Server.
- VNet2: Has an IP address space of 10.20.0.0/16 and contains a subnet named Subnet2 (10.20.1.0/24) that hosts a virtual machine named VM2 that runs Windows Server.

VNet1 and VNet2 are connected by using virtual network peering.

Users report that VM1 cannot connect to VM2.

You need to verify whether the traffic from VM1 to the 10.20.0.0/16 subnet uses virtual network peering as the next hop.

What should you use?

Select only one answer.

Connection troubleshoot in Azure Network Watcher from VM1 to VM2

**This answer is incorrect.**

the effective routes for the network interface of VM1

**This answer is correct.**

Azure Network Watcher next hop for the network interface of VM1

the Network Controller role in VM1

**Objec**tive:**

4.1 Configure and manage virtual networks in Azure

**What This Item Tests:**

Create and configure virtual networks and subnets

**Additional Reading:**

[Constraints for peered virtual networks - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview#troubleshoot)

[Network troubleshooter - Training | Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/azure/app-service/troubleshoot-vnet-integration-apps#network-troubleshooter)

[Manage virtual networks - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/describe-microsoft-azure-resources-management/4-manage-virtual-networks)

**Rationale:**

Viewing the effective routes on the network interface of VM1 shows all the system, peering, and user-defined routes that Azure applies to outbound traffic, including the next hop type for the 10.20.0.0/16 prefix.

Connection troubleshoot validates reachability but does not display routing decisions.

Azure Network Watcher next hop is a diagnostic tool that identifies the next routing hop (type, IP address, and route table ID) for traffic leaving a virtual machine. Next hop does not display routing decisions.

The Network Controller role in Windows Server is a centralized, programmable management point for Software Defined Networking (SDN).**

# 4
You create several Azure virtual machines that run Windows Server.

You need to connect to the virtual machines without exposing RDP ports over the internet.

Which Azure service should you deploy?

Select only one answer.

Azure Bastion

**This answer is correct.**

Azure Front Door

Azure Network Watcher

Azure Virtual Desktop

Azure Bastion is a service that lets you connect to a virtual machine by using a browser, without exposing RDP and SSH ports. Azure Monitor helps you maximize the availability and performance of applications and services. Azure Network Watcher provides tools to monitor, diagnose, view metrics, and enable or disable logs for resources in an Azure virtual network. Remote Desktop is a feature of the operating system, which exposes the RDP port to connect to a server from the internet.

[About Azure Bastion | Microsoft Learn](https://learn.microsoft.com/azure/bastion/bastion-overview)

[Configure virtual networks - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-virtual-networks/)

# 5
Your company plans to migrate servers from on-premises to Azure. There will be dev, test, and production virtual machines on a single virtual network.

You need to restrict traffic between the dev, test, and production virtual machines to specific ports.

What should you use?

Select only one answer.

a network security group (NSG)

**This answer is correct.**

an Azure firewall

an Azure load balancer

an Azure virtual network

Must configure network security group (NSG) rules to allow TCP or ICMP traffic for specific ports. Azure Firewall is a managed service that protects your Azure services across multiple virtual networks. Load balancers are used to distribute incoming traffic to available backend servers. Azure VPN is used to have a connection establishment between on-premises and Azure.

[Azure network security groups overview | Microsoft Learn](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)

[Configure network security groups - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-network-security-groups/)

# 6
You have an Azure subscription that contains an ASP.NET application. The application is hosted on four Azure virtual machines that run Windows Server.

You have a load balancer named LB1 that load balances requests to the virtual machines.

You need to ensure that site users connect to the same web server for all requests made to the application.

Which two actions should you perform? Each correct answer presents part of the solution.

Select all answers that apply.

Configure an inbound NAT rule.

**This answer is incorrect.**

Set Session persistence to **Client IP**.

**This answer is correct.**

Set Session persistence to **None**.

Set Session persistence to **Protocol**.

**This answer is correct.**

By setting Session persistence to Client IP and Protocol, you ensure that site users connect to the same web server for all requests made to the application. Setting Session persistence to None disables sticky sessions and an inbound NAT rule is used to forward traffic from a load balancer frontend to a backend pool.

[Azure Load Balancer distribution modes | Microsoft Learn](https://learn.microsoft.com/azure/load-balancer/distribution-mode-concepts)

[Introduction to Azure Load Balancer](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-load-balancer/)

# 7
You have an Azure subscription that contains an Azure DNS zone named contoso.com.

You add a new subdomain named test.contoso.com.

You plan to delegate test.contoso.com to a different DNS server.

How should you configure the domain delegation?

Select only one answer.

Add an A record for test.contoso.com.

**This answer is incorrect.**

Add an NS record set named test to the contoso.com zone.

**This answer is correct.**

Create the SOA record for test.contoso.com.

Modify the A record for contoso.com.

You must create a DNS NS record set named test in the contoso.com zone. An NS zone must be created at the apex of the zone named contoso.com. You do not need to create the SOA record set in test.contoso.com. It must only be created in contoso.com. You do not need to create or modify the DNS A record.

[Delegate a subdomain - Azure DNS | Microsoft Learn](https://learn.microsoft.com/azure/dns/delegate-subdomain)

[Host your domain on Azure DNS - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/host-domain-azure-dns/)

# 8
You have an Azure subscription that contains four virtual machines. Each virtual machine is connected to a subnet on a different virtual network.

You install the DNS Server role on a virtual machine named VM1.

You configure each virtual network to use the IP address of VM1 as the DNS server.  

You need to ensure that all four virtual machines can resolve IP addresses by using VM1.

What should you do?

Select only one answer.

Configure a DNS server on all four virtual machines.

Configure network peering.

**This answer is correct.**

Create and associate a route table to all four subnets.

**This answer is incorrect.**

Create Site-to-Site (S2S) VPNs.

By default, Azure virtual machines can communicate only with other virtual machines that are connected to the same virtual network. If you want a virtual machine to communicate with other virtual machines that are connected to other virtual networks, you must configure network peering.

A route table controls how network traffic is routed. But without network peering, network traffic is still limited to single virtual network.

Configuring a Site-to-Site (S2S) VPN is incorrect because you are not connecting on-premises virtual machines to the cloud.

[Virtual Network service endpoints](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)

# 9
Your company has deployed an Azure Load Balancer to distribute traffic across multiple VMs in a web farm. Users report intermittent connection timeouts when accessing the web app.

You need to resolve the connection timeout issues and ensure even traffic distribution by the load balancer.

What should you do?

Select only one answer.

Change the distribution mode to five-tuple hash.

**This answer is correct.**

Configure a health probe for the load balancer.

**This answer is incorrect.**

Enable session persistence with source IP affinity.

Upgrade the load balancer to a higher SKU.

Changing the distribution mode to five-tuple hash ensures even traffic distribution by considering multiple parameters, which helps in resolving connection timeouts. Configuring a health probe for the load balancer does not impact internal traffic distribution or resolve connection timeouts. Enabling session persistence with source IP affinity can lead to uneven traffic distribution, directing requests from the same client to the same VM, which doesn't resolve the issue. Upgrading the load balancer to a higher SKU without addressing the distribution mode will not resolve the uneven traffic distribution or connection timeout issues.

[Improve application scalability and resiliency by using Azure Load Balancer](https://learn.microsoft.com/en-us/training/modules/improve-app-scalability-resiliency-with-load-balancer/)

# 10
An organization uses a Microsoft Azure Standard Load Balancer to distribute traffic across multiple virtual machines (VMs) in a backend pool. Users report intermittent connectivity issues with applications on these VMs.

You need to troubleshoot and resolve connectivity issues.

Which three actions should you perform? Each correct answer presents part of the solution.

Select all answers that apply.

Check the health probe configuration.

**This answer is correct.**

Ensure VMs respond to the configured port.

**This answer is correct.**

Increase the timeout setting.

Modify the session persistence setting.

**This answer is incorrect.**

Restart the VMs.

Verify NSG rules allow inbound traffic.

**This answer is correct.**

To troubleshoot and resolve connectivity issues with a Microsoft Azure Standard Load Balancer, it is essential to check the health probe configuration, ensure VMs respond to the configured port, and verify that NSG rules allow inbound traffic. These actions address potential misconfigurations that could prevent traffic from reaching VMs. Modifying the session persistence setting, increasing the timeout setting, or restarting the VMs do not directly resolve connectivity issues and may introduce new limitations or misconceptions.

[Secure storage endpoints | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/configure-storage-accounts/7-secure-storage-endpoints)  
[Create network security group rules | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/configure-network-security-groups/5-create-network-security-groups-rules)

# 11
You have an Azure subscription that contains a resource group named RG1. RG1 contains an Azure virtual machine named VM1.

You need to use VM1 as a template to create a new Azure virtual machine.

Which three methods can you use to complete the task? Each correct answer presents a complete solution.

Select all answers that apply.

From Azure Cloud Shell, run the `Get-AzVM` and `New-AzVM` cmdlets.

From Azure Cloud Shell, run the `Save-AzDeploymentScriptLog` and `New-AzResourceGroupDeployment` cmdlets.

From Azure Cloud Shell, run the `Save-AzDeploymentTemplate` and `New-AzResourceGroupDeployment` cmdlets.

**This answer is correct.**

From RG1, select **Export template**, select **Download**, and then, from Azure Cloud Shell, run the `New-AzResourceGroupDeployment` cmdlet.

**This answer is correct.**

From VM1, select **Export template**, and then select **Deploy**.

**This answer is correct.**

From RG1, selecting the Download option from the Export template page exports the Azure Resource Manager (ARM) template from the resource group properties. You can then deploy the ARM template by running the `New-AzResourceGroupDeployment` cmdlet.

By using the `Save-AzDeploymentTemplate` cmdlet, you can save the resource ARM template. You can then deploy the ARM template by running the `New-AzResourceGroupDeployment` cmdlet.

From VM1, selecting the Deploy option from the Export template page allows you to deploy a new Azure virtual machine and use the configuration of VM1 as the template.

The `Save-AzDeploymentScriptLog` cmdlet is used to save the log of a deployment script execution.

The `Get-AzVM` cmdlet generates a list of virtual machines that are created in the Azure subscription.

[Use Azure portal to export a template - Training | Microsoft Learn](https://learn.microsoft.com/azure/azure-resource-manager/templates/export-template-portal) 

[Export template in Azure PowerShell - Azure Resource Manager | Microsoft Learn](https://learn.microsoft.com/azure/azure-resource-manager/templates/export-template-powershell)

# 12
You have an Azure Resource Manager (ARM) template named deploy.json that is stored in an Azure Blob storage container.

You plan to deploy the template by running the `New-AzDeployment` cmdlet.

Which parameter should you use to reference the template?

Select only one answer.

`-Tag`

**This answer is incorrect.**

`-Templatefile`

`-TemplateSpecId`

`-TemplateUri`

**This answer is correct.**

The PowerShell deployment cmdlets can be used to deploy JSON templates that are stored locally in a resources group as a template spec, or from a web-based location. You can use the `-TemplateUri` parameter to specify a web-based location, such as GitHub or an Azure Blob Storage account. You can use `-Templatefile` to specify a local file. You can use `-TemplateSpecId` to specify a template that was save to Azure as a template spec.

[Deploy resources with PowerShell and template - Azure Resource Manager | Microsoft Learn](https://learn.microsoft.com/azure/azure-resource-manager/templates/deploy-powershell)

[Deploy Azure infrastructure by using JSON ARM templates - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/create-azure-resource-manager-template-vs-code/)

# 13
Your company has a set of resources deployed to an Azure subscription. The resources are deployed to a resource group named app-grp1 by using Azure Resource Manager (ARM) templates.

You need to verify the date and the time that the resources in app-grp1 were created.

Which blade should you review for app-grp1 in the Azure portal?

Select only one answer.

Deployments

**This answer is correct.**

Diagnostics setting

Deployment stacks

Policy

Navigating to the Diagnostics settings blade provides the ability to diagnose errors or review warnings. Navigating to the Metrics blade provides metrics information (CPU, resources) to users. On the Deployments blade for the resource group (app-grp1), all the details related to a deployment, such as the name, status, date last modified, and duration, are visible. Navigating to the Policy blade only provides information related to the policies enforced on the resource group.

[Azure AD deployment checklist - Microsoft Entra | Microsoft Learn](https://learn.microsoft.com/azure/active-directory/fundamentals/active-directory-deployment-checklist-p2)

# 14
You have an Azure Resource Manager (ARM) template named Template1 that is used to deploy Azure virtual machines.

Template1 contains the following text. 

"resources": [  
  {  
    "type": "Microsoft.Compute/virtualMachines",  
    "apiVersion": "2025-04-01",  
    "name": "[parameters('vmName')]",  
    "location": "[resourceGroup().location]",  
    "properties": {  
      &lt;text removed&gt;  
    }  
  }  
]

You need to deploy two Azure virtual machines by using Template1.

What should you add to Template1?

Select only one answer.

a copy element

**This answer is correct.**

the API version

the Azure subscription ID

the resource group location

The correct solution is to add a copy element, because ARM templates use the copy property to deploy multiple instances of a resource, such as two virtual machines, in a single deployment. The API version is already specified in the template and does not control the number of resources deployed. The subscription ID is never hardcoded in ARM templates since deployments are scoped to a subscription, and the resource group location is already provided through "[resourceGroup().location]". Therefore, only the copy element enables the template to create two virtual machines from a single resource definition.

[Add flexibility to your Azure Resource Manager template by using template functions](https://learn.microsoft.com/en-us/training/modules/modify-azure-resource-manager-template-reuse/2-azure-resource-manager-functions)  
[Examine Azure Resource Manager templates](https://learn.microsoft.com/en-us/training/modules/explore-azure-governance-manageability/3-examine-azure-resource-manager-templates)  
[Azure Resource Manager documentation](https://learn.microsoft.com/en-us/training/modules/arm-template-whatif/2-deployment-modes)

# 15
Your company plans to host an application on four Azure virtual machines.

You need to ensure that at least two virtual machines are available if a single Azure datacenter fails.

Which availability option should you select for the virtual machine?

Select only one answer.

an availability set

an availability zone

**This answer is correct.**

scale sets

To protect against datacenter level failures, and if you want connectivity to multiple machines, you must ensure that the virtual machines are deployed across various availability zones.

[What are Azure regions and availability zones? | Microsoft Learn](https://learn.microsoft.com/azure/reliability/availability-zones-overview)

[Configure virtual machine availability - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-virtual-machine-availability/)

# 16
You are deploying a virtual machine by using an availability set in the East US Azure region.

You have deployed 18 virtual machines in two fault domains and 10 update domains.

Microsoft performed planned physical hardware maintenance in the East US region.

What is the maximum number of virtual machines that will be unavailable?

Select only one answer.

2

**This answer is correct.**

8

9

**This answer is incorrect.**

18

18 virtual machines are shared across 10 update domains. The first 10 virtual machines go to 10 update domains, so eight update domains will have two virtual machines. When there is physical hardware maintenance, some virtual machines will be unavailable based on their configuration. If there was a rack failure, then 18 virtual machines will be distributed to two fault domains with nine virtual machines each.

[Availability sets overview - Azure Virtual Machines | Microsoft Learn](https://learn.microsoft.com/azure/virtual-machines/availability-set-overview)

[Configure virtual machine availability - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-virtual-machine-availability/)

# 17
You plan to deploy an Azure virtual machine.

You are evaluating whether to use an Azure Spot instance.

Which two factors can cause an Azure Spot instance to be evicted? Each correct answer presents a complete solution.

Select all answers that apply.

the average CPU usages of the instance

the Azure capacity needs

**This answer is correct.**

the current price of the instance

**This answer is correct.**

the time of day

Azure Spot instances allow you to provision virtual machines at a reduced cost, but these virtual machines can be stopped by Azure when Azure needs the capacity for other pay-as-you-go workloads, or when the price of the spot instance exceeds the maximum price that you have set. These virtual machines are good for dev, testing, or for workloads that do not require any specific SLA.

[Use Azure Spot Virtual Machines - Azure Virtual Machines | Microsoft Learn](https://learn.microsoft.com/azure/virtual-machines/spot-vms)

[Configure virtual machine availability - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-virtual-machine-availability/)
# 18
You have an Azure subscription that contains an Azure Storage account named vmstorageaccount1.  

You create an Azure container instance named container1.

You need to configure persistent storage for container1.

What should you create in vmstorageaccount1?

Select only one answer.

a blob container

a file share

**This answer is correct.**

a queue

a table

An Azure container instance (Docker container) can mount Azure File Storage shares as directories and use them as persistent storage. An Azure container instance cannot mount and use as persistent storage blob containers, queues and tables.

.

[Persistent Docker volumes with Azure File Storage | Azure Blog and Updates | Microsoft Azure](https://azure.microsoft.com/blog/persistent-docker-volumes-with-azure-file-storage/)

[Configure Azure Container Instances - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-azure-container-instances/)
# 19
Your development team plans to deploy an Azure container instance. The container needs a persistent storage layer.

Which service should you use?

Select only one answer.

Azure Blob storage

Azure Files

**This answer is correct.**

Azure Queue Storage

Azure SQL Database

You can persist data for Azure Container Instances with the use of Azure Files. Azure Files offers fully managed file shares hosted in Azure Storage that are accessible via the industry standard Server Message Block (SMB) protocol.

[Mount Azure Files volume to container group - Azure Container Instances | Microsoft Learn](https://learn.microsoft.com/azure/container-instances/container-instances-volume-azure-files)

[Explore Azure Storage services - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-storage-accounts/3-explore-azure-storage-services?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-storage)

# 20
You have an Azure subscription that contains an Azure container app named cont1.

You plan to add scaling rules to cont1.

You need to ensure that cont1 replicas are created based on received messages in Azure Service Bus.

Which scale trigger should you use?

Select only one answer.

CPU usage

event-driven

**This answer is correct.**

HTTP traffic

**This answer is incorrect.**

memory usage

Azure Container Apps allows a set of triggers to create new instances, called replicas. For Azure Service Bus, an event-driven trigger can be used to run the escalation method. The remaining scale triggers cannot use a scale rule based on messages in an Azure service bus.

[Scaling in Azure Container Apps | Microsoft Learn](https://learn.microsoft.com/azure/container-apps/scale-app#event-driven)

[Configure Azure Container Instances - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-azure-container-instances/)
# 21
You have an Azure subscription that contains an Azure App Service web app named App1.

You have the following diagnostic logging configurations:

- Application Logging (FileSystem): Error
- Application Logging (Blob): Information
- Detailed Error Message: Warning
- Web Server Logging: Verbose

You need to configure diagnostic logging to store all warnings or higher.  

Which types of diagnostic logging and severity should you enable?

Select all answers that apply.

Application Logging (Blob)

**This answer is correct.**

Application Logging (FileSystem)

**This answer is correct.**

Detailed Error Message

**This answer is incorrect.**

Verbose

Warning

**This answer is correct.**

You must enable the Application Logging (Blob) diagnostic, which can be stored for more than a week. You must also set the severity level to warning, to store warning, error, and critical log messages.

[Enable diagnostics logging - Azure App Service | Microsoft Learn](https://learn.microsoft.com/azure/app-service/troubleshoot-diagnostic-logs)

[Configure Azure App Service - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-azure-app-services/)

# 22
You have a Basic Azure App Service plan that contains a web app.

You need to ensure that the web app can scale automatically when the CPU usage is over 80% for a duration of 15 minutes.

Which two actions should you perform? Each correct answer presents part of the solution.

Select all answers that apply.

Configure a deployment slot.

Configure a scaling condition to scale based on a metric, and then add the rules.

**This answer is correct.**

Configure a scaling condition to scale based on an instance count, and then set the instance count.

Scale out the App Service plan.

**This answer is incorrect.**

Scale up the App Service plan.

**This answer is correct.**

The Basic app service plan does not support automatic scaling - you must scale up the plan to Premium (or higher) to support automatic scaling. After that you must configure a scaling condition, based on a metric (CPU), which will automatically trigger scaling (out) of the app service web app.

[Scale up features and capacities - Azure App Service | Microsoft Learn](https://learn.microsoft.com/azure/app-service/manage-scale-up)

[Configure Azure App Service - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-azure-app-services/)
# 23
You have an Azure subscription.

You plan to deploy a web app in a Linux-based Docker container.

You need to recommend a solution for the deployment of the web app that meets the following requirements:

- Supports a custom domain name
- Provides the ability to scale out automatically based on demand.
- Minimizes administrative effort
- Minimizes costs

Which solution should you recommend?

Select only one answer.

Azure App Service

**This answer is correct.**

Azure Container Instances

**This answer is incorrect.**

Azure Kubernetes Service (AKS)

Azure Virtual Machine Scale Sets

Azure App Service fulfills all the stated requirements. Azure Virtual Machine Scale Sets, Azure Kubernetes Service (AKS), and Azure Container Instances are more difficult to administer and more costly.

[Overview - Azure App Service | Microsoft Learn](https://learn.microsoft.com/azure/app-service/overview)

[Configure Azure App Service plans - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-app-service-plans/)
# 24
You plan to provision an Azure subscription that will contain the following virtual networks:

- VNet1 in the East US Azure region with two subnets
- VNet2 in the East US region with four subnets
- VNet3 in the West Europe Azure region with four subnets
- VNet4 in the West Europe region with two subnets

How many Azure Network Watcher instances will be provisioned as part of the deployment?

Select only one answer.

1

2

**This answer is correct.**

4

12

Azure Network Watcher is a regional service that allows you to monitor and diagnose conditions at a network scenario level in, to, and from Azure. When you create or update a virtual network in a subscription, Network Watcher will be enabled automatically in the virtual network's region. There is no impact on resources or associated charges for automatically enabling Network Watcher.

[Create an Azure Network Watcher instance | Microsoft Learn](https://learn.microsoft.com/azure/network-watcher/network-watcher-create)

[Introduction to Azure Network Watcher](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-network-watcher/)

# 25
You have a Log Analytics workspace that collects data from various data sources.

You create a new Azure Monitor log query.

You plan to view data pinned as a chart to a shared dashboard.

What is the maximum number of days for which data can be shown on the shared dashboard?

Select only one answer.

14

30

**This answer is correct.**

90

**This answer is incorrect.**

180

Data shown on a shared dashboard can only be displayed for a maximum of 30 days.

[Azure Monitor workbook chart visualizations - Azure Monitor | Microsoft Learn](https://learn.microsoft.com/azure/azure-monitor/visualize/workbooks-chart-visualizations)

[Introduction to Azure Monitor](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-monitor/)
# 26
You have 100 virtual machines deployed to Azure. You have Azure Monitor alerts configured for CPU and memory utilization for the virtual machines.

You open Azure Monitor alerts and discover 50 closed alerts for the virtual machines.

What can cause the alert state to be Closed?

Select only one answer.

An administrator manually changed the state of the alerts.

**This answer is correct.**

The alerts are older than 60 days.

**This answer is incorrect.**

The alert rule contains an action group that remediates the alert conditions.

The conditions that caused the alerts are no longer present.

The alert state is manually set by the user and does not have any automated logic behind it. The alert state can be either New, Acknowledged, or Closed.

[Manage Azure Monitor alerts - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-azure-alerts/2-manage-azure-monitor-alerts)

# 27
You have multiple Azure virtual machines and an Azure recovery services vault. Virtual machines are configured with the default backup policy.  

What is the retention period of virtual machine backups in the default backup policy?

Select only one answer.

7 days

14 days

30 days

**This answer is correct.**

90 days

By default, backups of virtual machines are kept for 30 days.

[Back up an Azure VM from the VM settings - Azure Backup | Microsoft Learn](https://learn.microsoft.com/azure/backup/backup-azure-vms-first-look-arm)

# 28
You have an Azure subscription that contains two virtual machines named VM1 and VM2.

VM1 and VM2 are backed up to a Recovery Service vault named Vault1 by using the same backup policy.

Your company plans to create additional virtual machines and Recovery Services vaults. During this process, Vault1 will be decommissioned.

You need to delete Vault1.

Which three actions should you perform before you can delete Vault1? Each correct answer presents part of the solution.

Select all answers that apply.

Delete VM1 and VM2.

Disable the soft delete feature and delete all data.

**This answer is correct.**

Enable a Read lock on Vault1.

Permanently remove any items in the soft delete state.

**This answer is correct.**

Stop the backup of VM1 and VM2.

**This answer is correct.**

You must stop the backups so that you can prepare to move to the new policy. The soft delete feature is enabled by default, so it must be disabled. You must remove all the items that are in the soft delete state. Deleting the virtual machines is not required. You cannot delete the policy without deleting the vault and backup, and a new policy is not required.

[Overview of Recovery Services vaults - Azure Backup | Microsoft Learn](https://learn.microsoft.com/azure/backup/backup-azure-recovery-services-vault-overview)

[Delete a Microsoft Azure Recovery Services vault - Azure Backup | Microsoft Learn](https://learn.microsoft.com/azure/backup/backup-azure-delete-vault?tabs=portal)

# 29
You have an Azure virtual machine named VM1 that is protected by using Azure site recovery.

You fail over VM1 from the primary region to the secondary region.

You need to reprotect VM1 after the failover so that VM1 will replicate back to the primary region.

What is the VM1 status before the reprotection?

Select only one answer.

Committing failover

Failover committed

**This answer is correct.**

Failover confirmed

Starting failover

Before you begin, you must ensure that the virtual machine status is Failover committed. This will ensure replication back to the primary region.

[Tutorial to fail over Azure VMs to a secondary region for disaster recovery with Azure Site Recovery. - Azure Site Recovery | Microsoft Learn](https://learn.microsoft.com/azure/site-recovery/azure-to-azure-tutorial-failover-failback)

[Configure file and folder backups - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-file-folder-backups/)

# 30
You have an Azure virtual machine that you back up by using Azure Backup.

The backup policy sub type is Standard, and the backup policy has the following configurations:

- Backup schedule frequency: Weekly
- Retain instant recovery snapshot(s) for: 5 days
- Retention of weekly backup point: On Sunday at 8:00 AM for 12 weeks

You discover that Instant Restore is consuming more storage than expected.

You need to reduce the amount of storage consumed by Instant Restore.

What should you do first?

Select only one answer.

Change the backup schedule frequency to Daily.

Change the retention of weekly backup points to 1 week.

Modify the backup policy to reduce the retention of instant recovery snapshots.

**This answer is correct.**

Provision an additional blob storage container.

Correct – The “Retain instant recovery snapshot(s)” setting directly determines how long snapshots are stored locally before being transferred to the Recovery Services vault. Reducing this from 5 days to 2 days lowers Instant Restore storage usage.

[Azure Instant Restore Capability - Azure Backup | Microsoft Learn](https://learn.microsoft.com/azure/backup/backup-instant-restore-capability)

[Configure file and folder backups - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-file-folder-backups/)
# 31
You have an Azure subscription that is linked to a Microsoft Entra tenant named contoso.com.

All users in contoso.com are currently able to invite external users to B2B collaboration.

You need to ensure that only members of the Guest Inviter, User Administrator, and Global Administrator roles can invite guest users.

What should you configure?

Select only one answer.

Access reviews

Conditional Access

**This answer is incorrect.**

Cross-tenant access settings

External collaboration settings

**This answer is correct.**

External collaboration settings let you specify which roles in your organization can invite external users for B2B collaboration. These settings also include options for allowing or blocking specific domains and options for restricting which external guest users can see in your Microsoft Entra directory.

Conditional Access allows you to apply rules to strengthen authentication and block access to resources from unknown locations.

Cross-tenant access settings are used to configure collaboration with a specific Microsoft Entra organization.

Access reviews are not used to control who can invite guest users.

[Enable B2B external collaboration settings - Microsoft Entra | Microsoft Learn](https://learn.microsoft.com/azure/active-directory/external-identities/external-collaboration-settings-configure)
# 32
Your Microsoft Entra tenant and on-premises Active Directory domain contain multiple users.

You need to configure self-service password reset (SSPR) functionality. The solution must minimize costs.

Which Microsoft Entra ID edition should you use?

Select only one answer.

Microsoft Entra ID Free

Microsoft Entra ID P1

**This answer is correct.**

Microsoft Entra ID P2

Only Microsoft Entra ID P1 and P2 support SSPR, but Microsoft Entra ID P1 is the lower cost option.

[Enable Azure Active Directory self-service password reset - Microsoft Entra | Microsoft Learn](https://learn.microsoft.com/azure/active-directory/authentication/tutorial-enable-sspr)

[What is self-service password reset in Azure Active Directory? - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/allow-users-reset-their-password/2-self-service-password-reset)
# 33
You have an Azure subscription that contains multiple users and administrators.  

You are creating a new custom role by using the following JSON.  

``

{   "Name": "Custom Role",   "Id": null,   "IsCustom": true,   "Description": "Custom Role description",   "Actions": [     "Microsoft.Compute/*/read",     “Microsoft.Compute/snapshots/write”,     “Microsoft.Compute/snapshots/read”,   ],   "NotActions": [   “Microsoft.Compute/snapshots/delete”   ],   "AssignableScopes": [     "/subscriptions/00000000-0000-0000-0000-000000000000",     "/subscriptions/11111111-1111-1111-1111-111111111111"   ] }

Which two actions can be performed by a user that is assigned the custom role? Each correct answer presents a complete solution.

Select all answers that apply.

Create and delete a snapshot.

Create and read a snapshot.

**This answer is correct.**

Create virtual machines.

Read all virtual machine settings.

**This answer is correct.**

The role can read all compute resources, call Microsoft support roles, and allow the creation and reading of a snapshot.

[Azure custom roles - Azure RBAC | Microsoft Learn](https://learn.microsoft.com/azure/role-based-access-control/custom-roles)

[Secure your Azure resources with Azure role-based access control (Azure RBAC)](https://learn.microsoft.com/training/modules/secure-azure-resources-with-rbac/)
# 34
You have an Azure subscription.

You run the following command:

```
  Get-AzRoleDefinition | Format-Table -Property Name, Id
```

The command output contains data that includes the following:

```
CustomRole1   111-222-333-444-555
Owner         8e3af657-a8ff-443c-a75c-2fe8c4bcb635
Contributor   b24988ac-6180-42a0-ab88-20f7382dd24c
Reader        acdd72a7-3385-48ef-bd42-f606fba81ae7
```

You have a script that manages access to resources at the resource group level. The assignment process is automated by running the following PowerShell script nightly.

```
$rg = "RG1"
$RoleName = "111-222-333-444-555"
$Role = Get-AzRoleDefinition -Name $RoleName
New-AzRoleAssignment -SignInName user1@contoso.com
    -RoleDefinitionName $Role.Name `
    -ResourceGroupName $rg
```

User1 is unable to access the RG1 resource group. You discover that the script fails to complete for User1.

You need to modify the script to ensure that it does not fail.

What should you change in the script?

Select only one answer.

`$Role = Add-AzRoleDefinition -Name $RoleName`

`$Role = Get-AzRoleAssignment -Name $RoleName`

`$Role = Set-AzRoleAssignment -Name $RoleName`

**This answer is incorrect.**

`$RoleName = "CustomRole1"`

**This answer is correct.**

For the script to work as written, the $RoleName variable should refer to the name instead of the ID.

[Assign Azure roles using Azure PowerShell - Azure RBAC | Microsoft Learn](https://learn.microsoft.com/azure/role-based-access-control/role-assignments-powershell)

[Secure your Azure resources with Azure role-based access control (Azure RBAC)](https://learn.microsoft.com/training/modules/secure-azure-resources-with-rbac/)
# 35
You have an Azure subscription that contains multiple virtual machines.  

You need to ensure that a user named User1 can view all the resources in a resource group named RG1. You must use the principle of least privilege.

Which role should you assign to User1?

Select only one answer.

Billing Reader

Contributor

Reader

**This answer is correct.**

Tag Contributor

The Reader role allows you to view all the resources but does not allow you to make any changes. The Contributor role allows you to manage all the resources, the Billing Reader role provides read access only to billing data, and the Tag Contributor role allows you to manage entity tags without providing access to the entities themselves.

[Azure built-in roles - Azure RBAC | Microsoft Learn](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles)

[Secure your Azure resources with Azure role-based access control (Azure RBAC)](https://learn.microsoft.com/training/modules/secure-azure-resources-with-rbac/)

# 36
You have an Azure subscription that contains several storage accounts.

You need to provide a user with the ability to perform the following tasks:

- Manage containers within the storage accounts.
- View storage account access keys.

The solution must use the principle of least privilege.

Which role should you assign to the user?

Select only one answer.

Owner

**This answer is incorrect.**

Reader

Storage Account Contributor

**This answer is correct.**

Storage Blob Data Contributor

Storage Account Contributor allows the management of storage accounts. It provides access to the account key, which can be used to access data via Shared Key authorization. Storage Blob Data Contributor grants permissions to read, write, and delete Azure Storage containers and blobs. Reader allows you to view all resources but does not allow you to make any changes. Owner grants full access to manage all resources, including the ability to assign roles in Azure RBAC.

[Azure built-in roles - Azure RBAC | Microsoft Learn](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles)

[Secure your Azure resources with Azure role-based access control (Azure RBAC)](https://learn.microsoft.com/training/modules/secure-azure-resources-with-rbac/)
# 37
You have an Azure subscription that contains a resource group named RG1. RG1 contains a virtual machine that runs daily reports.

You need to ensure that the virtual machine shuts down when resource group costs exceed 75 percent of the allocated budget.

Which two actions should you perform? Each correct answer presents part of the solution.

Select all answers that apply.

Create an action group of type Runbook, and then select **Scale Up VM**.

Create an action group of type Runbook, and then select **Stop VM** as an action.

**This answer is correct.**

From Cost Management + Billing, create a new cost analysis.

From Cost Management + Billing, modify the Budgets settings.

**This answer is correct.**

You must go to Cost Management + Billing, and then Budgets to edit the budget associated with the resource group resources. You must also create a new action group of the Runbook type, and then choose Stop VM as an action. The cost analysis will not stop the virtual machine from running and the Scale Up VM action group is not required.

[Tutorial - Create and manage Azure budgets - Microsoft Cost Management | Microsoft Learn](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
# 38
You have an Azure subscription that contains hundreds of virtual machines that were migrated from a local datacenter.

You need to identify which virtual machines are underutilized.

Which Azure Advisor settings should you use?

Select only one answer.

Cost

**This answer is correct.**

High Availability

Operational Excellence

Performance

**This answer is incorrect.**

The Cost blade allows you to optimize and reduce your overall Azure spending. You can use this to identify the virtual machines that are underutilized. The Performance blade allows you to improve the speed of your applications. High availability is unavailable via Azure Advisor. Operational Excellence helps you achieve process and workflow efficiency, resource manageability, and deployment best practices.

[Introduction to Azure Advisor - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/intro-to-azure-advisor/)

# 39
You have several management groups and Azure subscriptions.

You want to prevent the accidental deletion of resources.

To which three resource types can you apply delete locks? Each correct answer presents a complete solution.

Select all answers that apply.

management groups

**This answer is incorrect.**

resource groups

**This answer is correct.**

storage account data

subscriptions

**This answer is correct.**

virtual machines

**This answer is correct.**

You can use delete locks to block the deletion of virtual machines, subscriptions, and resource groups. You cannot use delete locks on management groups or storage account data.

[Protect your Azure resources with a lock - Azure Resource Manager | Microsoft Learn](https://learn.microsoft.com/azure/azure-resource-manager/management/lock-resources?tabs=json)
# 40
You have an Azure subscription that contains 25 virtual machines.

You need to ensure that each virtual machine is associated to a specific department for reporting purposes.

What should you use?

Select only one answer.

administrative units

management groups

storage accounts

tags

**This answer is correct.**

Tags are metadata elements that can be applied to Azure resources. Tags can be used for tracking resources such as virtual machines and associating each resource to a department for billing and reporting purposes.

Administrative units are containers used for delegating administrative roles to manage a specific portion of Microsoft Entra. Administrative units cannot contain Azure virtual machines.

Management groups are containers that can be used to manage access, policy, and compliance across multiple Azure subscriptions.

Azure Storage accounts contain Azure Storage data objects, including blobs, file shares, queues, tables, and disks. A storage account cannot contain virtual machines.

[Tag resources, resource groups, and subscriptions for logical organization - Azure Resource Manager | Microsoft Learn](https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources?tabs=json)

[Introduction to Azure virtual machines](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-virtual-machines/)
# 41
You have an Azure subscription.

You plan to create an Azure Policy definition named Policy1.

You need to include remediation information in Policy.

To which definition section should you add remediation information for Policy1?

Select only one answer.

metadata

**This answer is correct.**

mode

parameters

policyRule

You must use the RemediationDescription field in the metadata section from properties to specify a custom recommendation. The remaining options are Azure policies, but do not allow specific custom remediation information.

[Create custom Azure security policies in Microsoft Defender for Cloud | Microsoft Learn](https://learn.microsoft.com/azure/defender-for-cloud/custom-security-policies?pivots=azure-portal#enhance-your-custom-recommendations-with-detailed-information)

[Improve incident response with alerting on Azure - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/incident-response-with-alerting-on-azure/)
# 42
You have an Azure subscription that contains a storage account named storage1.

You need to provide a partner organization with access to storage1. Access to storage1 must automatically expire after 24 hours.

What should you configure?

Select only one answer.

a shared access signature (SAS)

**This answer is correct.**

an access key

Azure Content Delivery Network (CDN)

lifecycle management

A SAS provides secure delegated access to resources in a storage account. With a SAS, you have granular control over how a client can access data, including time restrictions.

Access keys and Azure CDN provide permanent access to resources. They will require manual steps to remove access. Lifecycle management is not needed.

[Configure Azure Storage security - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-storage-security/)

[Grant limited access to data with shared access signatures (SAS) - Azure Storage | Microsoft Learn](https://learn.microsoft.com/azure/storage/common/storage-sas-overview)
# 43
You have an Azure subscription that contains a storage account named storage1.

You need to ensure that access to storage1 is prevented from the internet.

What should you configure on storage1?

Select only one answer.

Access keys

Data protection

**This answer is incorrect.**

Encryption

Networking

**This answer is correct.**

The Networking node of a storage account provides settings to configure public network access and network routing. To disable public network access, you can disable public network access, or configure the access to only allow specific virtual networks and IP addresses.

[Configure Azure Storage security - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-storage-security/)

[Configure Azure Storage firewalls and virtual networks | Microsoft Learn](https://learn.microsoft.com/azure/storage/common/storage-network-security?tabs=azure-portal)
# 44
You have an Azure subscription that contains a storage account named storage1.

You need to grant a third-party application access to storage1 for the next 30 days.

What should you use?

Select only one answer.

a conditional access policy

a shared access signature

**This answer is correct.**

an access key

an Azure role

The correct solution is to use a shared access signature (SAS), because only SAS can specify time limited access to Azure storage. An Access key provides unlimited access to Azure storage account, an Azure role can provide access and/or management of Azure resource, which is not time limited and a conditional access policy acts as a zero-trust, "if-then" policy engine that evaluates signals like user identity, device compliance, location, and risk to make real-time access decisions.

[Discover shared access signatures](https://learn.microsoft.com/en-us/training/modules/implement-shared-access-signatures/2-shared-access-signatures-overview)  
[Understand shared access signatures](https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/4-shared-access-signatures)

# 45
You have an Azure subscription that contains a storage account named storage1. storage1 contains an Azure Files share named share1.

You need to ensure that users can authenticate to share1 by using Microsoft Entra and access the file share by using SMB.

What should you do?

Select only one answer.

Configure identity-based access.

**This answer is correct.**

Generate a shared access signature (SAS) and a connection string.

Enable public network access.

Regenerate the access keys.

**Objective:**

2.1 Configure access to storage

**What This Item Tests:**

Configure identity-based access for Azure Files

**Additional Reading:**

[Review Azure Storage security strategies - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/configure-storage-security/2-review-strategies)

Correct - Identity-based access for an Azure Storage account is a security model that uses Microsoft Entra ID or Active Directory to authorize requests to storage data, rather than relying on a static storage account key or SAS.  
Incorrect – SAS tokens and access keys provide key-based access, rather than identity-based access, and enabling public network access does not configure authentication or authorization.
# 46
You have an Azure Storage account named corpimages and an on-premises shared folder named \server1\images.

You need to migrate all the contents from \server1\images to corpimages.

Which two commands can you use? Each correct answer presents a complete solution.

Select all answers that apply.

`Azcopy copy \\server1\images https://corpimages.blob.core.windows.net/public -recursive`

**This answer is correct.**

`Azcopy sync \\server1\images https://corpimages.blob.core.windows.net/public -recursive`

**This answer is incorrect.**

`Get-ChildItem -Path \\server1\images -Recurse | Set-AzStorageBlobContent -Container "corpimages"`

**This answer is correct.**

`Set-AzStorageBlobContent -Container "ContosoUpload" -File "\\server1\images" -Blob "corporateimages "`

The AzCopy command allows you to copy all files to a storage account. You then use `Get-ChildItem` with the `path` parameter, recurse to select everything, and then use the `Set-AzureStorageBlobContent` cmdlet.

[Copy or move data to Azure Storage by using AzCopy v10 | Microsoft Learn](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10#transfer-data)

[Set-AzureStorageBlobContent (Azure.Storage) | Microsoft Learn](https://learn.microsoft.com/powershell/module/azure.storage/set-azurestorageblobcontent?view=azurermps-6.13.0)

[Upload, download, and manage data with Azure Storage Explorer - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/upload-download-and-manage-data-with-azure-storage-explorer/)
# 47
You have an Azure Storage account.

You need to copy data to the storage account by using the AzCopy tool.

Which two types of data storage are supported by AzCopy? Each correct answer presents a complete solution.

Select all answers that apply.

blob

**This answer is correct.**

file

**This answer is correct.**

queue

table

You can provide authorization credentials by using Microsoft Entra, or by using a shared access signature (SAS) token. Both storage types, blob and file, are supported in AzCopy.

[Copy or move data to Azure Storage by using AzCopy v10 | Microsoft Learn](https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-v10)

[Upload, download, and manage data with Azure Storage Explorer - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/upload-download-and-manage-data-with-azure-storage-explorer/)
# 48
A company is using Azure Blob Storage to store large amounts of unstructured data that is accessed infrequently but requires fast retrieval when needed.  

You need to minimize storage costs while ensuring data retrieval performance is not compromised.    

What should you do?

Select only one answer.

Configure the access tier of the Azure Blob Storage account to Cold.

**This answer is correct.**

Configure the access tier of the Azure Blob Storage account to Hot.

Enable Azure Storage account object replication.

Configure the access tier of the Azure Blob Storage account to Cool.

**This answer is incorrect.**

The Cold access tier is cost-effective for storing large amounts of data that is infrequently accessed. The Hot access tier is more expensive and is optimized for data that is accessed frequently. Object replication is not related to cost optimization but rather to data availability and redundancy. 

[Storage account overview - Training | Microsoft Learn](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview)  
[Connect Azure Storage Explorer to a storage account - Training | Microsoft Learn](https://learn.microsoft.com/en-us/training/modules/upload-download-and-manage-data-with-azure-storage-explorer/2-connect-storage-account)
# 49
You have an Azure Storage account named storageaccount1 with a blob container named container1 that stores confidential information.

You need to ensure that content in container1 is not modified or deleted for six months after the last modification date.

What should you configure?

Select only one answer.

a custom Azure role

lifecycle management

**This answer is incorrect.**

the change feed

the immutability policy

**This answer is correct.**

A timed-based retention policy or legal hold policies can be applied to block deletion. Immutability policies can be scoped to a blob version or to a container.

[Overview of immutable storage for blob data - Azure Storage | Microsoft Learn](https://learn.microsoft.com/azure/storage/blobs/immutable-storage-overview?tabs=azure-portal)

[Configure Azure Blob Storage - Training | Microsoft Learn](https://learn.microsoft.com/training/modules/configure-blob-storage/)
# 50
You have an Azure subscription that contains a storage account.

You need to recommend a storage solution for storing infrequently accessed data. The solution must meet the following requirements:

- The data must be stored for at least 90 days.
- The data must be available within seconds.
- Storage costs must be minimized.

Which tier should you recommend?

Select only one answer.

Cold

**This answer is correct.**

Cool

Hot

Premium

The correct solution is the Cold tier, because it is an online storage tier in Azure designed for infrequently accessed data that must remain available within seconds. The Cold tier has a recommended minimum retention period of 90 days, aligning directly with the scenario, and offers lower storage costs than Hot or Cool tiers while still supporting immediate access. The Cool tier requires only 30 days of retention and has higher costs than Cold for long-term storage, the Hot tier is optimized for frequently accessed data at higher storage prices, and the Premium tier is intended for high-performance workloads, not for cost efficiency. Therefore, Cold best satisfies the requirements for cost savings, online availability, and the 90-day storage requirement.

[Explore Azure Blob storage](https://learn.microsoft.com/en-us/training/modules/explore-azure-blob-storage/2-blob-storage-overview)  
[Assign blob access tiers](https://learn.microsoft.com/en-us/training/modules/configure-blob-storage/4-create-blob-access-tiers)


# 51
Which of the following Azure Application Gateway features can protect web applications against SQL injection attacks?

Health probes

TLS/SSL termination

Web application firewall

Correct

# 52. 

You have a back-end pool made up of four Azure infrastructure as a service (IaaS) virtual machines. Occasionally, one or more of these virtual machines might become temporarily unresponsive. You want to ensure that Application Gateway doesn't forward traffic to an unresponsive virtual machine, even if you're unaware that a problem exists. Which Application Gateway feature can prevent traffic from forwarding to an unresponsive virtual machine?

Health probes

Correct

Web application firewall

Connection draining

# 53. 

You have a back-end pool made up of eight Azure IaaS virtual machines. You need to install a new framework on each of these virtual machines. You don't want the virtual machine to participate in the back-end pool while you do this maintenance operation. You want to stop new connections from occurring on the virtual machine that you're doing maintenance on. You also want to allow any existing connections that are present to complete naturally. Which of the following Azure Application Gateway features can you use to accomplish this goal?

Session affinity

Connection draining

Correct

Health probes





1. 

You're in the process of trying to ascertain which resources are connected to a specific virtual network that's being used as a Dev/Test environment for experimental Adatum workloads. Which of the following Network Watcher tools would you use to accomplish this goal?

Topology

Correct

Connection monitor

VPN troubleshoot

2. 

Which of the following Network Watcher tools allows you to detect whether changes in NSG rules affect connectivity between IaaS VMs on a virtual network in Adatum's Azure subscription?

Topology

Connection monitor

Correct

VPN troubleshoot

3. 

Which of the following Network Watcher tools allows you to detect if your on-premises devices can't communicate with your Azure virtual machine over the new VPN connection that you created?

Topology

Connection Monitor

VPN troubleshoot

Correct

[Understand MS Entra ID Module assessment](https://learn.microsoft.com/en-us/training/modules/understand-azure-active-directory/7-knowledge-check/?ns-enrollment-type=learningpath&ns-enrollment-id=learn.az-104-manage-identities-governance)
https://learn.microsoft.com/en-us/training/modules/sovereignty-policy-initiatives/check



1. 

What is a role definition in Azure?

A collection of permissions with a name that is assignable to a user, group, or application.

A role definition in Azure is a collection of permissions with a name that you can assign to a user, group, or application.

The collection of users, groups, or applications that have permissions to a role.

The binding of a role to a security principal at a specific scope to grant access.

2. 

Suppose an administrator wants to assign a role to allow a user to create and manage Azure resources but not be able to grant access to others. Which of the following built-in roles would support this?

Owner

Contributor

A contributor can create and manage all types of Azure resources, but they can't grant access to other users.

Reader

User Access Administrator

3. 

What is the inheritance order for scope in Azure?

Management group, Resource group, Subscription, Resource

Management group, Subscription, Resource group, Resource

The inheritance order for scope is Management group, Subscription, Resource group, Resource. For example, if you assigned a Contributor role to a group at the Subscription scope level, it'll be inherited by all Resource groups and Resources.

Subscription, Management group, Resource group, Resource

Subscription, Resource group, Management group, Resource


1. 

Suppose a team member can't view resources in a resource group. Where would the administrator go to check the team member's access?

Check the team member's permissions by going to their **Azure profile > My permissions**.

Go to the resource group and select **Access control (IAM)** > **Check Access**.

Correct

Go to one of the resources in the resource group and select **Role assignments**.

2. 

Suppose an administrator in another department needs access to a virtual machine managed by your department. What's the best way to grant them access to just that resource?

At the resource scope, create a role for them with the appropriate access.

At the resource group scope, assign the role with the appropriate access.

At the resource scope, assign the role with the appropriate access.

Correct

3. 

Suppose a developer needs full access to a resource group. If you are following least-privilege best practices, what scope should you specify?

Resource

Resource group

Correct

Subscription

4. 

Suppose an administrator needs to generate a report of the role assignments for the last week. Where in the Azure portal would they generate that report?

Search for **Activity log** and filter on the **Create role assignment (roleAssignments)** operation.

Correct

At the appropriate scope, go to **Access control (IAM)** > **Download role assignments**.

At the appropriate scope, go to **Access control (IAM)** > **Role assignments**.

1. 

When is a user considered registered for SSPR?

They registered at least one of the permitted authentication methods.

They registered at least the number of methods that you've required to reset a password.

A user is considered registered for SSPR when they've registered at least the number of methods that you've required to reset a password. You can set this number in the Azure portal.

They set up the minimum number of security questions.

2. 

When you enable SSPR for your Microsoft Entra organization...

Users can only change their password when they're signed in.

Admins can reset their password by using one authentication method.

Users can reset their passwords when they can't sign in.

If the user passes the authentication tests, then they can reset their password.



1.

What is a key disadvantage of vertical scaling when compared to horizontal scaling in cloud environments?

 

It is more flexible in handling variable workloads

It requires downtime to resize the virtual machine

Correct

It allows for more instances to be added easily

2.

Which scaling strategy should be adopted for a microservices architecture to ensure each service can scale independently based on demand?

 

Using a single, large monolithic application

Horizontal scaling by deploying each microservice in separate containers or VMs

Correct

Vertical scaling by increasing the size of the VM hosting all services

3.

Your organization is deploying a critical application that requires high availability. Which Azure feature should you use to ensure your application's virtual machines are distributed across multiple datacenters, providing protection against datacenter failures?

 

Availability Sets

Incorrect

Availability Zones

Update Domains

4.

What is a key advantage of using Azure Virtual Machine Scale Sets for managing application demand fluctuations?

 

Automatic adjustment of virtual machine count as demand changes.

Correct

Manual scaling of virtual machines based on user input.

Fixed pricing regardless of usage.

5.

Your company plans to deploy a global application that experiences varying traffic patterns. Which Azure solution should be used to automatically adjust the number of running instances based on current demand?

 

Azure Traffic Manager

Azure Blob Storage

Azure Virtual Machine Scale Sets

Correct

6.

If your application experiences a consistent decrease in demand during weekends, how can you optimize the cost using Azure Virtual Machine Scale Sets?

 

Disable autoscaling during weekends.

Increase the number of instances during weekends.

Configure autoscale rules to decrease instances during weekends.

Correct

7.

A seasonal e-commerce platform expects a surge in traffic during the holiday season. Which scaling approach would provide cost-effective management of resources while maintaining performance?

 

Horizontal scaling with autoscaling to dynamically adjust resources

Correct

Vertical scaling with scheduled upgrades to larger VMs

Maintaining a constant high number of VMs throughout the year

8.

When configuring an Azure Virtual Machine Scale Set, why is it important to understand the distinction between fault domains and update domains?

 

To guarantee zero downtime for all virtual machines.

To ensure that virtual machines are not affected by regional outages.

To minimize the simultaneous impact of maintenance and hardware failures.

Correct

9.

Which statement accurately describes the role of fault domains in Azure's availability set configuration?

 

Fault domains ensure VMs are distributed across different physical racks to avoid single points of failure.

Correct

Fault domains manage sequential updates to virtual machines during planned maintenance.

Fault domains provide automatic load balancing across VMs within a datacenter.


1. 

What scaling option provides more CPU, memory, or disk space without adding more virtual machines?

Scale up

Correct

Scale out

Scale back

2. 

Which App Service Plan supports the Production team's 10 staging slots requirement?

Basic B1

Standard S1

Premium V3 P1V3

Correct

3. 

Triggering an event at 8:00 AM on Saturday is an example of what type of rule?

A metric-based rule.

A time-based rule.

Correct

An app-insight rule.

1. 

When you clone a configuration from another deployment slot, which configuration setting follows the content across the swap?

Custom domain names

Connection strings

Correct

Scale settings

2. 

How can you support the Marketing team requests about research web page usage?

Continuous deployment

Application logging

Azure Application Insights

Correct

3. 

Which option is a valid automated deployment source?

GitHub

Correct

JavaScript code

SharePoint

1.

Which deployment method is used for deploying multiple containers in Azure Container Instances?

 

Using Windows Admin Center for individual containers.

Using Hyper-V Manager for individual containers.

Using an orchestrator such as Azure Kubernetes Service.

Correct

2.

Which component is essential to include in a Docker image for it to run successfully in Azure Container Instances?

 

A runtime environment for the application.

Correct

An Azure Resource Manager template.

A detailed Kubernetes configuration file.

3.

In Azure Container Groups, how are resources allocated to a multi-container setup?

 

Resources are evenly distributed among all containers in the group.

Resources are allocated based on the largest container's requirements.

Resources are allocated based on the combined requests of all containers in the group.

Correct

4.

Which advantage of containers over virtual machines can lead to better resource utilization?

 

Containers use fewer system resources by running only the necessary user-mode components.

Correct

Containers require more CPU and memory to operate effectively.

Containers provide a stronger security boundary than virtual machines.

5.

Your company requires a solution that ensures strong isolation between applications for security purposes. Which technology should be chosen?

 

Azure Container Instances

Azure Container Apps

Virtual Machines

Correct

6.

Your organization wants to deploy containers that can be accessed directly over the internet using a specified domain name. Which feature of Azure Container Instances enables this capability?

 

Virtual network deployment.

Coscheduled groups.

Public IP connectivity and DNS names.

Correct

7.

You have deployed an Azure Container Instance with a Docker image, but the application is not accessible. What could be a possible reason?

 

The container runtime is not compatible with Azure Container Instances.

The DNS configuration for the container instance is incorrect.

Correct

The container instance is not linked to an Azure Virtual Network.

8.

Which of the following is a unique characteristic of Azure Container Instances compared to other Azure services?

 

Provides direct access to Kubernetes APIs

Fast startup times without managing virtual machines

Correct

Requires adoption of a higher-level service for deployment

9.

Your organization is considering using Azure Container Instances for deploying its applications. What is one major advantage of using containers over virtual machines in terms of operating system requirements?

 

Containers require a full operating system installation, similar to virtual machines.

Containers run the user mode portion of an operating system, which uses fewer system resources.

Correct

Containers use more system resources than virtual machines because they run multiple applications within the same instance of an operating system.

1.

Why is it important to verify the domain ownership when configuring a custom domain for Azure Blob Storage?

 

To improve the performance of data access.

To allow access from the Azure portal.

To ensure that the domain can be legally mapped to the storage account.

Correct

2.

Your company requires a storage solution that maintains high availability even if an entire Azure region becomes unavailable. Which replication strategy should you choose to ensure that your data remains accessible in such a scenario?

 

Locally redundant storage (LRS)

Read-access geo-zone-redundant storage (RA-GZRS)

Correct

Zone-redundant storage (ZRS)

3.

What is the difference between Azure Service Endpoints and Private Endpoints in terms of security configuration for Azure Storage?

 

Service Endpoints are used for data replication, while Private Endpoints are used for data encryption.

Service Endpoints allow traffic over the public internet, while Private Endpoints keep traffic within the Microsoft backbone network.

Correct

Service Endpoints assign a public IP to Azure Storage, while Private Endpoints assign a private IP.

4.

After setting up a custom domain for Azure Blob Storage, access attempts fail. Which configuration should you double-check to resolve the issue?

 

Verify that the storage account is set to a premium tier.

Check if the storage account is in the same region as the custom domain's registrar.

Ensure the CNAME record correctly points to the storage account.

Correct

5.

Which security feature of Azure Storage assigns a private IP address from your VNet to the storage account, ensuring network isolation?

 

Service Endpoints

NSG Rules

Private Endpoints

Correct

6.

When comparing Azure's Locally Redundant Storage (LRS) and Geo-Redundant Storage (GRS), what is the main advantage of choosing GRS?

 

Data is synchronously replicated across multiple zones within a region.

Data is replicated to a secondary geographic region to protect against regional outages.

Correct

Data is replicated three times within a single data center for cost savings.

7.

For an application that requires both regional disaster recovery and the ability to access data in multiple regions without latency, which Azure replication strategy should be selected?

 

Zone-redundant storage (ZRS)

Locally redundant storage (LRS)

Read-access geo-redundant storage (RA-GRS)

Correct

8.

Your company requires all storage account data to be accessible only through a specific private IP range within the Azure environment. Which feature should be implemented to meet this requirement?

 

Implement Azure Private Endpoints.

Correct

Use Azure Firewall to block all public access.

Configure Azure Virtual Network Service Endpoints.

9.

When configuring a custom domain for your Azure storage account, which Azure portal setting must you verify to ensure the domain maps correctly?

 

Storage account location

Virtual network settings

Custom domain setting under the blob service configuration

Correct


1.

What is a significant advantage of using object replication over simple data backups in Azure Blob Storage?

 

Object replication provides continuous data availability and regional failover capabilities.

Object replication automatically compresses data to save storage space.

Object replication allows for automatic data tier transitions based on usage patterns.

Incorrect

2.

Which use case best illustrates the benefit of using Azure Blob Storage for a media company?

 

Maintaining a secure repository for sensitive customer data.

Storing and streaming high-definition video content to customers worldwide.

Correct

Hosting a relational database for transaction processing.

3.

Which Azure Blob Storage access tier is most cost-effective for data that is rarely accessed and must be retained for compliance purposes?

 

Cool tier

Hot tier

Archive tier

Correct

4.

Which component is essential for managing the lifecycle of blobs that require versioning and deletion of previous versions?

 

Blob versioning

Correct

Blob snapshots

Container access level settings

5.

How does Azure Blob Storage object replication differ from geo-replication?

 

Object replication incurs higher data transfer costs compared to geo-replication.

Object replication allows configuration of specific containers for replication, whereas geo-replication replicates all data automatically.

Correct

Object replication supports replication to multiple regions simultaneously, unlike geo-replication.

6.

Your company wants to minimize storage costs for legal compliance data that is rarely accessed but must be retained for several years. Which Azure Blob Storage tier should you choose?

 

Cool tier

Archive tier

Correct

Hot tier

7.

A company observes that their data retrieval costs have increased significantly. They currently use the Hot tier for data that is read infrequently. What should they do to optimize costs while maintaining accessibility?

 

Switch to the Cool tier

Correct

Switch to the Cold tier

Switch to the Archive tier

8.

What distinguishes object replication in Azure Blob Storage from simple data backups?

 

Object replication supports automatic data tier transitions, unlike backups.

Incorrect

Object replication incurs no data transfer costs, unlike backups.

Object replication provides regional redundancy, whereas backups typically do not.

9.

Which Azure Blob Storage access tier is designed for data that can remain offline and tolerate retrieval latencies of several hours?

 

Cool tier

Hot tier

Archive tier

Correct


1. 

What is the recommended way to manage and rotate your Azure storage account access keys?

Use Azure Key Vault to manage and rotate your keys.

Correct

Save access keys in plain text accessible to others.

Hard code access keys in your application code.

2. 

What is the recommended way to authorize access to data in Azure Storage?

Using either Microsoft Entra ID or a shared access signature SAS.

Correct

Using Shared Key authorization.

Using access keys and connection strings for all apps accessing production or sensitive data.

3. 

You want to give read access to image assets for a limited period of time. What security option would be the best option to use?

Storage account keys

Encryption in transit

Shared Access Signature

Correct


