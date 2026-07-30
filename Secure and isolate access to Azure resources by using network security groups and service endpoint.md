
# Introduction

Imagine you're the solution architect for a manufacturing company. Your company has several sites, and users throughout the company need to use an enterprise resource planning (ERP) app to migrate to Azure. The company will only consider moving key systems onto the platform if stringent security requirements can be met. One requirement is tight control over which computers have network access to the servers running the app. You want to secure both virtual machine (VM) networking and Azure services networking as part of your company's network security strategy. Your goal is to prevent unwanted or unsecured network traffic from being able to reach key systems.

You'll use network security groups to secure network traffic for VMs running on Azure. You'll learn to use virtual network service endpoints to control network traffic to and from Azure services, such as storage or database services.

# Use network security groups to control network access

As part of the project to move your ERP system to Azure, you must ensure that servers have proper isolation so that only allowed systems can make network connections. For example, you have database servers that store data for your ERP app. You want to block prohibited systems from communicating with the servers over the network, while allowing app servers to communicate with the database servers.

## Network security groups

Network security groups filter network traffic to and from Azure resources. They also contain security rules that you configure to allow or deny inbound and outbound traffic. You can use network security groups to filter traffic between VMs or subnets, both within a virtual network and from the internet.

### Network security group assignment and evaluation

Network security groups are assigned to a network interface or a subnet. When you assign a network security group to a subnet, the rules apply to all network interfaces in that subnet. You can restrict traffic further by associating a network security group to a VM's network interface.

When you apply network security groups to both a subnet and a network interface, each network security group is evaluated independently. Inbound traffic is first evaluated by the network security group applied to the subnet, then by the network security group applied to the network interface. Conversely, outbound traffic from a VM is first evaluated by the network security group applied to the network interface, then by the network security group applied to the subnet.

![Diagram of network security groups.](https://learn.microsoft.com/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/media/2-nsg1.png)

Applying a network security group to a subnet instead of individual network interfaces can reduce administration and management efforts. This approach also ensures that all VMs within the specified subnet are secured with the same set of rules.

Each subnet and network interface can have one network security group applied to it. Network security groups support TCP (Transmission Control Protocol), UDP (User Datagram Protocol), and ICMP (Internet Control Message Protocol), and operate at Layer 4 of the OSI (Open Systems Interconnection) model.

In this manufacturing-company scenario, network security groups can help you secure the network. You can control which computers can connect to your app servers. You can configure the network security group so that only a specific range of IP addresses can connect to the servers. You can lock this down even more by only allowing access to or from specific ports or from individual IP addresses. You can apply these rules to devices that are connecting remotely from on-premises networks or between resources within Azure.

## Security rules

A network security group contains one or more security rules. You can configure security rules to either allow or deny traffic.

Rules have several properties:

|Property|Explanation|
|---|---|
|Name|A unique name within the network security group|
|Priority|A number between 100 and 4096|
|Source and destination|Any, or an individual IP address, classless inter-domain routing (CIDR) block (10.0.0.0/24, for example), service tag, or app security group|
|Protocol|TCP, UDP, or Any|
|Direction|Whether the rule applies to inbound or outbound traffic|
|Port range|An individual port or range of ports|
|Action|Allow or deny the traffic|

Network security group security rules are evaluated by priority. They use the five-tuple information (source, source port, destination, destination port, and protocol) to allow or deny the traffic. When the conditions for a rule match the device configuration, rule processing stops.

For example, suppose your company has created a security rule to allow inbound traffic on port 3389 (RDP) to your web servers, with a priority of 200. Next, suppose that another admin has created a rule to deny inbound traffic on port 3389, with a priority of 150. The deny rule takes precedence because it's processed first. The rule with priority 150 is processed before the rule with priority 200.

With network security groups, the connections are stateful. Return traffic is automatically allowed for the same TCP/UDP session. For example, an inbound rule allowing traffic on port 80 also allows the VM to respond to the request (typically on an ephemeral port). You don't need a corresponding outbound rule.

Regarding the ERP system, the web servers for the ERP app connect to database servers that are in their own subnets. You can apply security rules to state that the only allowed communication from the web servers to the database servers is port 1433 for SQL Server database communications. All other traffic to the database servers will be denied.

### Default security rules

When you create a network security group, Azure creates several default rules. These default rules can't be changed, but you can override them with your own rules. These default rules allow connectivity within a virtual network and from Azure load balancers. They also allow outbound communication to the internet, and deny inbound traffic from the internet.

The default rules for inbound traffic are:

|Priority|Rule name|Description|
|---|---|---|
|65000|AllowVnetInbound|Allow inbound coming from any VM to any VM within the virtual network|
|65001|AllowAzureLoadBalancerInbound|Allow traffic from the default load balancer to any VM within the subnet|
|65500|DenyAllInBound|Deny traffic from any external source to any of the VMs|

The default rules for outbound traffic are:

|Priority|Rule name|Description|
|---|---|---|
|65000|AllowVnetOutbound|Allow outbound going from any VM to any VM within the virtual network|
|65001|AllowInternetOutbound|Allow outbound traffic going to the internet from any VM|
|65500|DenyAllOutBound|Deny traffic from any internal VM to a system outside the virtual network|

### Augmented security rules

You can use augmented security rules for network security groups to simplify managing large numbers of rules. Augmented security rules also help when you need to implement more complex network sets of rules. Augmented rules let you add the following options into a single security rule:

- Multiple IP addresses
- Multiple ports
- Service tags
- App security groups

Suppose your company wants to restrict access to resources in your datacenter spread across several network address ranges. With augmented rules, you can add all these ranges into a single rule, reducing the administrative overhead and complexity in your network security groups.

### Service tags

You can use service tags to simplify network security group security even further. You can allow or deny traffic to a specific Azure service, either globally or per region.

Service tags simplify security for VMs and Azure virtual networks by allowing you to restrict access by resources or services. Service tags represent a group of IP addresses, and help simplify the configuration of your security rules. For resources that you can specify by using a tag, you don't need to know the IP address or port details.

You can restrict access to many services. Microsoft manages the service tags, meaning you can't create your own. Some examples of the tags are:

- **VirtualNetwork**: Represents all virtual network addresses anywhere in Azure, and in your on-premises network if you're using hybrid connectivity.
- **AzureLoadBalancer**: Denotes Azure's infrastructure load balancer. The tag translates to the virtual IP address of the host (168.63.129.16) where Azure health probes originate.
- **Internet**: Represents anything outside the virtual network address that's publicly reachable, including resources that have public IP addresses. One such resource is the Web Apps feature of Azure App Service.
- **AzureTrafficManager**: Represents the IP address for Azure Traffic Manager.
- **Storage**: Represents the IP address space for Azure Storage. You can specify whether traffic is allowed or denied. You can also specify if access is allowed only to a specific region, but you can't select individual storage accounts.
- **SQL**: Represents the address for Azure SQL Database, Azure Database for MySQL, Azure Database for PostgreSQL, and Azure Synapse Analytics services. You can specify whether traffic is allowed or denied, and you can limit to a specific region.
- **AppService**: Represents address prefixes for Azure App Service.

## App security groups

App security groups let you configure network security for resources used by specific apps. You can group VMs logically, no matter what their IP address or subnet assignment.

You can use app security groups within a network security group to apply a security rule to a group of resources. It's easier to deploy and scale up specific app workloads. You can add a new VM deployment to one or more app security groups, and that VM automatically picks up your security rules for that workload.

An app security group lets you group network interfaces together. You can then use that app security group as a source or destination rule within a network security group.

For example, your company has many front-end servers in a virtual network. The web servers must be accessible over ports 80 and 8080. Database servers must be accessible over port 1433. You assign the network interfaces for the web servers to one app security group, and the network interfaces for the database servers to another app security group. You then create two inbound rules in your network security group. One rule allows HTTP traffic to all servers in the web server app security group. The other rule allows SQL traffic to all servers in the database server app security group.

![Diagram of app security groups.](https://learn.microsoft.com/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/media/2-asg-nsg.svg)

Without app security groups, you'd need to create a separate rule for each VM. Alternatively, you'd need to add a network security group to a subnet, and then add all the VMs to that subnet.

The key benefit of app security groups is that it makes administration easier. You can easily add and remove network interfaces to an app security group as you deploy or redeploy app servers. You can also dynamically apply new rules to an app security group, which are then automatically applied to all the VMs in that app security group.

## When to use network security groups

As a best practice, you should always use network security groups to help protect your networked assets against unwanted traffic. Network security groups give you granular control access over the network layer, without the potential complexity of setting security rules for every VM or virtual network.


# Secure network access to PaaS services with virtual network service endpoints

You've migrated your existing app and database servers for your ERP system to Azure as VMs. Now, to reduce your costs and administrative requirements, you're considering using some Azure platform as a service (PaaS) services. Storage services will hold certain large file assets, such as engineering diagrams. These engineering diagrams have proprietary information, and must remain secure from unauthorized access. These files must only be accessible from specific systems.

In this unit, you'll look at how to use virtual network service endpoints for securing supported Azure services.

## Virtual network service endpoints

Use virtual network service endpoints to extend your private address space in Azure by providing a direct connection to your Azure services. Service endpoints let you secure your Azure resources to only your virtual network. Service traffic will remain on the Azure backbone and doesn't go out to the internet.

![Diagram of a service endpoint on a private network.](https://learn.microsoft.com/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/media/4-service-endpoint.svg)

By default, Azure services are all designed for direct internet access. All Azure resources have public IP addresses, including PaaS services such as Azure SQL Database and Azure Storage. Because these services are exposed to the internet, anyone can potentially access your Azure services.

Service endpoints can connect certain PaaS services directly to your private address space in Azure, so they act like they're on the same virtual network. Use your private address space to access the PaaS services directly. Adding service endpoints doesn't remove the public endpoint. It simply provides a redirection of traffic.

Azure service endpoints are available for many services, such as:

- Azure Storage.
- Azure SQL Database.
- Azure Cosmos DB.
- Azure Key Vault.
- Azure Service Bus.
- Azure Data Lake.

For a service like SQL Database, which you can't access until you add IP addresses to its firewall, you should still consider service endpoints. Using a service endpoint for SQL Database restricts access to specific virtual networks, providing greater isolation and reducing the attack surface.

## How service endpoints work

To enable a service endpoint, you must:

1. Turn off public access to the service.
2. Add the service endpoint to a virtual network.

When you enable a service endpoint, you restrict the flow of traffic and enable your Azure VMs to access the service directly from your private address space. Devices can't access the service from a public network. On a deployed VM vNIC, if you look at **Effective routes**, you'll notice the service endpoint as the **Next Hop Type**.

This is an example route table before enabling a service endpoint:

|SOURCE|STATE|ADDRESS PREFIXES|NEXT HOP TYPE|
|---|---|---|---|
|Default|Active|10.1.1.0/24|VNet|
|Default|Active|0.0.0.0./0|Internet|
|Default|Active|10.0.0.0/8|None|
|Default|Active|100.64.0.0./10|None|
|Default|Active|192.168.0.0/16|None|

And here's an example route table after you've added two service endpoints to the virtual network:

|SOURCE|STATE|ADDRESS PREFIXES|NEXT HOP TYPE|
|---|---|---|---|
|Default|Active|10.1.1.0/24|VNet|
|Default|Active|0.0.0.0./0|Internet|
|Default|Active|10.0.0.0/8|None|
|Default|Active|100.64.0.0./10|None|
|Default|Active|192.168.0.0/16|None|
|Default|Active|20.38.106.0/23, 10 more|VirtualNetworkServiceEndpoint|
|Default|Active|20.150.2.0/23, 9 more|VirtualNetworkServiceEndpoint|

All traffic for the service now is routed to the **VirtualNetworkServiceEndpoint** and remains internal to Azure.

## Service endpoints and hybrid networks

Service resources that you've secured by using virtual network service endpoints aren't, by default, accessible from on-premises networks. To access resources from an on-premises network, use NAT IPs. If you use ExpressRoute for connectivity from on-premises to Azure, you have to identify the NAT IP addresses ExpressRoute uses. By default, each circuit uses two NAT IP addresses to connect to the Azure backbone network. You then need to add these IP addresses into the Azure service resource's IP firewall configuration (for example, Azure Storage).

The following diagram shows how you can use a service endpoint and firewall configuration to enable on-premises devices to access Azure Storage resources:

![Diagram of a service endpoint for on-premises access to Azure resources.](https://learn.microsoft.com/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/media/4-service-endpoint-flow.svg)