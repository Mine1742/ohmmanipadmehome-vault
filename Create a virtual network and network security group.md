
First, you'll create the virtual network and subnets for your server resources. You'll then create a network security group.

1. Open the [Azure Cloud Shell](https://shell.azure.com/) and run the following command to assign the name of you resource group to the variable `rg`. Replace **myResourceGroupName** with the name of your resource group.
    
    Azure CLI
    
    ```
    rg="myResourceGroupName"
    ```
    
2. To create the **ERP-servers** virtual network and the **Applications** subnet, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network vnet create \
        --resource-group $rg \
        --name ERP-servers \
        --address-prefixes 10.0.0.0/16 \
        --subnet-name Applications \
        --subnet-prefixes 10.0.0.0/24
    ```
    
3. To create the **Databases** subnet, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network vnet subnet create \
        --resource-group $rg \
        --vnet-name ERP-servers \
        --address-prefixes 10.0.1.0/24 \
        --name Databases
    ```
    
4. To create the **ERP-SERVERS-NSG** network security group, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network nsg create \
        --resource-group $rg \
        --name ERP-SERVERS-NSG
    ```
    

## Create VMs running Ubuntu

Next, you'll create two VMs called **AppServer** and **DataServer**. You deploy **AppServer** to the **Applications** subnet, and **DataServer** to the **Databases** subnet. Add the VM network interfaces to the **ERP-SERVERS-NSG** network security group. Then, to test your network security group, use these VMs.

1. To build the **AppServer** VM, run the following command in Cloud Shell. For the admin account, replace `<password>` with a complex password.
    
    Azure CLI
    
    ```
    wget -N https://raw.githubusercontent.com/MicrosoftDocs/mslearn-secure-and-isolate-with-nsg-and-service-endpoints/master/cloud-init.yml && \
    az vm create \
        --resource-group $rg \
        --name AppServer \
        --vnet-name ERP-servers \
        --subnet Applications \
        --nsg ERP-SERVERS-NSG \
        --image Ubuntu2204 \
        --size Standard_DS1_v2 \
         --generate-ssh-keys \
        --admin-username azureuser \
        --custom-data cloud-init.yml \
        --no-wait \
        --admin-password <password>
    ```
    
2. To build the **DataServer** VM, run the following command in Cloud Shell. For the admin account, replace `<password>` with a complex password.
    
    Azure CLI
    
    ```
    az vm create \
        --resource-group $rg \
        --name DataServer \
        --vnet-name ERP-servers \
        --subnet Databases \
        --nsg ERP-SERVERS-NSG \
        --size Standard_DS1_v2 \
        --image Ubuntu2204 \
        --generate-ssh-keys \
        --admin-username azureuser \
        --custom-data cloud-init.yml \
         --no-wait \
        --admin-password <password>
    ```
    
3. It can take several minutes for the VMs to be in a running state. To confirm that the VMs are running, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az vm list \
        --resource-group $rg \
        --show-details \
        --query "[*].{Name:name, Provisioned:provisioningState, Power:powerState}" \
        --output table
    ```
    
    When your VM creation is complete, you should see the following output:
    
    Output
    
    ```
    Name        Provisioned    Power
    ----------  -------------  ----------
    AppServer   Succeeded      VM running
    DataServer  Succeeded      VM running
    ```
    

## Check default connectivity

Now, you'll try to open a Secure Shell (SSH) session to each of your VMs. Remember, so far you've deployed a network security group with default rules.

1. To connect to your VMs, use SSH directly from Cloud Shell. To do this, you need the public IP addresses that have been assigned to your VMs. To list the IP addresses that you'll use to connect to the VMs, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az vm list \
        --resource-group $rg \
        --show-details \
        --query "[*].{Name:name, PrivateIP:privateIps, PublicIP:publicIps}" \
        --output table
    ```
    
2. To make it easier to connect to your VMs during the rest of this exercise, assign the public IP addresses to variables. To save the public IP address of **AppServer** and **DataServer** to a variable, run the following command in Cloud Shell:
    
    Bash
    
    ```
    APPSERVERIP="$(az vm list-ip-addresses \
                     --resource-group $rg \
                     --name AppServer \
                     --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
                     --output tsv)"
    
    DATASERVERIP="$(az vm list-ip-addresses \
                     --resource-group $rg \
                     --name DataServer \
                     --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
                     --output tsv)"
    ```
    
3. To check whether you can connect to your **AppServer** VM, run the following command in Cloud Shell:
    
    Bash
    
    ```
    ssh azureuser@$APPSERVERIP -o ConnectTimeout=5
    ```
    
    You'll get a `Connection timed out` message.
    
4. To check whether you can connect to your **DataServer** VM, run the following command in Cloud Shell:
    
    Bash
    
    ```
    ssh azureuser@$DATASERVERIP -o ConnectTimeout=5
    ```
    
    You'll get the same connection failure message.
    

Remember that the default rules deny all inbound traffic into a virtual network, unless this traffic is coming from the same virtual network. The **Deny All Inbound** rule blocked the inbound SSH connections you just attempted.

**Inbound**

|Name|Priority|Source IP|Destination IP|Access|
|---|---|---|---|---|
|Allow VNet Inbound|65000|VIRTUAL_NETWORK|VIRTUAL_NETWORK|Allow|
|Deny All Inbound|65500|*|*|Deny|

## Create a security rule for SSH

As you've now experienced, the default rules in your **ERP-SERVERS-NSG** network security group include a **Deny All Inbound** rule. You'll now add a rule so that you can use SSH to connect to **AppServer** and **DataServer**.

1. To create a new inbound security rule to enable SSH access, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network nsg rule create \
        --resource-group $rg \
        --nsg-name ERP-SERVERS-NSG \
        --name AllowSSHRule \
        --direction Inbound \
        --priority 100 \
        --source-address-prefixes '*' \
        --source-port-ranges '*' \
        --destination-address-prefixes '*' \
        --destination-port-ranges 22 \
        --access Allow \
        --protocol Tcp \
        --description "Allow inbound SSH"
    ```
    
2. To check whether you can now connect to your **AppServer** VM, run the following command in Cloud Shell:
    
    Bash
    
    ```
    ssh azureuser@$APPSERVERIP -o ConnectTimeout=5
    ```
    
    The network security group rule might take a minute or two to take effect. If you receive a connection failure message, wait a moment and try again.
    
3. You should now be able to connect. After the `Are you sure you want to continue connecting (yes/no)?` message, enter `yes`.
    
4. Enter the password you defined when you created the VM.
    
5. To close the **AppServer** session, enter `exit`.
    
6. To check whether you can now connect to your **DataServer** VM, run the following command in Cloud Shell:
    
    Bash
    
    ```
    ssh azureuser@$DATASERVERIP -o ConnectTimeout=5
    ```
    
7. You should now be able to connect. After the `Are you sure you want to continue connecting (yes/no)?` message, enter `yes`.
    
8. Enter the password you defined when you created the VM.
    
9. To close the **DataServer** session, enter `exit`.
    

## Create a security rule to prevent web access

Now, add a rule so that **AppServer** can communicate with **DataServer** over HTTP, but **DataServer** can't communicate with **AppServer** over HTTP. These are the internal IP addresses for these servers:

|Server name|IP address|
|---|---|
|AppServer|10.0.0.4|
|DataServer|10.0.1.4|

1. To create a new inbound security rule to deny HTTP access over port 80, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network nsg rule create \
        --resource-group $rg \
        --nsg-name ERP-SERVERS-NSG \
        --name httpRule \
        --direction Inbound \
        --priority 150 \
        --source-address-prefixes 10.0.1.4 \
        --source-port-ranges '*' \
        --destination-address-prefixes 10.0.0.4 \
        --destination-port-ranges 80 \
        --access Deny \
        --protocol Tcp \
        --description "Deny from DataServer to AppServer on port 80"
    ```
    

## Test HTTP connectivity between virtual machines

Here, you'll check if your new rule works. **AppServer** should be able to communicate with **DataServer** over HTTP. **DataServer** shouldn't be able to communicate with **AppServer** over HTTP.

1. To connect to your **AppServer** VM, in Cloud Shell, run the following command. Check if **AppServer** can communicate with **DataServer** over HTTP.
    
    Bash
    
    ```
    ssh -t azureuser@$APPSERVERIP 'wget http://10.0.1.4; exit; bash'
    ```
    
2. Enter the password you defined when you created the VM.
    
3. The response should include a `200 OK` message.
    
4. To connect to your **DataServer** VM, in Cloud Shell, run the following command. Check if **DataServer** can communicate with **AppServer** over HTTP.
    
    Bash
    
    ```
    ssh -t azureuser@$DATASERVERIP 'wget http://10.0.0.4; exit; bash'
    ```
    
5. Enter the password you defined when you created the VM.
    
6. This shouldn't succeed, because you've blocked access over port 80. After several minutes, you should get a `Connection timed out` message. To stop the command before the timeout, select **Ctrl+C**.
    

## Deploy an app security group

Next, create an app security group for database servers so that all servers in this group can be assigned the same settings. You're planning to deploy more database servers, and want to prevent these servers from accessing app servers over HTTP. By assigning sources in the app security group, you don't need to manually maintain a list of IP addresses in the network security group. Instead, you assign the network interfaces of the VMs you want to manage to the app security group.

![Diagram of exercise scenario app security groups.](https://learn.microsoft.com/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/media/3-exercise-second-task.svg)

1. To create a new app security group called **ERP-DB-SERVERS-ASG**, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network asg create \
        --resource-group $rg \
        --name ERP-DB-SERVERS-ASG
    ```
    
2. To associate **DataServer** with the app security group, run the following command in Cloud Shell:
    
    Azure CLI
    
    ```
    az network nic ip-config update \
        --resource-group $rg \
        --application-security-groups ERP-DB-SERVERS-ASG \
        --name ipconfigDataServer \
        --nic-name DataServerVMNic \
        --vnet-name ERP-servers \
        --subnet Databases
    ```
    
3. To update the HTTP rule in the **ERP-SERVERS-NSG** network security group, run the following command in Cloud Shell. It should reference the **ERP-DB-Servers** app security group.
    
    Azure CLI
    
    ```
    az network nsg rule update \
        --resource-group $rg \
        --nsg-name ERP-SERVERS-NSG \
        --name httpRule \
        --direction Inbound \
        --priority 150 \
        --source-address-prefixes "" \
        --source-port-ranges '*' \
        --source-asgs ERP-DB-SERVERS-ASG \
        --destination-address-prefixes 10.0.0.4 \
        --destination-port-ranges 80 \
        --access Deny \
        --protocol Tcp \
        --description "Deny from DataServer to AppServer on port 80 using application security group"
    ```
    

## Test the updated HTTP security rule

1. To connect to your **AppServer** VM, run the following command in Cloud Shell. Check if **AppServer** can communicate with **DataServer** over HTTP.
    
    Bash
    
    ```
    ssh -t azureuser@$APPSERVERIP 'wget http://10.0.1.4; exit; bash'
    ```
    
2. Enter the password you defined when you created the VM.
    
3. As before, the response should include a `200 OK` message. The app security group settings can take a minute or two to take effect. If you don't initially receive the `200 OK` message, wait a minute and try again.
    
4. To connect to your **DataServer**, run the following command in Cloud Shell. Check if **DataServer** can communicate with **AppServer** over HTTP.
    
    Bash
    
    ```
    ssh -t azureuser@$DATASERVERIP 'wget http://10.0.0.4; exit; bash'
    ```
    
5. Enter the password you defined when you created the VM.
    
6. As before, this shouldn't succeed, because you've blocked access over port 80. After several minutes, you should get a `Connection timed out` message. To stop the command before the timeout, select **Ctrl+C**.
    

You've now confirmed that your network security group rule works using an app security group in the same way as when you used a source IP address. If we added additional data servers, we could easily ensure they have the proper network security by adding the new servers to the **ERP-DB-SERVERS-ASG**.