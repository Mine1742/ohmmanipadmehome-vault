#az104 #azure 
In the next stage of your security implementation, you'll deploy a network virtual appliance (NVA) to secure and monitor traffic between your front-end public servers and internal private servers.

First, configure the appliance to forward IP traffic. If IP forwarding isn't enabled, traffic that is routed through your appliance will never be received by its intended destination servers.

In this exercise, you deploy the **nva** network appliance to the **dmzsubnet** subnet. Then you enable IP forwarding so that traffic from **`*`** and traffic that uses the custom route is sent to the **privatesubnet** subnet.

![Diagram of a Network virtual appliance with IP forwarding enabled.](https://learn.microsoft.com/en-us/training/modules/control-network-traffic-flow-with-routes/media/5-nva-ip-forwarding.svg)

In the following steps, you'll deploy an NVA. You'll then update the Azure virtual NIC and the network settings within the appliance to enable IP forwarding.

 Note

This exercise is optional. If you want to complete this exercise, you'll need to create an Azure subscription before you begin. If you don't have an Azure account or you don't want to create one at this time, you can read through the instructions so you understand the information that's being presented.

## Deploy the network virtual appliance

To build the NVA, deploy an Ubuntu LTS instance.

1. In [Azure Cloud Shell](https://shell.azure.com/), run the following command to deploy the appliance. Replace `<password>` with a suitable password of your choice for the **azureuser** admin account, and **myResourceGroupName** with the name of your resource group.
    
    Azure CLI
    
    ```
    az vm create \
        --resource-group "myResourceGroupName" \
        --name nva \
        --vnet-name vnet \
        --subnet dmzsubnet \
        --image Ubuntu2204 \
        --admin-username azureuser \
        --admin-password <password>
    ```
    

## Enable IP forwarding for the Azure network interface

In the next steps, you enable IP forwarding for the **nva** network appliance. When traffic flows to the NVA but is meant for another target, the NVA will route that traffic to its correct destination.

1. Run the following command to get the NVA network interface's ID:
    
    Azure CLI
    
    ```
    NICID=$(az vm nic list \
        --resource-group "myResourceGroupName" \
        --vm-name nva \
        --query "[].{id:id}" --output tsv)
    
    echo $NICID
    ```
    
2. Run the following command to get the NVA network interface's name:
    
    Azure CLI
    
    ```
    NICNAME=$(az vm nic show \
        --resource-group "myResourceGroupName" \
        --vm-name nva \
        --nic $NICID \
        --query "{name:name}" --output tsv)
    
    echo $NICNAME
    ```
    
3. Run the following command to enable IP forwarding for the network interface:
    
    Azure CLI
    
    ```
    az network nic update --name $NICNAME \
        --resource-group "myResourceGroupName" \
        --ip-forwarding true
    ```
    

## Enable IP forwarding in the appliance

1. Run the following command to save the NVA virtual machine's public IP address to the variable `NVAIP`:
    
    Azure CLI
    
    ```
    NVAIP="$(az vm list-ip-addresses \
        --resource-group "myResourceGroupName" \
        --name nva \
        --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
        --output tsv)"
    
    echo $NVAIP
    ```
    
2. Run the following command to enable IP forwarding within the NVA:
    
    Bash
    
    ```
    ssh -t -o StrictHostKeyChecking=no azureuser@$NVAIP 'sudo sysctl -w net.ipv4.ip_forward=1; exit;'
    ```
    
    When prompted, enter the password you used when you created the virtual machine.