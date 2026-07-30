# Azure Monitor: 

helps you collect, analyze, and alert on various types of host and client monitoring data from your Azure VMs.

- Azure Monitor provides a set of VM host logs and performance and usage metrics for all Azure VMs.
- You can enable recommended alert rules when you create VMs or afterwards to alert on important VM host metrics.
- Azure Monitor Metrics Explorer lets you graph and analyze metrics for Azure VMs and other resources.
- VM insights provides a simple way to monitor important VM client performance counters and processes running on your VM.
- You can create data collection rules to collect other metrics and logs from your VM client.
- You can use Log Analytics to query and analyze log data.

# Backups Summary

In this module, you learned the importance of having a tested backup and recovery strategy for your organization. You learned about the different types of Azure backups, and the reasons why you would choose one backup type versus another depending on your scenario.

You learned that you can back up Azure virtual machines or on-premises machines. In addition, you learned how to back up an Azure virtual machine (VM). You then restored it by using the various options available to you, and you were able to monitor the progress.

You can now use Azure Backup to help protect your environment against data loss or disk corruption. You can restore services according to your business continuity and disaster recovery plan.

 Important

In this module you created resources using your Azure subscription. You want to clean up these resources so that you will not continue to be charged for them. You can delete resources individually or delete the resource group to delete the entire set of resources.

## Learn more

For more information about Azure Backup, see the following articles:

- [Latest Azure Backup pricing and availability](https://azure.microsoft.com/pricing/details/backup)
- [Documentation for the Azure Backup service](https://learn.microsoft.com/en-us/azure/backup)
- [Support matrix for Azure VM backup](https://learn.microsoft.com/en-us/azure/backup/backup-support-matrix-iaas)
- [Security features in Azure Backup](https://learn.microsoft.com/en-us/azure/backup/security-overview)
- [Built-in monitoring and alerting capabilities](https://learn.microsoft.com/en-us/azure/backup/backup-azure-monitoring-built-in-monitor)
- [Azure Files - Snapshot management by Azure Backup](https://learn.microsoft.com/en-us/azure/backup/backup-afs)
- [Back up SQL Server databases running on Azure VMs](https://learn.microsoft.com/en-us/azure/backup/backup-azure-sql-database)
- [Backup SAP HANA (High-performance Analytic Appliance) databases running on Azure VMs](https://learn.microsoft.com/en-us/azure/backup/backup-azure-sap-hana-database)
- [Azure Data Protection Manager (DPM)](https://learn.microsoft.com/en-us/azure/backup/backup-azure-dpm-introduction) and [Azure Backup Server (MABS)](https://learn.microsoft.com/en-us/azure/backup/backup-mabs-protection-matrix)

Access Management summary
When you create a resource, you want to know that only specific access is granted to users and groups. In this module you learned the different methods to assign and control access to Azure resources.

During this module you have learned to:

- Assign Azure roles and custom roles to access Azure resources.
- Create and manage application access with managed identities.
- Configure and manage access into Azure Key Vault.
- Retrieve object from a key vault securely.
- Explore the capabilities of Microsoft Entra Permissions Management.

## To learn more, research using these links

- [Assign Azure roles using the Azure portal - Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps)
- [Create or update Azure custom roles using the Azure portal - Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles)
- [Configure managed identities using the Azure portal - Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/)
- [Assign a managed identity access to a resource using the Azure portal - Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-assign-access-azure-resource?pivots=identity-mi-access-cli)
- [Understand Azure role definitions - Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions)
- [Grant permission to applications to access an Azure key vault using Azure RBAC](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy)
- [Create and access a secret in Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal)
-# Summary
Our goal was to help you evaluate whether Azure Backup would offer the features and capabilities you need to help you protect your data. During the module, we explored how Azure Backup might address:

- Ensuring availability of your data.
- Protecting your Azure workloads.
- Securing your data.

We applied the criteria to a scenario where your company was hosting an application that used a SQL Server database instance running on multiple Azure VMs. We noted how Azure Backup could provide data protection by backing up our Azure VMs or the files, folders, and system state on those VMs.

We also saw how Azure Backup helps with compliance by offering retention options for the data and security with encryption and RBAC. Using Backup center, we showed how easy it is to manage these backups.

Backup center simplifies data protection management at-scale by allowing you to discover, govern, monitor, operate, and optimize backup management, all from one unified console. This helps you to drive operational efficiency with Azure. Your backups are automatically secured against ransomware, malicious admins, and accidental deletions.

## References

- [Azure Backup website](https://azure.microsoft.com/products/backup/)
- [Azure Backup compliance standards](https://learn.microsoft.com/en-us/azure/backup/compliance-offerings)

# Azure Files Summary and resources

Azure Administrators are familiar with Azure Files and the Azure File Sync agent. They know how to implement fully managed file shares in the cloud by using industry standard protocols. They understand how to use Azure File Sync to cache Azure Files shares on an on-premises Windows Server or cloud virtual machine.

In this module, you learned when to use Azure Files and how the service compares to Azure Blob Storage. You also reviewed Azure Files features such as snapshots and soft delete. You learned how Azure File Sync can be used with on-premises data stores. You also were introduced to Azure Storage Explorer.

**The main takeaways for this module are:**

- Azure Files provides the SMB and NFS protocols, client libraries, and a REST interface that allows access from anywhere to stored files.
    
- Azure Files is ideal to lift and shift an application to the cloud that already uses the native file system APIs. Share data between the app and other applications running in Azure.
    
- Azure Files offers two industry-standard file system protocols for mounting Azure file shares: the Server Message Block (SMB) protocol and the Network File System (NFS) protocol.
    
- Azure Files offers two types of file shares: standard and premium. The premium tier stores data on modern solid-state drives (SSDs), while the standard tier uses hard disk drives (HDDs).
    
- File share snapshots capture a point-in-time, read-only copy of your data.
    
- Soft delete allows you to recover your deleted file share.
    
- Azure Storage Explorer is a standalone application that makes it easy to work with stored data on Windows, macOS, and Linux.
    
- Azure File Sync enables you to cache file shares on an on-premises Windows Server or cloud virtual machine.

# Virtual Machines
## Summary and resources

In this module, you learned about Linux virtual machines in Azure.

- In the first exercise, you created a virtual machine in the portal, connected using SSH, and installed the Nginx server.
- In the second exercise, you enabled VM Insights, created action groups and alerts, and monitored the virtual machine metrics and logs.
- In the third exercise, you added a data disk, and accessed blob and file storage. Additionally you assigned an Azure role, configured a managed identity, and used AzCopy.
- In the fourth exercise, you used Azure Backup to create a virtual machine backup policy.

## Key takeaways

Here are the main takeaways for the module.

- Azure virtual machines are on-demand, scalable computing resources. Both Windows and Linux virtual machines are available.
- Configuring virtual machines includes choosing an operating system, image size, storage, and networking settings.
- There are several ways to securely connect to a Linux virtual machine. One of the most common connections is SSH with a credential file.
- Network Security Group rules let you allow or deny inbound and outbound port connections. For example, port 22 for SSH.
- Azure Monitor provides alerts to help you detect and address issues before users notice.
- You can configure alerts on any virtual machine metric or log data.
- Data disks can be added to virtual machines. In Linux, the disk must be formatted and mounted.
- Virtual machines can access Azure file shares and blob storage. Managed identities and Azure roles provide secure access.
- AzCopy is a utility to transfer data from virtual machines to Azure storage accounts.
- Azure Backup provides retention and backup policies for virtual machines.

## Learn more with online training

- [Monitor your Azure virtual machines with Azure Monitor](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/). Monitor your Azure VMs by using Azure Monitor agent to collect and analyze VM host and client metrics and logs.
- [Provisioning a Linux virtual machine in Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/provision-linux-virtual-machine-in-azure/). Azure allows you to use several common provisioning tools to deploy Linux virtual machines (VMs), to include Terraform, Bicep, the Azure portal, and the Azure CLI. In this module, you learn how to deploy a Linux virtual machine using each of these methods.
- [Add and size disks in Azure virtual machines](https://learn.microsoft.com/en-us/training/modules/add-and-size-disks-in-azure-virtual-machines/). Understand and create the different types of disk storage available to Azure virtual machines (VMs). This task includes adding a data disk and resizing a data disk.
- [Protect your virtual machines by using Azure Backup](https://learn.microsoft.com/en-us/training/modules/protect-virtual-machines-with-azure-backup/). Use Azure Backup to help protect on-premises servers, virtual machines, SQL Server, Azure file shares, and other workloads.


# Understanding Entra ID
## Summary

Active Directory provides the core service of identity management. AD DS is the traditional on-premises solution, whereas Microsoft Entra ID is the cloud-based solution. Microsoft Entra ID is frequently adopted at first to facilitate authentication for cloud-based apps, but is capable of providing authentication services for the entire infrastructure. While they provide similar solutions, each offer different capability and are often used together to provide a best-of-breed solution. Microsoft Entra ID is offered as a free service, with paid tiers for additional capabilities, depending on an organization's needs.

### Learn more

- [What is Microsoft Entra ID?](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-whatis)
- [Compare Active Directory to Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-compare-azure-ad-to-ad)
# Deploy Linux VM
This module reviewed the process of planning a deployment of Azure Linux VMs.

- You chose the VM sizes most suitable for their intended workloads and identified the corresponding networking dependencies.
- You learned how to m
- 
- anage and troubleshoot your VMs by using boot diagnostics and serial console.
- You reviewed storage options and performance optimization techniques that help maximize the benefits of the planned deployment.

With the knowledge you've gained, you can recommend the compute, networking, and storage options most suitable for hosting your company's Linux-based workloads on Azure VMs.

## Related resources

- [Sizes for virtual machines in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes?toc=%2Fazure%2Fvirtual-network%2Ftoc.json)
- [What are Azure Reservations?](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations)
- [Use Azure Spot Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms)
- [What is Azure Bastion?](https://learn.microsoft.com/en-us/azure/bastion/bastion-overview)
- [Azure Serial Console for Linux](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/serial-console-linux)
- [Use Serial Console to access GRUB and single-user mode](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/serial-console-grub-single-user-mode)
- [Create an Azure Virtual Machine with Accelerated Networking](https://learn.microsoft.com/en-us/azure/virtual-network/create-virtual-machine-accelerated-networking)
- [Create an Azure Virtual Machine with Accelerated Networking](https://learn.microsoft.com/en-us/azure/virtual-network/create-virtual-machine-accelerated-networking)
- [Optimize network throughput for Linux virtual machines](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-optimize-network-bandwidth#linux-virtual-machines)
- [Azure managed disk types](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types)
- [Azure premium storage: design for high performance](https://learn.microsoft.com/en-us/azure/virtual-machines/premium-storage-performance)
- [Create a SWAP partition for an Azure Linux VM](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/create-swap-file-linux-vm)
- [Optimize your Linux VM on Azure](https://learn.microsoft.com/en-us/previous-versions/azure/virtual-machines/linux/optimization)
- [Configure Software RAID on Linux](https://learn.microsoft.com/en-us/previous-versions/azure/virtual-machines/linux/configure-raid?toc=%2Fazure%2Fvirtual-machines%2Flinux%2Ftoc.json)
- [Configure LVM on a Linux VM in Azure](https://learn.microsoft.com/en-us/previous-versions/azure/virtual-machines/linux/configure-lvm)
- [Cloud-init support for virtual machines in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/using-cloud-init)
- [Azure Linux VM Agent overview](https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/agent-linux)

# Intro to Linux on Azure Summary
With Azure, you have the freedom to choose to use IaaS, PaaS, or both. Before you plan a move to Azure, you need to evaluate your short-term and long-term goals and decide the best approach for your various workloads. With Linux on Azure, you can take advantage of existing Linux skill sets and rely on familiar tools and methods for provisioning and maintaining systems while offloading hardware support responsibilities. When you're ready, you can use tools like Azure Resource Manager to integrate with more advanced services and solutions.

As with any technology shift, analyzing the current environment and planning carefully are key.

Now that you have a better understanding of the resources available for your Linux deployment, it's time to begin planning and sizing your environment to best meet your needs.

## Learn more

- [Choose an Azure compute service - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree)
- [Use platform as a service (PaaS) options - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/managed-services?source=recommendations)
- [Integrated support for Red Hat solutions in Microsoft Azure](https://www.redhat.com/en/partners/microsoft/red-hat-on-azure)
- [Red Hat on Azure](https://azure.microsoft.com/solutions/linux-on-azure/red-hat/)
- [SUSE on Azure](https://azure.microsoft.com/solutions/linux-on-azure/suse/)
- [Ubuntu on Azure](https://ubuntu.com/azure)
- [Azure Hybrid Benefit for Red Hat Enterprise Linux (RHEL) and SUSE Linux Enterprise Server (SLES) virtual machines](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/azure-hybrid-benefit-linux)


#  Configure Virtual Networks Summary and resources

In this module, you learned about Azure virtual networks and their importance in creating private networks in Azure. You explored the benefits of using virtual networks, such as scalability, availability, and isolation. You learned how to create virtual networks with subnetting and how to determine which resources require public or private IP addresses.

The main takeaways from this module are:

- Azure virtual networks allow different Azure resources to securely communicate with each other, the internet, and on-premises networks.
    
- Subnets within virtual networks provide logical divisions, improving security, performance, and management.
    
- When creating virtual networks, ensure that the IP address space is unique and doesn't overlap with other subnets.
    
- IP addresses can provide public or private access to resources.
    

## Learn more with Copilot

Copilot can assist you in designing Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- Explain CIDR for a nontechnical audience. Provide examples.
    
- What are the basic steps and considerations for creating a virtual network in Azure?
    
- What types of Azure resources should be assigned a static IP address?
    

## Learn more with documentation

- [What is Azure Virtual Network?](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview). This article is your starting point to learn about virtual networks.
    
- [Public IP addresses](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/public-ip-addresses). This article reviews the basics of when to use public IP addresses.
    
- [Private IP addresses](https://learn.microsoft.com/en-us/azure/virtual-network/private-ip-addresses). This article reviews the basics of when to use private IP addresses.
    

## Learn more with self-paced training

- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/). Learn how to design and implement core Azure Networking infrastructure.
    
- [Implement Windows Server IaaS virtual machine IP addressing and routing](https://learn.microsoft.com/en-us/training/modules/implement-windows-server-iaas-virtual-machine-ip-addressing-routing/). Learn about IP addressing and virtual networks for virtual machines.


# Network Security Group Summary
In this module, you learned about network security groups (NSGs) in Azure. NSGs are used to limit network traffic to resources in your virtual network by containing a list of security rules. You can associate NSGs with subnets or network interfaces and define rules to control inbound and outbound traffic.

You also learned how NSG rules are evaluated and processed. Lastly, you learned how application security groups, allow for grouping virtual machines based on workload.

The main takeaways from this module are:

- Network security groups are essential for controlling network traffic in Azure virtual networks.
    
- NSG rules are evaluated and processed based on priority and can be created for subnets and network interfaces.
    
- Effective NSG rules can be achieved by considering rule precedence, intra-subnet traffic, and managing rule priority.
    
- Application security groups provide an application-centric view of infrastructure and simplify rule management.
    

## Learn more with Copilot

Copilot can assist you in designing Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- What is the difference between an Azure network security group and an application security group? Provide usage examples.
    
- Can you explain NSG rules in detail?
    
- How can I troubleshoot network security group rules?
    

## Learn more with documentation

- [Read about network security groups](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview). This article describes the properties of a network security group rule, the default security rules that are applied, and the rule properties that you can modify.
    
- [Filter network traffic with network security groups in the Azure portal](https://learn.microsoft.com/en-us/azure/virtual-network/tutorial-filter-network-traffic). Learn how to create a network security group and an application security group.
    
- [Create, change, or delete a network security group](https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group?tabs=network-security-group-portal). Learn how to work with network and application security groups.
    
- [Application security groups](https://learn.microsoft.com/en-us/azure/virtual-network/application-security-groups). Learn about application security groups and traffic control with rules.
    

## Learn more with self-paced training

- [Secure and isolate access to Azure resources with network security groups and service endpoints (sandbox)](https://learn.microsoft.com/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/). Learn how to secure your virtual machines and Azure services from unauthorized network access.
    
- [Filter network traffic with a network security group using the Azure portal](https://learn.microsoft.com/en-us/training/modules/filter-network-traffic-network-security-group-using-azure-portal/). Learn how to create, configure, and apply NSGs for improved network security.
# Host your Domain on Azure DNS summary
Your company recently bought the custom domain name wideworldimporters.com from a third-party domain-name registrar. The domain name is for a new website your organization plans to launch. You need a hosting service for DNS domains. This hosting service would resolve the wideworldimporters.com domain to your Azure-based web server's IP address.

Your company wanted to manage all their infrastructure and related domain name information in one place. You saw how easy it was to manage Domain Name System (DNS) information by using an Azure DNS zone. First, you created an Azure DNS zone, and then you updated the NS records at your domain registrar to point at it.

You learned the uses of the different record sets, A, AAAA, CNAME, NS, and SOA. You also learned how you can use Azure aliases to override the static A/AAAA/CNAME record to provide a dynamic reference to your resources. Using an Azure DNS zone improved your company's administration of resources, because your staff only needed one place to manage DNS-related tasks.

The Azure DNS zone allows better control and integration with your Azure resources. It's possible to achieve some of the more basic record set functions by using the domain registrar's management console. However, linking to any of your Azure resources becomes difficult or impossible without a high degree of complex redirection.

By using an Azure DNS zone to host your domain, your organization benefits by having all the resources managed through a single, common interface. This solution provides better integration with existing Azure resources, improved security, and monitoring tools.

 Important

In the optional exercises for this module, you created resources by using your own Azure subscription. Clean up these resources so that you won't continue to be charged for them.

## Learn more

- [Quickstart: Create an Azure private DNS zone by using the Azure portal](https://learn.microsoft.com/en-us/azure/dns/private-dns-getstarted-portal)
- [Overview of DNS zones and records](https://learn.microsoft.com/en-us/azure/dns/dns-zones-records)
# Configure Vnet Peering Summary
In this module, you learned Azure Virtual Network peering lets you connect virtual networks in a hub and spoke topology. You learned how to configure your virtual networks with Azure VPN Gateway for transit connectivity. You explored how to extend peering with user-defined routes and service chaining.

The main takeaways from this module are:

- Azure Virtual Network peering allows for the connection of virtual networks in a hub and spoke topology.
    
- There are two types of peering: regional and global. Regional peering connects virtual networks in the same region. Global peering connects virtual networks in different regions.
    
- Network traffic between peered virtual networks is private and kept on the Azure backbone network.
    
- You can configure Azure VPN Gateway in the peered virtual network as a transit point to access resources in another network.
    
- Network security groups can be applied to block or allow access between virtual networks when configuring virtual network peering.
    

## Learn more with Copilot

Copilot can assist you in designing Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- What is Azure virtual network peering and what are the advantages of this feature?
    
- What are some of the configurations settings for Azure virtual network peering?
    

## Learn more with documentation

- [Azure Virtual Network peering](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview). This article is your starting point for learning about virtual network peering.
    
- [Create, change, or delete a virtual network peering](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-peering?tabs=peering-portal). This article reviews how to create a virtual network peering and what each setting means.
    

## Learn more with self-paced training

- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/). Learn how to design and implement core Azure networking infrastructure such as virtual networks, and virtual network peering.

# control-network-traffic-flow-with-routes
In this module, you learned how to customize routes in an Azure virtual network and how to redirect the traffic flow through a network virtual appliance. You also learned how to create your own custom network virtual appliance by deploying an Azure virtual machine.

 Important

In the optional exercises for this module, you created resources by using your own Azure subscription. Clean up these resources so that you won't continue to be charged for them.

## Learn more

For more information on using routes in your network infrastructure, see the following articles:

- [Virtual network traffic routing](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview)
- [Tutorial: Route network traffic with a route table using the Azure portal](https://learn.microsoft.com/en-us/azure/virtual-network/tutorial-create-route-table-portal)
- [Deploy highly available network virtual appliances](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/dmz/nva-ha)
- [Implement a secure hybrid network](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/dmz/secure-vnet-dmz)
# Load Balance Summary

In this module, you learned about Azure Load Balancer. An Azure service that allows you to evenly distribute incoming network traffic across a group of Azure virtual machines, or across instances in a Virtual Machine Scale Set. You also learned how Load Balancer delivers high availability and network performance to your applications. You learned about the types of scenarios in which Load Balancer is an appropriate solution for your organization, and how Load Balancer is likely able to meet Adatum's networking needs. You also learned about the difference between Azure Load Balancer and other traffic management technologies, including Azure Application Gateway and Azure Traffic Manager.
## Learn more

- [What is Azure Load Balancer?](https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview)
- [Load-balancing options](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview)
- [Azure Load Balancer components](https://learn.microsoft.com/en-us/azure/load-balancer/components)
- [Module: Introduction to Azure Load Balancer](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-load-balancer/)
# Azure application Gateway Summary

In this module, you learned about Azure Application Gateway, a service that allows you to manage the requests that client applications can send to a web app. You learned that Application Gateway routes traffic to a pool of web servers based on the URL of a request. The pool of web servers can be Azure virtual machines, Azure virtual machine scale sets, Azure App Service, and even on-premises servers. You learned that Application Gateway provides features such as load balancing HTTP traffic, a web application firewall, and support for TLS/SSL encryption of your data. You also learned that Application Gateway supports encrypting traffic between users and an application gateway, and between application servers and an application gateway.

## Learn more

- [What is Azure Application Gateway?](https://learn.microsoft.com/en-us/azure/application-gateway/overview)
- [Azure Application Gateway features](https://learn.microsoft.com/en-us/azure/application-gateway/features)
- [How an application gateway works](https://learn.microsoft.com/en-us/azure/application-gateway/how-application-gateway-works)
- [Application gateway components](https://learn.microsoft.com/en-us/azure/application-gateway/application-gateway-components)
- [Load balance your web service traffic with Application Gateway](https://learn.microsoft.com/en-us/training/modules/load-balance-web-traffic-with-application-gateway/)

# Network Watcher Summary

In this module, you learned about Azure Network Watcher, a service you can use to perform monitoring and diagnostic tasks on IaaS resources deployed on Azure virtual networks. You learned about the monitoring and diagnostic tools that are available in Network Watcher, and which tool is appropriate for specific troubleshooting scenarios.

## Learn more

- [What is Azure Network Watcher?](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview)
- [Enable or disable Azure Network Watcher](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-create)
- [Monitor and troubleshoot your end-to-end Azure network infrastructure by using network monitoring tools](https://learn.microsoft.com/en-us/training/modules/troubleshoot-azure-network-infrastructure/)
- [Configure Network Watcher](https://learn.microsoft.com/en-us/training/modules/configure-network-watcher/)
- [Design and implement network monitoring](https://learn.microsoft.com/en-us/training/modules/design-implement-network-monitoring/)

# Create-configure-manage-identities Summary and resources

You completed this module, you are able to:

- Create, configure, and manage users
- Create, configure, and manage groups
- Manage licenses
- Configure and manage device registration
- Explore custom security attributes and automatic account provisioning

## Resources

Use these resources to discover more:

- [Quickstart: Create and assign a user account](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-assign-users)
    
- [Bulk create users in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/users/users-bulk-add)
    
- [Create a basic group and add members using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups)
    
- [Create or update a dynamic membership group in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/users/groups-create-rule)
    
- [What is Microsoft Entra Cloud Sync?](https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/what-is-cloud-sync)
    
- [Manage license requests](https://learn.microsoft.com/en-us/microsoft-365/commerce/licenses/manage-license-requests)
    
- [Assign licenses to users - Microsoft 365 Admin Center](https://learn.microsoft.com/en-us/microsoft-365/admin/manage/assign-licenses-to-users)
    
- [Plan Microsoft Entra device deployment](https://learn.microsoft.com/en-us/entra/identity/devices/plan-device-deployment)
    
- [API-driven inbound provisioning concepts](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/inbound-provisioning-api-concepts)


# Azure policy initiatives Summary

Azure Policy is a crucial component of the governance model in the Cloud Adoption Framework for Azure, which is designed to balance control and stability with speed and results. It helps you enforce organizational and regulatory standards and assess compliance at scale through built-in and custom policies and policy initiatives.

The module covered the hierarchical organization of Azure resources, policy operations in Greenfield and Brownfield scenarios, and the various components of policy definitions. You also delved into the evaluation and effects of policies, safe deployment practices, and integration with Event Grid for automated actions based on policy state changes. Key points included:

- Importance of careful policy design
- Testing to ensure effective governance without disrupting operations
- Logical operators and conditions in policy evaluation
- Supported effect types such as _disabled_, _modify_, _deny_, _audit_, _deployIfNotExists_, and _manual_

Additionally, the module emphasized starting with _enforcementMode_ deactivated for new policies to test their impact and then deploying policies in rings to gradually expand to production environments.

For more information, see the [Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) documentation.
# RBAC Summary
In this module, you learned about Azure RBAC, and how you can use it to secure your Azure resources. To grant access, you assign users a role at a particular scope. Using Azure RBAC, you can grant only the amount of access to users that they need to perform their jobs.

Azure RBAC has more than 200 built-in roles. However, if your organization needs specific permissions, you can create your own custom roles. Azure keeps track of your Azure RBAC changes in case you need to see what changes were made in the past.

## Further reading

To continue learning about Azure RBAC, check out [What is Azure role-based access control (Azure RBAC)?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).
# SSPR Summary

In this module, you've learned how you can use SSPR in Microsoft Entra ID to allow users to reset their forgotten or expired passwords. An administrator doesn't have to do the password reset. SSPR is secured by authentication methods of your choice. These methods can include a mobile authentication app, a code sent to you by an SMS text message, or security questions.

SSPR helps reduce the amount of work required from administrators. It also minimizes the productivity impact for users when they forget their password.

## Clean up

Remember to clean up after you've finished.

- **Delete the user you created in Microsoft Entra ID**: Go to **Microsoft Entra ID** > **Manage** > **Users**. Check the box next to the user and select **Delete**. Select **OK**.
- **Delete the group you created in Microsoft Entra ID**: Go to **Microsoft Entra ID** > **Manage** > **Groups**. Check the box next to the group and select **Delete**. Select **OK**.
- **Turn off self-service password reset**: Go to **Microsoft Entra ID** > **Manage** > **Password reset**. Under **Self service password reset enabled**, select **None**. Select **Save**.

If you created a Premium trial Microsoft Entra tenant for this module, you can delete the tenant 30 days after the trial has expired.

## Learn more

- [Tutorial: Enable users to unlock their account or reset passwords using Microsoft Entra self-service password reset](https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr)
- [How it works: Microsoft Entra self-service password reset](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks)
- [Enable self-service password reset](https://learn.microsoft.com/en-us/entra/external-id/customers/how-to-enable-password-reset-customers)

# VM Scaling and Availability Summary and resources

Azure provides several high availability options for virtual machines. You can achieve high availability by using availability sets, availability zones, and Azure Virtual Machine Scale Sets.

In this module, you learned how to configure virtual machine availability by using availability sets and availability zones with update and fault domains. You discovered how to autoscale virtual machines and configure vertical and horizontal scaling. You reviewed how to implement Virtual Machine Scale Sets, including storage resiliency and scalability options.

The main takeaways from this module are:

- Azure Virtual Machine Scale Sets allow for the deployment and management of a group of identical virtual machines, making it easier to build large-scale services.
    
- Autoscaling with Virtual Machine Scale Sets helps optimize performance by automatically adjusting the number of instances based on workload demands.
    
- Availability sets and availability zones are important features in Azure for achieving high availability and fault tolerance for virtual machines.
    

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- How do virtual machine scale sets work with Azure availability zones and sets?
    
- What is the difference between manual and autoscaling of Azure virtual machines?
    

## Learn more with documentation

- [Availability options for Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/availability). This article provides an overview of the availability options for Azure virtual machines (VMs).
    
- [Autoscale with Azure Virtual Machine Scale Sets](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-autoscale-overview). This article reviews when use Virtual Machine Scale Sets.
    
- [Create virtual machines in a scale set using Azure portal](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/flexible-virtual-machine-scale-sets-portal). This article steps through using Azure portal to create a Virtual Machine Scale Set.
    

## Learn more with self-paced training

- [Introduction to Azure Virtual Machines (sandbox)](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-virtual-machines/). Learn about the decisions you make before creating a virtual machine, the options to create and manage the VM, and the extensions and services you use to manage your VM.
    
- [Implement scale and high availability with Windows Server VM](https://learn.microsoft.com/en-us/training/modules/implement-scale-high-availability-windows-server-virtual-machine/). You learn how to implement scaling for virtual machine scale sets and load-balanced VMs. You also learn how to implement Azure Site Recovery.
    
- [Introduction to Azure Virtual Machine Scale Sets](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-virtual-machine-scale-sets/). Learn about what Azure Virtual Machine Scale Sets do, how they work, and when you should use Azure Virtual Machine Scale Sets as a solution for your organization.

# Configure app service plans Summary and resources

In this module, you learned about Azure App Service plans and how they're used to define the compute resources for running applications in Azure App Service. These plans can be configured with a specific region, number of virtual machine instances, and size of virtual machine instances. The pricing tier of the App Service plan determines the features and cost. Pricing tiers include Free and Shared plans for development and testing purposes. Pricing tiers also include Isolated plans for mission-critical workloads.

You learned about scaling in Azure App Service. Scale up involves increasing the CPU, memory, and disk space by changing the pricing tier. Scale out increases the number of virtual machine instances running the application. Autoscaling allows you to automatically adjust the number of resources based on the load on your application. Autoscale can be configured with metric-based or time-based rules.

The main takeaways from this module are:

- Azure App Service plans are used to define the compute resources for running web applications in Azure App Service.
- The pricing tier of the App Service plan determines the features and cost, with options ranging from Free and Shared plans to Isolated plans.
- Scaling in Azure App Service can be done through scale up (changing the pricing tier) or scale out (increasing the number of virtual machine instances).
- Autoscaling allows for automatic adjustment of resources based on application load, with metric-based and time-based rules.

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- In Microsoft Azure, what are app service pricing plans? Provide examples of when to use each plan.
    
- In Microsoft Azure, what does scale in and scale out mean? How do I determine when to scale an application?
    

## Learn more with documentation

- [Azure App Service plans](https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans). This article provides an overview of App Service plans.
    
- [Manage an App Service plan in Azure](https://learn.microsoft.com/en-us/azure/app-service/app-service-plan-manage). This guide shows how to create and manage an App Service plan.
    
- [Scale up an app in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/manage-scale-up). This article shows you how to scale your app in Azure App Service.
    

## Learn more with self-paced training

- [Scale apps in Azure App Service](https://learn.microsoft.com/en-us/training/modules/scale-apps-app-service/). Learn how autoscale operates in App Service. Learn to identify autoscale factors, enable autoscale, and create autoscale conditions.
# App Services Summary and resources

Azure App Service is an HTTP-based service for hosting web applications. With App Service, you can develop web apps in your favorite language. The service lets you easily run and scale your web apps on Windows and Linux-based environments.

In this module, you reviewed the features and usage cases for Azure App Service. You learned how to create, secure, and back up your web apps. You explored how to configure deployment settings, including deployment slots, and custom domain names for your web apps. You discovered how to use Azure Application Insights to monitor web apps.

## The main takeaways for this module

- Azure App Service lets you develop and deploy web, mobile, and API apps.
    
- Azure App Service configuration settings include runtime stack, operating system, region, and App Service plan.
    
- Deployment slots help you manage different app stages. For example, development, test, stage, and production.
    
- The default Azure App Service domain name can be customized for your organization.
    
- Azure Application Insights is a feature of Azure Monitor that lets you monitor your live applications. You can integrate Application Insights with your App Service configure to automatically detect performance anomalies in your apps.
    
- Application Insights lets you continuously monitor the performance and usability of your apps.
    

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- What are the main tasks to configure an Azure App Service web app?
    
- What options are available for scaling an Azure App Service web app?
    

## Learn more with documentation

- [App Service overview](https://learn.microsoft.com/en-us/azure/app-service/overview). This article provides an overview of the App Service and why you would use this service.
    
- [Configure an App Service app](https://learn.microsoft.com/en-us/azure/app-service/configure-common). This article explains how to configure common settings for web apps, mobile back end, or API app.
    
- [Set up staging environments in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots). The article covers deployment slots and swap operations.
    

## Learn more with self-paced training

- [Stage a web app deployment for testing and rollback by using App Service deployment slots](https://learn.microsoft.com/en-us/training/modules/stage-deploy-app-service-deployment-slots/). Learn to use deployment slots to streamline deployment and roll back.
    
- [Explore Azure App Service deployment slots](https://learn.microsoft.com/en-us/training/modules/understand-app-service-deployment-slots/). Learn how slot swapping works and how to route traffic to different slots.
    
- [Host a web application with Azure App Service](https://learn.microsoft.com/en-us/training/modules/host-a-web-app-with-azure-app-service/). Learn how to create a website through the hosted web app platform in Azure App Service.

# Container instances Summary and resources

In this module, you learned how to identify when to use Azure Container Instances versus Azure virtual machines. You explored the features and usage cases of Azure Container Instances. You discovered how to implement Azure container groups.

The main takeaways from this module are:

- Containers provide lightweight isolation and use fewer system resources compared to virtual machines.
- Containers can be deployed individually using Docker or with an orchestrator like Azure Container Apps.
- Containers use Azure Disks or Azure Files for storage.
- A container group is a collection of containers that get scheduled on the same host machine.
- Containers can be rapidly recreated on another cluster node if a node fails.

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- Compare benefits and usage cases for containers and virtual machines.
    
- What are the best practices for configuring Azure Container Instances for task-based workloads? Explain the restart policies.
    
- How do I deploy a multi-container group in Azure Container Instances using Bicep? Show an example with environment variables.
    

## Learn more with documentation

- [Containers versus virtual machines](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/containers-vs-vm). This article reviews the key similarities and differences between containers and virtual machines (VMs), and when you might want to use each.
    
- [Quickstart: Deploy a container instance in Azure using the Azure portal](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-quickstart-portal). In this quickstart, you use the Azure portal to deploy an isolated Docker container and make its application available with a fully qualified domain name (FQDN). After configuring a few settings and deploying the container, you can browse to the running application:
    
- [Container groups in Azure Container Instances](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-container-groups). This article describes what container groups are and the types of scenarios they enable.
    

## Learn more with self-paced training

- [Run container images in Azure Container Instances](https://learn.microsoft.com/en-us/training/modules/create-run-container-images-azure-container-instances/). Learn how Azure Container Instances can help you quickly deploy containers, how to set environment variables, and specify container restart policies.
    
- [Implement Azure Container Apps](https://learn.microsoft.com/en-us/training/modules/implement-azure-container-apps/). Learn how Azure Container Apps can help you deploy and manage microservices and containerized apps on a serverless platform that runs on top of Azure Kubernetes Service.
    
- [Introduction to Docker containers](https://learn.microsoft.com/en-us/training/modules/intro-to-docker-containers/). Learn the benefits of using Docker containers as a containerization platform. Discuss the infrastructure provided by the Docker platform.
# Storage accounts Summary and resources

In this module, you learned about Azure Storage and how to create a storage account.

**The main takeaways from this module are:**

- Azure Storage provides a range of storage options for different types of data, including virtual machine data, unstructured data, and structured data.
    
- There are different types of storage accounts available, each with its own features and pricing model. It's important to consider the specific requirements of your application when choosing the right storage account type.
    
- Azure Storage offers four data services: Azure Blob Storage, Azure Files, Azure Queue Storage, and Azure Table Storage. Each service is optimized for different types of data and has its own use cases and benefits.
    
- Replication is an important consideration for ensuring data durability and high availability. Azure Storage offers different replication strategies to choose from based on your requirements.
    
- Configuring custom domains and secure endpoints allow you to access and secure your storage account in Azure.
    

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- What is an Azure storage account? What type of storage accounts are available?
    
- Explain for a nontechnical person Azure data redundancy for storage accounts.
    

## Learn more with Azure documentation

- [Storage account overview](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview). This article is your starting point for learning about Azure storage accounts.
    
- [Azure storage redundancy](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy). This article reviews how to tradeoff cost and availability when selecting a redundancy option.
    

## Learn more with self-paced training

- [Create an Azure storage account](https://learn.microsoft.com/en-us/training/modules/create-azure-storage-account/). Learn how to create an Azure Storage account with the correct options for your business needs.
    
- [Design and implement private access to Azure Services](https://learn.microsoft.com/en-us/training/modules/design-implement-private-access-to-azure-services/). Learn how to implement private access to Azure Services with Azure Private Link, and virtual network service endpoints.

# Blob Storage Summary and resources

In this module, you learned about Azure Blob Storage and how to configure it. You discovered that Blob Storage is Microsoft's object storage solution for the cloud. You learned Azure blob storage is optimized for storing massive amounts of unstructured data like text or binary files. You explored the features of Blob Storage and its use cases. You also learned how to configure Blob Storage, including choosing the appropriate access tiers to reduce cost and improve performance. And, you learned about creating a lifecycle management strategy, and configuring object replication for failover.

**The main takeaways from this module are:**

- Azure Blob Storage is a powerful solution for storing unstructured data in the cloud, such as text documents, images, and videos.
- Blob Storage offers different access tiers (Hot, Cool, Cold, and Archive) to optimize performance and cost based on the usage patterns of your data.
- You can configure lifecycle management policies to automatically transition data between access tiers and set expiration times for data.
- Object replication allows you to asynchronously copy blobs between containers in different regions, providing redundancy and reducing latency for read requests.

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- What are common administration tasks associated with Azure blob storage?
    
- How is Azure blob storage priced?
    

## Learn more with Azure documentation

- [Azure Blob Storage documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/) - Microsoft Azure's official documentation provides comprehensive information on configuring and managing blob storage. You can find detailed guides, tutorials, and examples to help you navigate through different aspects of blob storage configuration.
    
- [Azure Blob Storage Concepts](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) - This article provides an overview of the key concepts related to Azure Blob Storage, including storage accounts, containers, and blobs. It explains how to create and manage these entities and covers various configuration options.
    
- [Azure Blob Storage Security](https://learn.microsoft.com/en-us/azure/storage/blobs/security-recommendations) - Understanding the security aspects of blob storage is crucial for proper configuration. This article explores authentication, authorization, and encryption options available in Azure Blob Storage. It also covers best practices for securing your blob storage resources.
    
- [Azure Blob Storage Performance and Scalability](https://learn.microsoft.com/en-us/azure/storage/blobs/scalability-targets) - This article delves into performance considerations when configuring blob storage. The module covers the storage account type, and optimizing data transfer.
    
- [Azure Blob Storage Lifecycle Management](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-lifecycle-management-concepts) - Blob storage lifecycle management allows you to automate the movement and deletion of data based on predefined rules. This article explains how to configure and manage lifecycle policies to optimize storage costs and improve data management.

# Storage Security Summary and resources

Azure Administrators must be familiar with how to configure storage security.

In this module, you examined several options for securing Azure Storage. You discovered how to configure shared access signatures (SAS), including the uniform resource identifier (URI) and SAS parameters. You reviewed how to implement customer-managed keys and define stored access policies to configure Azure Storage encryption. You explored opportunities for improving your Azure Storage security solution.

## Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

- What are the different ways to secure Azure storage? Provide usage case examples.
    
- How do I configure an Azure Shared Access Signature?
    

## Learn more with documentation

- Grant [limited access to Azure Storage resources with shared access signatures](https://learn.microsoft.com/en-us/azure/storage/common/storage-dotnet-shared-access-signature-part-1).
    
- Read about [Azure Storage encryption for data at rest](https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption).
    
- Create a [SAS for your Azure storage account](https://learn.microsoft.com/en-us/rest/api/storageservices/create-account-sas).
    
- Create a [service-level SAS](https://learn.microsoft.com/en-us/rest/api/storageservices/create-service-sas).
    
- Construct a [user delegation SAS](https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas#construct-a-user-delegation-sas).
    
- Use [customer-managed keys for Azure Storage encryption](https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview).
    

## Learn more with self-paced training

- Secure your [Azure storage account](https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/).
    
- Implement [Azure Storage security](https://learn.microsoft.com/en-us/training/modules/security-storage/).