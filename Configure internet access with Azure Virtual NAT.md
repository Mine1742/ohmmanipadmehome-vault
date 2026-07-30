#az104 #azure 
[Azure NAT Gateway](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview) is a fully managed Network Address Translation (NAT) service that provides secure, scalable outbound connectivity from a subnet to the internet. NAT Gateway is the recommended method for outbound connectivity in Azure.

### NAT Gateway SKUs

Azure NAT gateway is available in two SKUs.

|Feature|Standard|StandardV2|
|---|---|---|
|Availability zone|Zonal (single zone)|Zone-redundant (all zones)|
|IPv6 support|No|Yes|
|Maximum throughput|50 Gbps|100 Gbps|
|Flow logs|No|Yes|

### NAT Gateway usage scenario

The following diagram shows outbound traffic flow from Subnet 1 through the NAT gateway to be mapped to a Public IP address or a Public IP prefix.

![Diagram with NAT service providing internet connectivity for internal resources.](https://learn.microsoft.com/en-us/training/wwl-azure/introduction-to-azure-virtual-networks/media/nat-flow-map-e4870a4e.png)

After NAT is configured, all UDP and TCP outbound flows from any virtual machine instance will use NAT for internet connectivity. No further configuration is necessary, and you don’t need to create any user-defined routes. NAT takes precedence over other outbound scenarios and replaces the default Internet destination of a subnet.

NAT scales automatically to support dynamic workloads. NAT can support up to 16 public IP addresses. By using port network address translation (PNAT or PAT), NAT provides up to 64,000 concurrent flows for UDP and TCP.

### Considerations for NAT Gateway

- Standard NAT gateway supports IPv4 only.
- StandardV2 NAT gateway supports both IPv4 and IPv6 public IP addresses and prefixes.
- NAT can't span multiple virtual networks.

## Check your knowledge

1. 

What is the purpose of NAT?

NAT enables you to share a single public IPv4 address among multiple internal resources.

NAT allows you to assign multiple private IPv4 addresses to a single virtual machine.

NAT enables you to configure an external IPv4 address on each individual virtual machine.

2. 

How does NAT scale to support dynamic workloads?

NAT supports up to four public IP addresses.

NAT doesn't scale dynamically. You must configure NAT to scale manually, by adding other NAT Gateways.

NAT supports up to 16 public IP addresses, and for each of address, uses port network address translation (PNAT or PAT) to provide up to 64,000 concurrent traffic flows.