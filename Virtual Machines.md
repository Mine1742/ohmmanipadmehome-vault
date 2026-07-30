#az104 #azure 

## Create a Linux VM with the Azure CLI

The Azure CLI includes the `vm` command to work with virtual machines in Azure. We can supply several subcommands to do specific tasks. The most common include:

|Sub-command|Description|
|---|---|
|`create`|Create a new virtual machine|
|`deallocate`|Deallocate a virtual machine|
|`delete`|Delete a virtual machine|
|`list`|List the created virtual machines in your subscription|
|`open-port`|Open a specific network port for inbound traffic|
|`restart`|Restart a virtual machine|
|`show`|Get the details for a virtual machine|
|`start`|Start a stopped virtual machine|
|`stop`|Stop a running virtual machine|
|`update`|Update a property of a virtual machine|

 Note

For a complete list of commands, you can check the [Azure CLI reference documentation](https://learn.microsoft.com/en-us/cli/azure/reference-index).

Let's start with the first one: `az vm create`. You can use this command to create a virtual machine in a resource group. There are several parameters you can pass to configure all the aspects of the new VM. The four parameters that you must supply are:

|Parameter|Description|
|---|---|
|`--resource-group`|The resource group that will own the virtual machine; use **myResourceGroupName**.|
|`--name`|The name of the virtual machine; must be unique within the resource group.|
|`--image`|The operating system image to use to create the VM.|
|`--location`|The region in which to place the VM. Typically, this would be close to the VM's consumer.|

In addition, it's helpful to add the `--verbose` flag to see progress while the VM is being created.

## Create a Linux virtual machine

Let's create a new Linux virtual machine. Execute the following command in Azure Cloud Shell to create an Ubuntu VM in the _West US_ location.

Azure CLI

```
az vm create \
  --resource-group "myResourceGroupName" \
  --location westus \
  --name SampleVM \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --verbose 
```

 Tip

You can use the **Copy** button to copy commands to the clipboard. To paste, right-click on a new line in the Cloud Shell terminal and select **Paste**, or use the Shift+Insert keyboard shortcut (⌘+V on macOS).

This command creates a new **Ubuntu** Linux virtual machine with the name `SampleVM`. Notice that the Azure CLI tool waits while the VM is being created. You can add the `--no-wait` option to tell the Azure CLI tool to return immediately and have Azure continue creating the VM in the background. This is useful if you're executing the command in a script.

We're specifying the administrator account name through the `--admin-username` flag to be `azureuser`. If you omit this, the `az vm create` command will use your _current user name_. Because the rules for account names are different for each OS, it's safer to specify a specific name.

 Note

Common names such as "root" and "admin" aren't allowed for most images.

We're also using the `generate-ssh-keys` flag. Linux distributions use this parameter, and it creates a pair of security keys so we can use the `ssh` tool to access the virtual machine remotely. The two files are placed into the `.ssh` folder on your machine and in the VM. If you already have an SSH key named `id_rsa` in the target folder, then that SSH key will be used rather than generating a new key.

Once Azure CLI finishes creating the VM, you'll get a JSON response which includes the current state of the virtual machine and its public and private IP addresses assigned by Azure:

JSON

{
  "fqdns": "",
  "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/Learn-bbbb1b1b-cc2c-dd3d-ee4e-ffffff5f5f5f/providers/Microsoft.Compute/virtualMachines/SampleVM",
  "location": "westus",
  "macAddress": "00-0D-3A-58-F8-45",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "40.83.165.85",
  "resourceGroup": "bbbb1b1b-cc2c-dd3d-ee4e-ffffff5f5f5f",
  "zones": ""
}

## Connecting to the VM with SSH

We can quickly test that the Linux VM is up and running by using the public IP address in the Secure Shell (`ssh`) tool. Remember that we set our admin name to `azureuser`, so we need specify that. Make sure to use the public IP address from _your_ running instance.

Azure CLI

```
ssh azureuser@<public-ip-address>
```

## Listing images

You can get a list of the available VM images using the following command:

Azure CLI

```
az vm image list --output table
```

 Note

If you get the error _az: command not found_, type `exit` into the shell and try again.

This outputs the most popular images that are part of an offline list built into the Azure CLI. However, there are _hundreds_ of image options available in the Azure Marketplace.

## Getting all images

You can get a full list by adding the `--all` flag to the command. Because the list of images in the Marketplace is very large, it's helpful to filter the list with the `--publisher`, `--sku` or `–-offer` options.

For example, try the following command to see _all_ Wordpress images available:

Azure CLI

```
az vm image list --sku Wordpress --output table --all
```

Or this command to see all images provided by Microsoft:

Azure CLI

```
az vm image list --publisher Microsoft --output table --all
```

These commands can take a few moments to complete.

## Location-specific images

Some images are only available in certain locations. Try adding the `--location [location]` flag to the command to scope the results to ones available in the region where you want to create the virtual machine. For example, type the following into Azure Cloud Shell to get a list of images available in the `eastus` region.

Azure CLI

```
az vm image list --location eastus --output table
```

Try checking some of the images in the other Azure available locations.

 Tip

These are the standard images that are provided by Azure. Keep in mind that you can also [create and upload your own custom images](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/tutorial-custom-images) to create VMs based on unique configurations or less common versions or distributions of an operating system.
## Predefined VM sizes

When you create a virtual machine, you can supply a _VM size_ value that determines the amount of compute resources devoted to the VM, including CPU, GPU, and memory made available to the virtual machine from Azure.

Azure defines a set of predefined VM sizes for Linux and Windows from which to choose based on the expected usage.

|Type|Sizes|Description|
|---|---|---|
|General purpose|Dsv3, Dv3, DSv2, Dv2, DS, D, Av2, A0-7|Balanced CPU-to-memory. Ideal for dev/test and small to medium applications and data solutions.|
|Compute optimized|Fs, F|High CPU-to-memory. Good for medium-traffic applications, network appliances, and batch processes.|
|Memory optimized|Esv3, Ev3, M, GS, G, DSv2, DS, Dv2, D|High memory-to-core. Great for relational databases, medium to large caches, and in-memory analytics.|
|Storage optimized|Ls|High disk throughput and IO. Ideal for big data, SQL, and NoSQL databases.|
|GPU optimized|NV, NC|Specialized VMs targeted for heavy graphic rendering and video editing.|
|High performance|H, A8-11|Our most powerful CPU VMs with optional high-throughput network interfaces (RDMA).|

The available sizes change based on the region in which you're creating the VM. You can get a list of the available sizes using the `vm list-sizes` command. Try typing the following command into Azure Cloud Shell:

Azure CLI

```
az vm list-sizes --location eastus --output table
```

Here's an abbreviated response for `eastus`:

Output

```
  MaxDataDiskCount    MemoryInMb  Name                      NumberOfCores    OsDiskSizeInMb    ResourceDiskSizeInMb
------------------  ------------  ----------------------  ---------------  ----------------  ----------------------
                 2          2048  Standard_B1ms                         1           1047552                    4096
                 2          1024  Standard_B1s                          1           1047552                    2048
                 4          8192  Standard_B2ms                         2           1047552                   16384
                 4          4096  Standard_B2s                          2           1047552                    8192
                 8         16384  Standard_B4ms                         4           1047552                   32768
                16         32768  Standard_B8ms                         8           1047552                   65536
                 4          3584  Standard_DS1_v2                       1           1047552                    7168
                 8          7168  Standard_DS2_v2                       2           1047552                   14336
                16         14336  Standard_DS3_v2                       4           1047552                   28672
                32         28672  Standard_DS4_v2                       8           1047552                   57344
                64         57344  Standard_DS5_v2                      16           1047552                  114688
        ....
                64       3891200  Standard_M128-32ms                  128           1047552                 4096000
                64       3891200  Standard_M128-64ms                  128           1047552                 4096000
                64       3891200  Standard_M128ms                     128           1047552                 4096000
                64       2048000  Standard_M128s                      128           1047552                 4096000
                64       1024000  Standard_M64                         64           1047552                 8192000
                64       1792000  Standard_M64m                        64           1047552                 8192000
                64       2048000  Standard_M128                       128           1047552                16384000
                64       3891200  Standard_M128m                      128           1047552                16384000
```

## Specify a size during VM creation

We didn't specify a size when we created our VM, so Azure selected a default general-purpose size for us. However, we can specify the size as part of the `vm create` command using the `--size` parameter. For example, you could use the following command to create a two-core virtual machine:

Azure CLI

```
az vm create \
    --resource-group "myResourceGroupName" \
    --name SampleVM2 \
    --image Ubuntu2204 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --verbose \
    --size "Standard_DS2_v2"
```

 Warning

Your subscription tier [enforces limits](https://learn.microsoft.com/en-us/azure/azure-subscription-service-limits) on how many resources you can create, as well as the total size of those resources. Quota limits depend upon your subscription type and region. The Azure CLI lets you know when you exceed this limit with a **Quota Exceeded** error. If you hit this error in your own paid subscription, you can request to raise the limits associated with your paid subscription (up to 10,000 vCPUs) through a [free online request](https://learn.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-quota-errors).

## Resize an existing VM

We can also resize an existing VM if the workload changes or if it was incorrectly sized at creation. Let's use the first VM we created, SampleVM. Before requesting a resize, we must check to see if the desired size is available in the cluster of which our VM is a part. We can use the `vm list-vm-resize-options` command:

Azure CLI

```
az vm list-vm-resize-options \
    --resource-group "myResourceGroupName" \
    --name SampleVM \
    --output table
```

This command returns a list of all the possible size configurations available in the resource group. If the size we want isn't available in our cluster but _is_ available in the region, we can [deallocate the VM](https://learn.microsoft.com/en-us/cli/azure/vm#az-vm-deallocate). This command stops the running VM and removes it from the current cluster without losing any resources. We can then resize it, which re-creates the VM in a new cluster where the size configuration is available.

To resize a VM, we'll use the `vm resize` command. For example, perhaps we find our VM is underpowered for the task we want it to perform. We could bump it up to a D2s_v3, where it has 2 vCores and 8 GB of memory. Type this command in Cloud Shell:

Azure CLI

```
az vm resize \
    --resource-group "myResourceGroupName" \
    --name SampleVM \
    --size Standard_D2s_v3
```

This command takes a few minutes to reduce the resources of the VM, and once it's done, it returns a new JSON configuration.

# Query system and runtime information about the VM

Let's start by running `vm list`.

Azure CLI

```
az vm list
```

This command will return _all_ virtual machines defined in this subscription. You can filter the output to a specific resource group through the `--resource-group` parameter.

## Output types

Notice that the default response type for all the commands we've done so far is JSON. This is great for scripting, but most people find it harder to read. You can change the output style for any response through the `--output` flag. For example, run the following command in Azure Cloud Shell to see the different output style.

Azure CLI

```
az vm list --output table
```

Along with `table`, you can specify `json` (the default), `jsonc` (colorized JSON), or `tsv` (Tab-Separated Values). Try a few variations with the preceding command to see the difference.

## Get the IP address

Another useful command is `vm list-ip-addresses`, which lists the public and private IP addresses for a VM. If they change, or you didn't capture them during creation, you can retrieve them at any time.

Azure CLI

```
az vm list-ip-addresses -n SampleVM -o table
```

This returns output like:

Output

```
VirtualMachine    PublicIPAddresses    PrivateIPAddresses
----------------  -------------------  --------------------
SampleVM          168.61.54.62         10.0.0.4
```

 Tip

Notice that we're using a shorthand syntax for the `--output` flag as `-o`. You can shorten most parameters to Azure CLI commands to a single dash and letter. For example, you can shorten `--name` to `-n` and `--resource-group` to `-g`. This is handy for entering keyboard characters, but we recommend using the full option name in scripts for clarity. Check the documentation for details about each command.

## Get VM details

We can get more detailed information about a specific virtual machine by name or ID running the `vm show` command.

Azure CLI

```
az vm show --resource-group "myResourceGroupName" --name SampleVM
```

This returns a fairly large JSON block with all sorts of information about the VM, including attached storage devices, network interfaces, and all of the object IDs for resources that the VM is connected to. Again, we could change to a table format, but that omits almost all of the interesting data. Instead, we can turn to a built-in query language for JSON called [JMESPath](http://jmespath.org/).

## Add filters to queries with JMESPath

JMESPath is an industry-standard query language built around JSON objects. The simplest query is to specify an _identifier_ that selects a key in the JSON object.

For example, given the object:

JSON

```
{
  "people": [
    {
      "name": "Fred",
      "age": 28
    },
    {
      "name": "Barney",
      "age": 25
    },
    {
      "name": "Wilma",
      "age": 27
    }
  ]
}
```

We can use the query `people` to return the array of values for the `people` array. If we just want _one_ of the people, we can use an indexer. For example, `people[1]` would return:

JSON

```
{
    "name": "Barney",
    "age": 25
}
```

We can also add specific qualifiers that would return a subset of the objects based on some criteria. For example, adding the qualifier `people[?age > '25']` would return:

JSON

```
[
  {
    "name": "Fred",
    "age": 28
  },
  {
    "name": "Wilma",
    "age": 27
  }
]
```

Finally, we can constrain the results by adding a select: `people[?age > '25'].[name]` that returns just the names:

JSON

```
[
  [
    "Fred"
  ],
  [
    "Wilma"
  ]
]
```

JMESQuery has several other interesting query features. When you have time, check out the [online tutorial](http://jmespath.org/tutorial.html) available on the [JMESPath.org](http://jmespath.org/) site.

## Filter your Azure CLI queries

With a basic understanding of JMES queries, we can add filters to the data returned by queries like the `vm show` command. For example, we can retrieve the admin username:

Azure CLI

```
az vm show \
    --resource-group "myResourceGroupName" \
    --name SampleVM \
    --query "osProfile.adminUsername"
```

We can get the size assigned to our VM:

Azure CLI

```
az vm show \
    --resource-group "myResourceGroupName" \
    --name SampleVM \
    --query hardwareProfile.vmSize
```

Or, to retrieve all the IDs for your network interfaces, we can run the query:

Azure CLI

```
az vm show \
    --resource-group "myResourceGroupName" \
    --name SampleVM \
    --query "networkProfile.networkInterfaces[].id"
```

This query technique works with any Azure CLI command, and you can use it to pull specific bits of data out on the command line. It's useful for scripting, as well. For example, you can pull a value out of your Azure account and store it in an environment or script variable. If you decide to use it this way, it's useful to add the `--output tsv` parameter (which you can shorten to `-o tsv`). This will return results that only include the actual data values with tab separators.

For example:

Azure CLI

```
az vm show \
    --resource-group "myResourceGroupName" \
    --name SampleVM \
    --query "networkProfile.networkInterfaces[].id" -o tsv
```

returns the text: `/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/bbbb1b1b-cc2c-dd3d-ee4e-ffffff5f5f5f/providers/Microsoft.Network/networkInterfaces/SampleVMVMNic`

# Start and stop your VM with the Azure CLI
## Stop a VM

We can stop a running VM with the `vm stop` command. You must pass the name and resource group or the unique ID for the VM:

Azure CLI

```
az vm stop \
    --name SampleVM \
    --resource-group "myResourceGroupName"
```

You can verify the VM has stopped by attempting to ping the public IP address, using `ssh`, or through the `vm get-instance-view` command. This final approach returns the same basic data as `vm show`, but includes details about the instance itself. Try entering the following command into Azure Cloud Shell to see the current running state of your VM:

Azure CLI

```
az vm get-instance-view \
    --name SampleVM \
    --resource-group "myResourceGroupName" \
    --query "instanceView.statuses[?starts_with(code, 'PowerState/')].displayStatus" -o tsv
```

This command should return `VM stopped` as the result.

## Start a VM

We can do the reverse through the `vm start` command.

Azure CLI

```
az vm start \
    --name SampleVM \
    --resource-group "myResourceGroupName"
```

This command starts a stopped VM. You can verify it through the `vm get-instance-view` query you used in the last section, which should now return `VM running`.

## Restart a VM

Finally, we can restart a VM if we've made changes that require a reboot by running the `vm restart` command. You can add the `--no-wait` flag if you want the Azure CLI to return immediately without waiting for the VM to reboot.
# Install software on your VM
## Install NGINX web server

1. Locate the public IP address of your _SampleVM_ Linux virtual machine.
    
    Azure CLI
    
    ```
    az vm list-ip-addresses --name SampleVM --output table
    ```
    
2. Next, open an `ssh` connection to _SampleVM_ using the Public IP address from the preceding step.
    
    Bash
    
    ```
    ssh azureuser@<PublicIPAddress>
    ```
    
3. After you're logged in to the virtual machine, run the following command to install the `nginx` web server. The command takes a few moments to complete.
    
    Bash
    
    ```
    sudo apt-get -y update && sudo apt-get -y install nginx
    ```
    
4. Exit the Secure Shell:
    
    Bash
    
    ```
    exit
    ```
    

## Retrieve your default page

1. In Azure Cloud Shell, use `curl` to read the default page from your Linux web server by running the following command, replacing `<PublicIPAddress>` with the public IP you found previously. You can also open a new browser tab and try to browse to the public IP address.
    
    Bash
    
    ```
    curl -m 80 <PublicIPAddress>
    ```
    
    This command will fail, because the Linux virtual machine doesn't expose port 80 (`http`) through the network security group that secures the network connectivity to the virtual machine. We can fix the failure by running the Azure CLI command `vm open-port`.
    
2. Enter the following command into Cloud Shell to open port 80:
    
    Azure CLI
    
    ```
    az vm open-port \
        --port 80 \
        --resource-group "myResourceGroupName" \
        --name SampleVM
    ```
    
    It takes a moment to add the network rule and open the port through the firewall.
    
3. Run the `curl` command again.
    
    Bash
    
    ```
    curl -m 80 <PublicIPAddress>
    ```
    
    This time, it should return data like the following. You can see the page in a browser as well.
    
    HTML
    
    ```
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>
    
    <p>For online documentation and support, refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>
    
    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```