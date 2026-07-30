# 

## Exercise scenario

In this unit, you will configure connectivity between the CoreServicesVnet and the ManufacturingVnet by adding peerings to allow traffic flow.

[![Diagram of virtual network peering.](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/8-exercise-connect-two-azure-virtual-networks-global.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/8-exercise-connect-two-azure-virtual-networks-global.png)

## Estimated time: 20 minutes

## Job skills

In this exercise, you:

- Task 1: Create a Virtual Machine to test the configuration
- Task 2: Connect to the Test VMs using RDP
- Task 3: Test the connection between the VMs
- Task 4: Create VNet peerings between CoreServicesVnet and ManufacturingVnet
- Task 5: Test the connection between the VMs

## Task 1: Create a Virtual Machine to test the configuration

In this section, you will create a test VM on the VNet to test if you can access resources inside another Azure virtual network from your Vnet.

### Create ManufacturingVM

1. In the Azure portal, select the Cloud Shell icon (top right). If necessary, configure the shell.
    - Select **PowerShell**.
    - Select **No Storage Account required** and your **Subscription**, then select **Apply**.
    - Wait for the terminal to create and a prompt to be displayed.
2. On the toolbar of the Cloud Shell pane, select the **Manage files** icon, in the drop-down menu, select **Upload** and upload the following files **ManufacturingVMazuredeploy.json** and **ManufacturingVMazuredeploy.parameters.json**.
    
    > **Note:** If you are working in your own subscription the [template files](https://github.com/MicrosoftLearning/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/tree/master/Allfiles/Exercises) are available in the GitHub lab repository.
    
3. Deploy the following ARM templates to create the VMs needed for this exercise:
    
    > **Note**: You will be prompted to provide an Admin password.
    
    code
    
    ```powershell
    $RGName = "ContosoResourceGroup"
       
    New-AzResourceGroupDeployment -ResourceGroupName $RGName -TemplateFile ManufacturingVMazuredeploy.json -TemplateParameterFile ManufacturingVMazuredeploy.parameters.json
    ```
    
4. When the deployment is complete, go to the Azure portal home page, and then select **Virtual Machines**.
    
5. Verify that the virtual machine has been created.

## Task 2: Connect to the Test VMs using RDP

1. On the Azure Portal home page, select **Virtual Machines**.
    
2. Select **ManufacturingVM**.
    
3. On ManufacturingVM, select **Connect > RDP**.
    
4. On ManufacturingVM | Connect, select **Download RDP file**.
    
5. Save the RDP file to your desktop.
    
6. Connect to ManufacturingVM using the RDP file, and the username **TestUser** and the password you provided during deployment.
    
7. On the Azure Portal home page, select **Virtual Machines**.
    
8. Select **TestVM1**.
    
9. On TestVM1, select **Connect > RDP**.
    
10. On TestVM1 | Connect, select **Download RDP file**.
    
11. Save the RDP file to your desktop.
    
12. Connect to TestVM1 using the RDP file, and the username **TestUser** and the password you provided during deployment.
    
13. On both VMs, in **Choose privacy settings for your device**, select **Accept**.
    
14. On both VMs, in **Networks**, select **Yes**.
    
15. On TestVM1, open a PowerShell prompt, and run the following command: ipconfig
    
16. Note the IPv4 address.
    

## Task 3: Test the connection between the VMs

1. On the ManufacturingVM, open a PowerShell prompt.
    
2. Use the following command to verify that there is no connection to TestVM1 on CoreServicesVnet. Be sure to use the IPv4 address for TestVM1.
    
    code
    
    ```powershell
     Test-NetConnection 10.20.20.4 -port 3389
    ```
    
3. The test connection should fail, and you will see a result similar to the following: [![PowerShell window with Test-NetConnection 10.20.20.4 -port 3389 showing failed](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/test-netconnection-fail.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/test-netconnection-fail.png)
    

## Task 4: Create VNet peerings between CoreServicesVnet and ManufacturingVnet

1. On the Azure home page, select **Virtual Networks**, and then select **CoreServicesVnet**.
    
2. In CoreServicesVnet, under **Settings**, select **Peerings**.
    
3. On CoreServicesVnet | Peerings, select **+ Add**.
    
4. Use this information to create the peering. When finished, select **Add**.
    
    **Remote virtual network summary**
    
    |**Option**|**Value**|
    |---|---|
    |Peering link name|`ManufacturingVnet-to-CoreServicesVnet`|
    |Virtual network|ManufacturingVnet|
    
    **Remote virtual network peering settings**
    
    |**Option**|**Value**|
    |---|---|
    |Allow ‘ManufacturingVnet’ to access ‘CoreServicesVnet’|Enabled|
    |‘ManufacturingVnet’ to receive forwarded traffic from ‘CoreServicesVnet’|Enabled|
    
    **Local virtual network summary**
    
    |**Option**|**Value**|
    |---|---|
    |Peering link name|`CoreServicesVnet-to-ManufacturingVnet`|
    
    **Local virtual network peering settings**
    
    |**Option**|**Value**|
    |---|---|
    |Allow ‘CoreServicesVnet’ to access ‘ManufacturingVnet’|Enabled|
    |Allow ‘CoreServicesVnet’ to receive forwarded traffic from ‘ManufacturingVnet’|Enabled|
    
5. Check the box to the left of **CoreServicesVnet-to-ManufacturingVnet** and select **Sync**
    
6. In CoreServicesVnet | Peerings, verify that the **CoreServicesVnet-to-ManufacturingVnet** peering is **Connected**.
    
7. Under Virtual networks, select **ManufacturingVnet**, and verify the **ManufacturingVnet-to-CoreServicesVnet** peering is **Connected**.
    

## Task 5: Test the connection between the VMs

1. On the ManufacturingVM, open a PowerShell prompt.
    
2. Use the following command to verify that there is now a connection to TestVM1 on CoreServicesVnet.
    
    code
    
    ```powershell
     Test-NetConnection 10.20.20.4 -port 3389
    ```
    
3. The test connection should succeed, and you will see a result similar to the following: [![Powershell window with Test-NetConnection 10.20.20.4 -port 3389 showing TCP test succeeded: true](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/test-connection-succeeded.png)](https://microsoftlearning.github.io/AZ-700-Designing-and-Implementing-Microsoft-Azure-Networking-Solutions/Instructions/media/test-connection-succeeded.png)
    

## Clean up resources

> **Note**: Remember to remove any newly created Azure resources that you no longer use. Removing unused resources ensures you will not see unexpected charges.

1. On the Azure portal, open the **PowerShell** session within the **Cloud Shell** pane. (Create Cloud Shell storage if needed, using default settings.)
    
2. Delete all resource groups you created throughout the labs of this module by running the following command:
    
    code
    
    ```powershell
    Remove-AzResourceGroup -Name 'ContosoResourceGroup' -Force -AsJob
    ```
    
    > **Note**: The command executes asynchronously (as determined by the -AsJob parameter), so while you will be able to run another PowerShell command immediately afterwards within the same PowerShell session, it will take a few minutes before the resource groups are actually removed.
    

## Extend your learning with Copilot

Copilot can assist you in learning how to use the Azure scripting tools. Copilot can also assist in areas not covered in the lab or where you need more information. Open an Edge browser and choose Copilot (top right) or navigate to _copilot.microsoft.com_. Take a few minutes to try these prompts.

- What the most common errors when configuring Azure virtual network peering?
- In Azure, if I peer Vnet1 with Vnet2 and then I peer Vnet2 with Vnet3, is Vnet1 peered with Vnet3?
- Can firewalls and gateways affect Azure virtual network peering?

## Learn more with self-paced training

- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/training/modules/introduction-to-azure-virtual-networks/). In this module, you learn how to design and implement Azure networking services. You learn about virtual networks, public and private IPs, DNS, virtual network peering, routing, and Azure Virtual NAT.
- [Configure Azure Virtual Network peering](https://learn.microsoft.com/training/modules/configure-vnet-peering/). Learn to configure an Azure Virtual Network peering connection and address transit and connectivity concerns.

## Key takeaways

Congratulations on completing the lab. Here are the main takeaways for this lab.

- Virtual network peering enables you to seamlessly connect two Azure virtual networks. The virtual networks appear as one for connectivity purposes.
- Azure supports connecting virtual networks within the same Azure region and across Azure regions (global).
- The traffic between virtual machines in peered virtual networks is routed directly through the Microsoft backbone infrastructure, not through a gateway or over the public Internet.
- You can resize the address space of Azure virtual networks that are peered without incurring any downtime on the currently peered address space.