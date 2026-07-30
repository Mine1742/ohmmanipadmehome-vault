#azure 

# Azure Identity Management via CLI

## Setup & Auth

```bash
# Login
az login

# Login with a specific tenant
az login --tenant <tenant-id>

# Set default subscription
az account set --subscription <subscription-id>

# Confirm context
az account show
```

---

## Users (Entra ID / AAD)

```bash
# List users
az ad user list --output table

# Get a specific user
az ad user show --id user@domain.com

# Create a user
az ad user create \
  --display-name "Jane Doe" \
  --user-principal-name jane@domain.com \
  --password "TempPass123!" \
  --force-change-password-next-sign-in true

# Update a user property
az ad user update --id user@domain.com --display-name "Jane A. Doe"

# Delete a user
az ad user delete --id user@domain.com

# List a user's group memberships
az ad user get-member-groups --id user@domain.com
```

---

## Groups

```bash
# List groups
az ad group list --output table

# Create a group
az ad group create --display-name "IT-Admins" --mail-nickname "IT-Admins"

# Add a member
az ad group member add --group "IT-Admins" --member-id <user-object-id>

# Remove a member
az ad group member remove --group "IT-Admins" --member-id <user-object-id>

# Check membership
az ad group member check --group "IT-Admins" --member-id <user-object-id>

# List group members
az ad group member list --group "IT-Admins" --output table
```

---

## Service Principals & App Registrations

```bash
# List service principals
az ad sp list --output table

# Create a service principal (also creates app registration)
az ad sp create-for-rbac --name "my-app-sp" --role Contributor \
  --scopes /subscriptions/<sub-id>

# Show a service principal
az ad sp show --id <app-id-or-object-id>

# List credentials (certs/secrets) on an SP
az ad app credential list --id <app-id>

# Reset/rotate credentials
az ad sp credential reset --id <app-id>

# Delete a service principal
az ad sp delete --id <object-id>
```

---

## Managed Identities

```bash
# Create a user-assigned managed identity
az identity create --name "my-identity" --resource-group "my-rg"

# List user-assigned managed identities
az identity list --resource-group "my-rg" --output table

# Get the principal ID (needed for role assignments)
az identity show --name "my-identity" --resource-group "my-rg" \
  --query principalId -o tsv

# Assign a managed identity to a VM
az vm identity assign --name "my-vm" --resource-group "my-rg" \
  --identities "my-identity"

# Assign system-assigned identity to a VM
az vm identity assign --name "my-vm" --resource-group "my-rg"
```

---

## Role Assignments (RBAC)

```bash
# List role assignments for a user
az role assignment list --assignee user@domain.com --output table

# Assign a role to a user at resource group scope
az role assignment create \
  --assignee user@domain.com \
  --role "Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

# Assign a role to a managed identity
az role assignment create \
  --assignee <principal-id> \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

# Remove a role assignment
az role assignment delete \
  --assignee user@domain.com \
  --role "Contributor" \
  --resource-group "my-rg"

# List available roles
az role definition list --output table
```

---

## Useful Querying Tips

```bash
# Get just the object ID of a user
az ad user show --id user@domain.com --query id -o tsv

# Find all SPs with a name pattern
az ad sp list --display-name "my-app" --output table

# List all role assignments in a subscription
az role assignment list --all --output table

# Filter role assignments by scope
az role assignment list --scope /subscriptions/<sub-id>/resourceGroups/<rg>
```

---

## Object Type Quick Reference

| Object | Command Prefix | Notes |
|---|---|---|
| Users | `az ad user` | Entra ID users |
| Groups | `az ad group` | Security & M365 groups |
| App Registrations | `az ad app` | The app object |
| Service Principals | `az ad sp` | Enterprise app / SP object |
| Managed Identities | `az identity` | System or user-assigned |
| Role Assignments | `az role assignment` | RBAC |

---

## Notes

- Synced (AD Connect) users cannot have cloud-side attribute changes via CLI
- For `ImmutableId` changes or synced-to-cloud-only conversions, use `az rest` or the MS Graph CLI (`mgc`)
- User-assigned managed identities require the `principalId` (not `clientId`) for RBAC assignments