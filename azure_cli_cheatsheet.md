# 🌀 Azure CLI Cheat Sheet

A practical reference for managing Azure resources from the command line using `az`.

---

## 🔑 AUTHENTICATION & ACCOUNT MANAGEMENT

```bash
az login                                       # Sign in interactively
az login --use-device-code                     # Login via device code
az account list --output table                 # List all subscriptions
az account set --subscription "My Subscription"
az account show                                # Show active account
```

---

## 🏗️ RESOURCE GROUPS

```bash
az group create --name MyResourceGroup --location eastus
az group list --output table
az group show --name MyResourceGroup
az group delete --name MyResourceGroup --yes --no-wait
```

---

## 💾 STORAGE ACCOUNTS

```bash
az storage account create --name mystorageacct --resource-group MyResourceGroup --location eastus --sku Standard_LRS
az storage account list --resource-group MyResourceGroup --output table
az storage container create --name backups --account-name mystorageacct
az storage blob upload --account-name mystorageacct --container-name backups --file file.txt --name file.txt
az storage blob list --account-name mystorageacct --container-name backups --output table
```

---

## ☁️ VIRTUAL MACHINES

```bash
az vm create --resource-group MyResourceGroup --name MyVM --image Ubuntu2204 --admin-username azureuser --generate-ssh-keys
az vm list --output table
az vm show --name MyVM --resource-group MyResourceGroup
az vm start --name MyVM --resource-group MyResourceGroup
az vm stop --name MyVM --resource-group MyResourceGroup
az vm delete --name MyVM --resource-group MyResourceGroup --yes
```

---

## 🌐 NETWORKING

```bash
az network vnet create --name MyVNet --resource-group MyResourceGroup --subnet-name MySubnet
az network nsg create --resource-group MyResourceGroup --name MyNSG
az network nsg rule create --resource-group MyResourceGroup --nsg-name MyNSG --name AllowHTTP --protocol tcp --direction inbound --priority 1000 --destination-port-ranges 80 --access allow
az network public-ip create --resource-group MyResourceGroup --name MyPublicIP
az network nic create --resource-group MyResourceGroup --name MyNIC --vnet-name MyVNet --subnet MySubnet --network-security-group MyNSG
```

---

## 🧱 AZURE APP SERVICE

```bash
az appservice plan create --name MyPlan --resource-group MyResourceGroup --sku B1 --is-linux
az webapp create --resource-group MyResourceGroup --plan MyPlan --name mywebapp123 --runtime "PYTHON|3.10"
az webapp list --output table
az webapp config set --resource-group MyResourceGroup --name mywebapp123 --startup-file "gunicorn --bind=0.0.0.0 app:app"
az webapp browse --name mywebapp123 --resource-group MyResourceGroup
```

---

## 🐳 AZURE CONTAINER & KUBERNETES

```bash
az acr create --resource-group MyResourceGroup --name MyContainerReg --sku Basic
az acr login --name MyContainerReg
az acr build --registry MyContainerReg --image myapp:v1 .
az aks create --resource-group MyResourceGroup --name MyAKSCluster --node-count 2 --generate-ssh-keys
az aks get-credentials --resource-group MyResourceGroup --name MyAKSCluster
kubectl get nodes
```

---

## 🧮 DATABASES

```bash
az sql server create --name my-sql-server --resource-group MyResourceGroup --location eastus --admin-user adminuser --admin-password StrongPassword123
az sql db create --resource-group MyResourceGroup --server my-sql-server --name MyDatabase --service-objective S0
az sql db list --resource-group MyResourceGroup --server my-sql-server
az postgres flexible-server create --name mypg --resource-group MyResourceGroup --location eastus --admin-user pguser --admin-password StrongPassword123
```

---

## 🔐 IAM & SECURITY

```bash
az ad user list --output table
az role assignment list --assignee user@domain.com
az role assignment create --assignee user@domain.com --role "Contributor" --resource-group MyResourceGroup
az keyvault create --name MyKeyVault --resource-group MyResourceGroup --location eastus
az keyvault secret set --vault-name MyKeyVault --name "DBPassword" --value "StrongPassword123"
```

---

## 💰 BILLING & COST MANAGEMENT

```bash
az billing account list --output table
az consumption usage list --start-date 2025-01-01 --end-date 2025-01-31 --output table
az consumption budget list --resource-group MyResourceGroup
```

---

## 🧾 LOGGING & MONITORING

```bash
az monitor activity-log list --max-events 20
az monitor metrics list --resource /subscriptions/SUB_ID/resourceGroups/MyResourceGroup/providers/Microsoft.Compute/virtualMachines/MyVM
az monitor log-analytics workspace list
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| Login to Azure | `az login` |
| Create a VM | `az vm create --name MyVM` |
| List resources | `az resource list --output table` |
| Deploy web app | `az webapp create --name mywebapp123` |
| Upload blob | `az storage blob upload --file file.txt` |
| Create resource group | `az group create --name MyGroup` |
| Assign IAM role | `az role assignment create --assignee user@domain.com` |

---

## 💡 TIPS

- Use `--output table` or `--output json` for readability.
- Chain commands with `&&` to automate workflows.
- Use `az configure --defaults` to set permanent defaults.
- Combine with `jq` to parse JSON outputs.
- Use `az interactive` for an in-shell command helper.

---

**Created for:** Azure administrators, engineers, and DevOps professionals  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #azurecli #az #devops #cloud #automation #microsoft
