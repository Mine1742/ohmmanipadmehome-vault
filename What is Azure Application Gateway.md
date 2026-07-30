#az104 #azure 
Azure Application Gateway is an Azure service that processes traffic to web apps that are hosted on a pool of web servers. The processing performed by Azure Application Gateway includes load balancing HTTP traffic and inspecting traffic using web application firewall. It also includes encrypting traffic between users and an application gateway, and encrypting traffic between application servers and an application gateway.

Adatum is a new and expanding online commerce store that sells industrial drones. You're responsible for networking at the company. Adatum has several web applications that are hosted on computers in its on-premises datacenter. At the moment, a special but aging hardware device is deployed on the Adatum perimeter network that manages traffic to the web applications hosted on these computers. You want to retire this device and have traffic mediated by an Azure service.

To meet your goals, you need to ensure that the Azure service replicates the functionality that the special hardware currently provides. Important functionality that must be present in the replacement service includes:

- Detect if one of the on-premises servers becomes unavailable so that traffic is no longer directed to it.
- TLS (Transport Layer Security) termination functionality to reduce the amount of CPU capacity consumed by encryption and decryption operations.
- Session affinity to ensure that the same back-end pool host always serves a client connection to a web application.
- Security filtering of malicious traffic such as SQL injection and cross site scripting attacks.

Azure Application Gateway manages the requests that client applications send to web apps that are hosted on a pool of web servers. The pool of web servers can be Azure virtual machines, Azure Virtual Machine Scale Sets, Azure App Service, and even on-premises servers.

Application Gateway provides features such as load balancing HTTP traffic and web application firewall. It provides support for TLS/SSL encryption of traffic between users and an application gateway and between application servers and an application gateway.

![Diagram that depicts the Azure Application Gateway topology.](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-application-gateway/images/application-gateway-topology.png)

Application Gateway uses a round-robin process to load balance requests to the servers in each back-end pool. Session stickiness ensures client requests in the same session are routed to the same back-end server. Session stickiness is especially important with e-commerce applications where you don’t want a transaction to be disrupted because the load balancer bounces it around between back-end servers.

Azure Application Gateway includes the following features:

- Support for the HTTP, HTTPS, HTTP/2, and WebSocket protocols.
- A web application firewall to protect against web application vulnerabilities.
- End-to-end request encryption.
- Autoscaling to dynamically adjust capacity as your web traffic load change.
- Connection draining allowing graceful removal of back-end pool members during planned service updates.