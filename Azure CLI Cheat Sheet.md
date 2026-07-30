A fast, practical reference for common Azure CLI tasks. Commands assume you are logged in and using a recent Azure CLI version.

---

## Authentication & Context

```bash
az login
az account list --output table
az account set --subscription "SUBSCRIPTION_NAME_OR_ID"
az account show
```

---

## Resource Groups

```bash
az group create --name MyRG --location eastus
az group list --output table
az group show --name MyRG
az group delete --name MyRG --yes --no-wait
```

---

## Virtual Machines

### Create VM (Quick Start)

```bash
az vm create \
  --resource-group MyRG \
  --name MyVM \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys
```

### Manage VM

```bash
az vm start --resource-group MyRG --name MyVM
az vm stop --resource-group MyRG --name MyVM
az vm deallocate --resource-group MyRG --name MyVM
az vm restart --resource-group MyRG --name MyVM
az vm delete --resource-group MyRG --name MyVM --yes
```

### VM Info

```bash
az vm list --output table
az vm show --resource-group MyRG --name MyVM
az vm get-instance-view --resource-group MyRG --name MyVM
```

---

## Networking

### Virtual Networks

```bash
az network vnet create \
  --resource-group MyRG \
  --name MyVNet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name MySubnet \
  --subnet-prefix 10.0.1.0/24
```

```bash
az network vnet list --output table
az network vnet show --resource-group MyRG --name MyVNet
```

az webapp show \
    --resource-group <group_name> \
    --name <app_name> \ 
    --query **outboundIpAddresses **\
    --output tsv
### Network Security Groups (NSG)

```bash
az network nsg create --resource-group MyRG --name MyNSG
```

```bash
az network nsg rule create \
  --resource-group MyRG \
  --nsg-name MyNSG \
  --name AllowSSH \
  --priority 1000 \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --destination-port-range 22
```

---

## Storage Accounts

```bash
az storage account create \
  --name mystorageacct123 \
  --resource-group MyRG \
  --location eastus \
  --sku Standard_LRS
```

```bash
az storage account list --output table
az storage account show --name mystorageacct123 --resource-group MyRG
```

### Containers & Blobs

```bash
az storage container create --name mycontainer --account-name mystorageacct123
az storage blob upload \
  --account-name mystorageacct123 \
  --container-name mycontainer \
  --name file.txt \
  --file ./file.txt
```

---

## Azure App Service

```bash
az appservice plan create \
  --name MyPlan \
  --resource-group MyRG \
  --sku B1
```

```bash
az webapp create \
  --resource-group MyRG \
  --plan MyPlan \
  --name mywebapp123 \
  --runtime "DOTNET:8"
```

```bash
az webapp list --output table
az webapp show --name mywebapp123 --resource-group MyRG
```

---

## Azure Container Registry (ACR)

```bash
az acr create \
  --resource-group MyRG \
  --name MyACR123 \
  --sku Basic
```

```bash
az acr login --name MyACR123
az acr repository list --name MyACR123 --output table
```

---

## Azure Kubernetes Service (AKS)

```bash
az aks create \
  --resource-group MyRG \
  --name MyAKS \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys
```

```bash
az aks get-credentials --resource-group MyRG --name MyAKS
az aks list --output table
```

---

## Identity & Access Management (IAM)

### Service Principals

```bash
az ad sp create-for-rbac \
  --name MyApp \
  --role Contributor \
  --scopes /subscriptions/SUBSCRIPTION_ID
```

### Role Assignments

```bash
az role assignment list --assignee USER_OR_SP_OBJECT_ID
az role assignment create \
  --assignee USER_OR_SP_OBJECT_ID \
  --role Reader \
  --scope /subscriptions/SUBSCRIPTION_ID
```

---
Deploy code to a Web App
Manual Deployment
• Git, CLI, ZIP Deploy, FTP(S)

az webapp deploy --resource-group <group-name>
--name <name app-> --src-path <zip-package-path>



## ARM / Bicep Deployments

```bash
az deployment group create \
  --resource-group MyRG \
  --template-file main.bicep \
  --parameters params.json
```

```bash
az deployment group list --resource-group MyRG
```

---

## Monitoring & Logs

```bash
az monitor activity-log list --max-events 10
az monitor metrics list \
  --resource RESOURCE_ID \
  --metric "Percentage CPU"
```

---

## Cleanup (The Responsible Ending)

```bash
az group delete --name MyRG --yes --no-wait
```

---

## Power Tips

- Add `--output table` for human-friendly views
    
- Add `--query` with JMESPath to filter results
    
- Use `az find "vm create"` to discover syntax fast
    
- `az configure --defaults location=eastus group=MyRG` saves typing
    

---

## AZ-204 Alignment Notes

- Heavy focus on **App Service**, **Storage**, **Containers**, **ARM/Bicep**, and **Identity**
    
- Expect CLI fluency around deployment, scaling, and authentication
    

---

by assigning yourself the **Key Vault Secrets Officer** role (or Reader if you only need read):

bash

```bash
# Get your user object ID
USER_ID=$(az ad signed-in-user show --query id -o tsv)

# Get the Key Vault resource ID
KV_ID=$(az keyvault show --name kVKV1742 --query id -o tsv)

# Assign Key Vault Secrets Officer (read + write secrets)
az role assignment create \
  --assignee $USER_ID \
  --role "Key Vault Secrets Officer" \
  --scope $KV_ID
```

Or if you only need to read secrets:

bash

```bash
az role assignment create \
  --assignee $USER_ID \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

Then **wait 1-2 minutes** and refresh the portal — the banner even says "please wait several minutes for role assignments to become effective."

---

**The four Key Vault RBAC roles for reference:**

|Role|Can Do|
|---|---|
|Key Vault Administrator|Full control — keys, secrets, certs|
|Key Vault Secrets Officer|Read/write/delete secrets only|
|Key Vault Secrets User|Read secret values only|
|Key Vault Reader|View metadata, cannot read values|

### Retrieve a secret
CLI
az keyvault secret show --name "mySC300keyvaultSecret" --vault-name "<your-unique-keyvault-name>" --query "value"

PS
$secret = Get-AzKeyVaultSecret -VaultName "<your-unique-keyvault-name>" -Name "mySC300keyvaultSecret" -AsPlainText

To create a virtual network with a public IP address and one subnet in Azure, you can use both Azure CLI and Azure PowerShell commands. Here are the steps for each:

### Azure CLI

1. **Create a Virtual Network with a Subnet:**
    

Bash

```
   az network vnet create --resource-group MyResourceGroup --name MyVnet --address-prefix 192.168.0.0/16 --subnet-name MySubnet --subnet-prefix 192.168.1.0/24
   
```

2. **Create a Public IP Address:**
    

Bash

```
   az network public-ip create --resource-group MyResourceGroup --name MyPublicIP --dns-name MyPublicDNS
   
```

### Azure PowerShell

1. **Set Variables:**
    

PowerShell

```
   $rg = 'MyResourceGroup'
   $location = 'East US'
   $vnetName = 'MyVirtualNetwork'
   $subnetName = 'MySubnet'
   $publicIpName = 'MyPublicIP'
   $addressPrefixVNet = '10.0.0.0/16'
   $addressPrefixSubnet = '10.0.1.0/24'
   $domainNameLabel = 'mydnslabel'
   
```

2. **Create a Resource Group:**
    

PowerShell

```
   New-AzResourceGroup -Name $rg -Location $location
   
```

3. **Create a Virtual Network:**
    

PowerShell

```
   New-AzVirtualNetwork -Name $vnetName -ResourceGroupName $rg -Location $location -AddressPrefix $addressPrefixVNet
   
```

4. **Create a Subnet:**
    

PowerShell

```
   New-AzVirtualNetworkSubnetConfig -Name $subnetName -AddressPrefix $addressPrefixSubnet
   
```

5. **Create a Public IP Address:**
    

PowerShell

```
   $publicIp = New-AzPublicIpAddress -Name $publicIpName -ResourceGroupName $rg -Location $location -AllocationMethod Static -DomainNameLabel $domainNameLabel
   
```

These commands will help you set up a virtual network with a public IP address and one subnet in Azure. Make sure to replace the placeholder values with your actual resource names and configurations.