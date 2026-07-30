Organizations with large scale operations create connections between different parts of their virtual network infrastructure. Virtual network peering enables you to seamlessly connect separate VNets with optimal network performance, whether they are in the same Azure region (VNet peering) or in different regions (Global VNet peering).

Network traffic between peered virtual networks is private. The virtual networks appear as one for connectivity purposes. The traffic between virtual machines in peered virtual networks uses the Microsoft backbone infrastructure, and no public Internet, gateways, or encryption is required in the communication between the virtual networks.

Virtual network peering enables you to seamlessly connect two Azure virtual networks. Once peered, the virtual networks appear as one, for connectivity purposes. There are two types of VNet peering.

![Diagram with VNet1 in Region 1, and VNet2 and VNet3 in Region 2. VNet2 and VNet3 are connected with regional VNet peering. VNet1 and VNet2 are connected with a global VNet peering.](https://learn.microsoft.com/en-us/training/wwl-azure/introduction-to-azure-virtual-networks/media/global-vnet-peering-2368962c.png)

- **Regional VNet peering** connects Azure virtual networks in the same region.
- **Global VNet peering** connects Azure virtual networks in different regions.

 Tip

Azure also supports [subnet peering](https://learn.microsoft.com/en-us/azure/virtual-network/how-to-configure-subnet-peering), a more granular peering option. Subnet peering lets you select specific subnets to peer across virtual networks rather than peering entire address spaces.

### Benefits of virtual network peering

The benefits of using virtual network peering, whether local or global, include:

- A low-latency, high-bandwidth connection between resources in different virtual networks.
- The ability to apply network security groups in either virtual network to block access to other virtual networks or subnets.
- The ability to transfer data between virtual networks across Azure subscriptions, Microsoft Entra tenants, deployment models, and Azure regions.
- The ability to peer virtual networks created through the Azure Resource Manager.
- No downtime to resources in either virtual network is required when creating the peering, or after the peering is created.

### Gateway Transit and Connectivity

You can configure a VPN gateway in the peered virtual network as a [gateway transit](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-peering-gateway-transit) point. In this case, a peered virtual network uses the remote gateway to gain access to other resources. A virtual network can have only one gateway. Gateway transit is supported for both VNet Peering and Global VNet Peering.

For example, the subnet gateway could:

- Use a site-to-site VPN to connect to an on-premises network.
- Use a VNet-to-VNet connection to another virtual network.
- Use a point-to-site VPN to connect to a client.

In these scenarios, gateway transit allows peered virtual networks to share the gateway and get access to resources. This means you don't need to deploy a VPN gateway in the peer virtual network.

![Screenshot of virtual network peering configuration page.](https://learn.microsoft.com/en-us/training/wwl-azure/introduction-to-azure-virtual-networks/media/configure-vnet-peering.png)

 Note

Network security groups can be applied in either virtual network to block access to other virtual networks or subnets.

Choose the best response for each question.

## Check your knowledge

1. 

Which feature allows one VNet to communicate with resources in a subnet in a different virtual network?

Internal Domain Name System (DNS).

Azure Availability Zones.

VNet peering.