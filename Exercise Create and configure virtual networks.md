## Exercise scenario

Your organization is migrating a web-based application to Azure. Your first task is to put in place the virtual networks and subnets. You also need to securely peer the virtual networks. You identify these requirements.

- Two virtual networks are required, app-vnet and hub-vnet. The virtual networks simulate a hub and spoke network architecture.
- The app-vnet hosts the application. The app-vnet virtual network requires two subnets. The frontend subnet hosts the web servers. The backend subnet hosts the database servers.
- The hub-vnet only requires a subnet for the firewall.
- The two virtual networks must be able to communicate with each other securely and privately through virtual network peering.
- Both virtual networks should be in the same region.

## Architecture diagram

![Diagram of the architecture as explained in the objectives.](https://learn.microsoft.com/en-us/training/wwl-azure/configure-virtual-networks/media/create-network-architecture.png)

# Exercise 01: Create and configure virtual networks

## Scenario

Your organization is migrating a web-based application to Azure. Your first task is to put in place the virtual networks and subnets. You also need to securely peer the virtual networks. You identify these requirements.

- Two virtual networks are required, **app-vnet** and **hub-vnet**. This simulates a hub and spoke network architecture.
- The app-vnet will host the application. This virtual network requires two subnets. The **frontend subnet** will host the web servers. The **backend subnet** will host the database servers.
- The hub-vnet only requires a subnet for the firewall.
- The two virtual networks must be able to communicate with each other securely and privately through **virtual network peering**.
- Both virtual networks should be in the same region.

## Skilling tasks

- Create a virtual network.
- Create a subnet.
- Configure vnet peering.

## Architecture diagram

[![Diagram that shows two virtual networks that are peered.](https://microsoftlearning.github.io/Configure-secure-access-to-workloads-with-Azure-virtual-networking-services/Instructions/Media/task-1.png)](https://microsoftlearning.github.io/Configure-secure-access-to-workloads-with-Azure-virtual-networking-services/Instructions/Media/task-1.png)

## Estimated timing: 20 minutes

## Exercise instructions

**Note**: To complete this lab you will need an [Azure subscription](https://azure.microsoft.com/free/) with **Contributor** RBAC role assigned. In this lab, when you are asked to create a resource, for any properties that are not specified, use the default value.

## Create hub and spoke virtual networks and subnets

An [Azure virtual network](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview) enables many types of Azure resources to securely communicate with each other, the internet, and on-premises networks. All Azure resources in a virtual network are deployed into [subnets](https://learn.microsoft.com/azure/virtual-network/virtual-network-manage-subnet?tabs=azure-portal) within the virtual network.

1. Sign in to the **Azure portal** - `https://portal.azure.com`.
    
2. Search for and select `Virtual Networks`.
    
3. Select **+ Create** and complete the configuration of the **app-vnet**. This virtual network requires two subnets, **frontend** and **backend**.
    
    |Property|Value|
    |---|---|
    |Resource group|**RG1**|
    |Virtual network name|`app-vnet`|
    |Region|**East US**|
    |IPv4 address space|**10.1.0.0/16**|
    |Subnet name|`frontend`|
    |Subnet address range|**10.1.0.0/24**|
    |Subnet name|`backend`|
    |Subnet address range|**10.1.1.0/24**|
    
    **Note**:Leave all other settings as their defaults. When finished select **“Review + create** and then **Create**.
    
4. Create the **Hub-vnet** virtual network configuration. This virtual network has the firewall subnet.
    
    |Property|Value|
    |---|---|
    |Resource group|**RG1**|
    |Name|`hub-vnet`|
    |Region|**East US**|
    |IPv4 address space|**10.0.0.0/16**|
    |Subnet name|**AzureFirewallSubnet**|
    |Subnet address range|**10.0.0.0/26**|
    
5. Once the deployments are complete, search for and select your ‘virtual networks`.
    
6. Verify your virtual networks and subnets were deployed.
    

## Configure a peer relationship between the virtual networks

[Virtual network peering](https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview) enables you to seamlessly connect two or more Virtual Networks in Azure.

1. Search for and select the `app-vnet` virtual network.
    
2. In the **Settings** blade, select **Peerings**.
    
3. **+ Add** a peering between the two virtual networks.
    
    |Property|Value|
    |---|---|
    |Remote peering link name|`app-vnet-to-hub`|
    |Virtual network|`hub-vnet`|
    |Local virtual network peering link name|`hub-to-app-vnet`|
    
    **Note**: Leave all other settings as their defaults. Select **“Add”** to create the virtual network peering.
    
4. Once the deployment completes, verify the **Peering status** is **Connected**.
    

## Learn more with online training

- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/training/modules/introduction-to-azure-virtual-networks/). In this module, you learn how to design and implement Azure networking services. You learn about virtual networks, public and private IPs, DNS, virtual network peering, routing, and Azure Virtual NAT.

## Key takeaways

Congratulations on completing the exercise. Here are the main takeaways:

- Azure virtual networks (VNets) provide a secure and isolated network environment for your cloud resources. You can create multiple virtual networks per region per subscription.
- When designing virtual networks make sure the VNet address space (CIDR block) doesn’t overlap with your organization’s other network ranges.
- A subnet is a range of IP addresses in the VNet. You can segment VNets into different size subnets, creating as many subnets as you require for organization and security within the subscription limit. Each subnet must have a unique address range.
- Certain Azure services, such as Azure Firewall, require their own subnet.
- Virtual network peering enables you to seamlessly connect two Azure virtual networks. The virtual networks appear as one for connectivity purposes.

# M01 - Unit 4 Design and implement a Virtual Network in Azure

## Exercise scenario

Consider the fictional organization Contoso Ltd, which is in the process of migrating infrastructure and applications to Azure. In your role as network engineer, you must plan and implement three virtual networks and subnets to support resources in those virtual networks.

The **CoreServicesVnet** virtual network is deployed in the **East US** region. This virtual network will have the largest number of resources. It will have connectivity to on-premises networks through a VPN connection. This network will have web services, databases, and other systems that are key to the operations of the business. Shared services, such as domain controllers and DNS also will be located here. A large amount of growth is anticipated, so a large address space is necessary for this virtual network.

The **ManufacturingVnet** virtual network is deployed in the **West Europe** region, near the location of your organization’s manufacturing facilities. This virtual network will contain systems for the operations of the manufacturing facilities. The organization is anticipating a large number of internal connected devices for their systems to retrieve data from, such as temperature, and will need an IP address space that it can expand into.

The **ResearchVnet** virtual network is deployed in the **Southeast Asia** region, near the location of the organization’s research and development team. The research and development team uses this virtual network. The team has a small, stable set of resources that is not expected to grow. The team needs a small number of IP addresses for a few virtual machines for their work.

[![Network layout for Contoso.
On-premises 10.10.0.0/16
ResearchVNet Southeast Asia 10.40.40.0/24
CoreServicesVNet East US 10.20.0.0/16
ManufacturingVNet West Europe 10.30.0.0/16](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/design-implement-vnet-peering.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/design-implement-vnet-peering.png)

You will create the following resources:

|**Virtual Network**|**Region**|**Virtual network address space**|**Subnet**|**Subnet**|
|---|---|---|---|---|
|CoreServicesVnet|East US|10.20.0.0/16|||
||||GatewaySubnet|10.20.0.0/27|
||||SharedServicesSubnet|10.20.10.0/24|
||||DatabaseSubnet|10.20.20.0/24|
||||PublicWebServiceSubnet|10.20.30.0/24|
|ManufacturingVnet|West Europe|10.30.0.0/16|||
||||ManufacturingSystemSubnet|10.30.10.0/24|
||||SensorSubnet1|10.30.20.0/24|
||||SensorSubnet2|10.30.21.0/24|
||||SensorSubnet3|10.30.22.0/24|
|ResearchVnet|Southeast Asia|10.40.0.0/16|||
||||ResearchSystemSubnet|10.40.0.0/24|

These virtual networks and subnets are structured in a way that accommodates existing resources yet allows for projected growth. Let’s create these virtual networks and subnets to lay the foundation for our networking infrastructure.

## Estimated time: 20 minutes

## Job skills

In this exercise, you will:

- Task 1: Create the Contoso resource group
- Task 2: Create the CoreServicesVnet virtual network and subnets
- Task 3: Create the ManufacturingVnet virtual network and subnets
- Task 4: Create the ResearchVnet virtual network and subnets
- Task 5: Verify the creation of VNets and Subnets

## Task 1: Create the Contoso resource group

1. Go to [Azure portal](https://portal.azure.com/).
    
2. On the home page, under **Azure services**, select **Resource groups**.
    
3. In the Resource groups, select **+ Create**.
    
4. Use the information in the following table to create the resource group.
    
    |**Tab**|**Option**|**Value**|
    |---|---|---|
    |Basics|Resource group|ContosoResourceGroup|
    ||Region|(US) East US|
    |Tags|No changes required||
    |Review + create|Review your settings and select **Create**||
    
5. In Resource groups, verify that **ContosoResourceGroup** appears in the list.
    

## Task 2: Create the CoreServicesVnet virtual network and subnets

1. On the Azure portal home page, navigate to the Global Search bar and search **Virtual Networks** and select virtual networks under services. [![Azure portal home page Global Search bar results for virtual network.](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/global-search-bar.PNG)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/global-search-bar.PNG)
    
2. Select **Create** on the Virtual networks page. [![Create a virtual network wizard.](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/create-virtual-network.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/create-virtual-network.png)
    
3. Use the information in the following table to create the CoreServicesVnet virtual network.  
    Remove or overwrite the default IP Address space. [![IP address configuration for Azure virtual network deployment](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/default-vnet-ip-address-range-annotated.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/default-vnet-ip-address-range-annotated.png)
    
    |**Tab**|**Option**|**Value**|
    |---|---|---|
    |Basics|Resource Group|ContosoResourceGroup|
    ||Name|CoreServicesVnet|
    ||Region|(US) East US|
    |IP Addresses|IPv4 address space|10.20.0.0/16|
    
4. Use the information in the following table to create the CoreServicesVnet subnets.
    
5. To begin creating each subnet, select **+ Add subnet**. To finish creating each subnet, select **Add**. If needed, **Edit** (pencil icon) or **Delete** the default subnet.
    
    |**Subnet**|**Option**|**Value**|
    |---|---|---|
    |GatewaySubnet|Subnet purpose|Virtual Network Gateway|
    ||Subnet name|GatewaySubnet|
    ||Subnet address range|10.20.0.0/27|
    |SharedServicesSubnet|Subnet name|SharedServicesSubnet|
    ||Subnet address range|10.20.10.0/24|
    |DatabaseSubnet|Subnet name|DatabaseSubnet|
    ||Subnet address range|10.20.20.0/24|
    |PublicWebServiceSubnet|Subnet name|PublicWebServiceSubnet|
    ||Subnet address range|10.20.30.0/24|
    
6. To finish creating the CoreServicesVnet and its associated subnets, select **Review + create**.
    
7. Verify your configuration passed validation, and then select **Create**.
    
8. Repeat steps 1 -8 for each VNet based on the tables below
    

## Task 3: Create the ManufacturingVnet virtual network and subnets

|**Tab**|**Option**|**Value**|
|---|---|---|
|Basics|Resource Group|ContosoResourceGroup|
||Name|ManufacturingVnet|
||Region|(Europe) West Europe|
|IP Addresses|IPv4 address space|10.30.0.0/16|

|**Subnet**|**Option**|**Value**|
|---|---|---|
|ManufacturingSystemSubnet|Subnet name|ManufacturingSystemSubnet|
||Subnet address range|10.30.10.0/24|
|SensorSubnet1|Subnet name|SensorSubnet1|
||Subnet address range|10.30.20.0/24|
|SensorSubnet2|Subnet name|SensorSubnet2|
||Subnet address range|10.30.21.0/24|
|SensorSubnet3|Subnet name|SensorSubnet3|
||Subnet address range|10.30.22.0/24|

## Task 4: Create the ResearchVnet virtual network and subnets

|**Tab**|**Option**|**Value**|
|---|---|---|
|Basics|Resource Group|ContosoResourceGroup|
||Name|ResearchVnet|
||Region|Southeast Asia|
|IP Addresses|IPv4 address space|10.40.0.0/16|

|**Subnet**|**Option**|**Value**|
|---|---|---|
|ResearchSystemSubnet|Subnet name|ResearchSystemSubnet|
||Subnet address range|10.40.0.0/24|

## Task 5: Verify the creation of VNets and Subnets

1. On the Azure portal home page, select **All resources**.
    
2. Verify that the CoreServicesVnet, ManufacturingVnet, and ResearchVnet are listed.
    
3. Select **CoreServicesVnet**.
    
4. In CoreServicesVnet, under **Settings**, select **Subnets**.
    
5. In CoreServicesVnet | Subnets, verify that the subnets you created are listed, and that the IP address ranges are correct.
    
    [![List of subnets in CoreServicesVnet.](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/verify-subnets-annotated.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/verify-subnets-annotated.png)
    
6. Repeat steps 3 - 5 for each VNet.
    

## Extend your learning with Copilot

Copilot can assist you in learning how to use the Azure scripting tools. Copilot can also assist in areas not covered in the lab or where you need more information. Open an Edge browser and choose Copilot (top right) or navigate to _copilot.microsoft.com_. Take a few minutes to try these prompts.

- Can you provide an example of how the 10.30.0.0/16 IP address is used in a real-world scenario?
- What is the Azure PowerShell command to create a virtual network called CoreServicesVnet in the East (US) region. The virtual network should use the 10.20.0.0/16 IP address space.
- What is the Azure CLI command to create a virtual network called ManufacturingVnet in the West Europe region. The virtual network should use the 10.30.0.0/16 IP address space.

## Learn more with self-paced training

- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/training/modules/introduction-to-azure-virtual-networks/). In this module, you learn how to design and implement Azure networking services. You learn about virtual networks, public and private IPs, DNS, virtual network peering, routing, and Azure Virtual NAT.
- [Configure Virtual Networks](https://learn.microsoft.com/training/modules/configure-virtual-networks/). Learn to configure virtual networks and subnets, including IP addressing.

## Key takeaways

- Azure Virtual Network is a service that provides the fundamental building block for your private network in Azure. An instance of the service (a virtual network) enables many types of Azure resources to securely communicate with each other, the internet, and on-premises networks. Ensure nonoverlapping address spaces. Make sure your virtual network address space (CIDR block) doesn’t overlap with your organization’s other network ranges.
- All Azure resources in a virtual network are deployed into subnets within the virtual network. Subnets enable you to segment the virtual network into one or more subnetworks and allocate a portion of the virtual network’s address space to each subnet. Your subnets shouldn’t cover the entire address space of the virtual network. Plan ahead and reserve some address space for the future.