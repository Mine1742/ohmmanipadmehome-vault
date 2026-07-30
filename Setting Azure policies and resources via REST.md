#azure 

# Azure REST API scripting guide

Reference for using the ARM REST API with bash (Cloud Shell) and PowerShell. Covers authentication, resource management, policy operations, and async handling.

---

## Authentication

Every ARM REST call requires a Bearer token scoped to `https://management.azure.com/`.

### Option 1 — Azure CLI (easiest for lab work)

```bash
az login
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)
SUB="7a2969bb-37f1-4ab0-87ce-9fae9309b394"
```

```powershell
$token = (az account get-access-token --resource https://management.azure.com/ | ConvertFrom-Json).accessToken
$sub   = "7a2969bb-37f1-4ab0-87ce-9fae9309b394"
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }
```

### Option 2 — Service principal (client credentials)

```bash
TENANT="your-tenant-id"
CLIENT_ID="your-sp-client-id"
CLIENT_SECRET="your-sp-secret"

TOKEN=$(curl -s -X POST \
  "https://login.microsoftonline.com/${TENANT}/oauth2/v2.0/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "scope=https://management.azure.com/.default" \
  | jq -r '.access_token')
```

---

## Base URL pattern

```
https://management.azure.com
  /subscriptions/{subId}
  /resourceGroups/{rg}
  /providers/{namespace}/{type}/{name}
  ?api-version=YYYY-MM-DD
```

Every request requires an `api-version` query parameter. Check `az provider show` for valid versions per resource type.

### Common api-version values

|Resource type|api-version|
|---|---|
|Resources / resource groups|`2024-03-01`|
|Policy definitions|`2023-04-01`|
|Policy assignments|`2023-04-01`|
|Policy insights|`2019-10-01`|
|Storage accounts|`2023-05-01`|
|Virtual machines|`2024-03-01`|
|Virtual networks|`2024-01-01`|

### Find valid api-versions for any resource type

```bash
az provider show --namespace Microsoft.Storage \
  --query "resourceTypes[?resourceType=='storageAccounts'].apiVersions[]" \
  -o tsv | head -5
```

---

## How to send a request

The URL is the address. You combine it with:

- **HTTP method** — GET, PUT, PATCH, DELETE, POST
- **Headers** — `Authorization: Bearer <token>` (always) and `Content-Type: application/json` (for PUT/PATCH/POST)
- **Body** — JSON payload for PUT/PATCH/POST; nothing for GET/DELETE

### curl

```bash
curl -X GET "https://management.azure.com/subscriptions/${SUB}/resourceGroups/az104/resources?api-version=2024-03-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"
```

### PowerShell

```powershell
Invoke-RestMethod -Method GET `
  -Uri "https://management.azure.com/subscriptions/$sub/resourceGroups/az104/resources?api-version=2024-03-01" `
  -Headers $headers
```

### az rest (no token needed)

```bash
az rest --method GET \
  --url "https://management.azure.com/subscriptions/${SUB}/resourceGroups/az104/resources?api-version=2024-03-01"
```

---

## Example 1 — Inventory (list resources)

### List all resources in a subscription and export to JSON

**bash**

```bash
#!/usr/bin/env bash
SUB="7a2969bb-37f1-4ab0-87ce-9fae9309b394"
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)

curl -s -X GET \
  "https://management.azure.com/subscriptions/${SUB}/resources?api-version=2024-03-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq '[.value[] | {
      name,
      type,
      location,
      resourceGroup: (.id | split("/") | .[4]),
      tags: (.tags // {})
    }]' > azure-inventory.json

echo "Exported $(jq length azure-inventory.json) resources to azure-inventory.json"
```

**PowerShell**

```powershell
$sub   = "7a2969bb-37f1-4ab0-87ce-9fae9309b394"
$token = (az account get-access-token --resource https://management.azure.com/ | ConvertFrom-Json).accessToken
$headers = @{ Authorization = "Bearer $token" }

$resp = Invoke-RestMethod -Method GET `
  -Uri "https://management.azure.com/subscriptions/$sub/resources?api-version=2024-03-01" `
  -Headers $headers

$inventory = $resp.value | Select-Object name, type, location,
  @{n="resourceGroup"; e={ ($_.id -split "/")[4] }},
  @{n="tags"; e={ $_.tags }}

$inventory | ConvertTo-Json -Depth 5 | Out-File azure-inventory.json
Write-Host "Exported $($inventory.Count) resources"
```

### Filter to a specific resource type

**bash**

```bash
curl -s -X GET \
  "https://management.azure.com/subscriptions/${SUB}/resources?api-version=2024-03-01&\$filter=resourceType eq 'Microsoft.Storage/storageAccounts'" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq '.value[] | {name, location, resourceGroup: (.id | split("/") | .[4])}'
```

**PowerShell**

```powershell
$filter = "`$filter=resourceType eq 'Microsoft.Storage/storageAccounts'"
$resp = Invoke-RestMethod -Method GET `
  -Uri "https://management.azure.com/subscriptions/$sub/resources?api-version=2024-03-01&$filter" `
  -Headers $headers

$resp.value | Select-Object name, location, @{n="rg"; e={ ($_.id -split "/")[4] }}
```

---

## Example 2 — Bulk tagging

PATCHes standard tags onto every resource in a resource group. PATCH merges tags — it does not overwrite unrelated tags already present.

**bash**

```bash
#!/usr/bin/env bash
SUB="7a2969bb-37f1-4ab0-87ce-9fae9309b394"
RG="az104"
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)

TAGS='{
  "owner": "albert",
  "env": "lab",
  "costCenter": "it-ops",
  "managed-by": "arm-rest"
}'

RESOURCE_IDS=$(curl -s -X GET \
  "https://management.azure.com/subscriptions/${SUB}/resourceGroups/${RG}/resources?api-version=2024-03-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  | jq -r '.value[].id')

while IFS= read -r ID; do
  NAME=$(echo "$ID" | awk -F'/' '{print $NF}')
  echo "Tagging: $NAME"

  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH \
    "https://management.azure.com${ID}?api-version=2024-03-01" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"tags\": ${TAGS}}")

  echo "  → HTTP $STATUS"
done <<< "$RESOURCE_IDS"
```

**PowerShell**

```powershell
$sub  = "7a2969bb-37f1-4ab0-87ce-9fae9309b394"
$rg   = "az104"
$token = (az account get-access-token --resource https://management.azure.com/ | ConvertFrom-Json).accessToken
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

$tags = @{ owner = "albert"; env = "lab"; costCenter = "it-ops"; "managed-by" = "arm-rest" }
$body = @{ tags = $tags } | ConvertTo-Json

$resources = (Invoke-RestMethod -Method GET `
  -Uri "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/resources?api-version=2024-03-01" `
  -Headers $headers).value

foreach ($r in $resources) {
  Write-Host "Tagging: $($r.name)"
  try {
    Invoke-RestMethod -Method PATCH `
      -Uri "https://management.azure.com$($r.id)?api-version=2024-03-01" `
      -Headers $headers -Body $body | Out-Null
    Write-Host "  → OK" -ForegroundColor Green
  } catch {
    Write-Host "  → Failed: $_" -ForegroundColor Red
  }
}
```

---

## Example 3 — Policy compliance report

### Export non-compliant resources to CSV

**bash**

```bash
#!/usr/bin/env bash
SUB="7a2969bb-37f1-4ab0-87ce-9fae9309b394"
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)
OUT="noncompliant-$(date +%Y%m%d).csv"

echo "resourceId,resourceType,policyName,complianceState" > "$OUT"

curl -s -X POST \
  "https://management.azure.com/subscriptions/${SUB}/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2019-10-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"filter": "complianceState eq '\''NonCompliant'\''"}' \
  | jq -r '.value[] | [.resourceId, .resourceType, .policyDefinitionName, .complianceState] | @csv' >> "$OUT"

echo "Report saved: $OUT ($(wc -l < "$OUT") rows)"
```

**PowerShell**

```powershell
$sub  = "7a2969bb-37f1-4ab0-87ce-9fae9309b394"
$token = (az account get-access-token --resource https://management.azure.com/ | ConvertFrom-Json).accessToken
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }
$out = "noncompliant-$(Get-Date -Format yyyyMMdd).csv"

$body = '{"filter": "complianceState eq ''NonCompliant''"}'

$resp = Invoke-RestMethod -Method POST `
  -Uri "https://management.azure.com/subscriptions/$sub/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2019-10-01" `
  -Headers $headers -Body $body

$resp.value | Select-Object resourceId, resourceType, policyDefinitionName, complianceState `
  | Export-Csv -Path $out -NoTypeInformation

Write-Host "Report saved: $out ($($resp.value.Count) rows)"
```

### Trigger an on-demand compliance scan first

```bash
curl -s -X POST \
  "https://management.azure.com/subscriptions/${SUB}/resourceGroups/az104/providers/Microsoft.PolicyInsights/policyStates/latest/triggerEvaluation?api-version=2019-10-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Length: 0"
# Scan takes ~5-10 minutes; query results after it completes
```

---

## Example 4 — Deploy a resource (PUT with polling)

PUT is idempotent in ARM — running the same script twice updates in place rather than creating a duplicate.

**bash**

```bash
#!/usr/bin/env bash
SUB="7a2969bb-37f1-4ab0-87ce-9fae9309b394"
RG="az104"
NAME="albertstor$(date +%s | tail -c 5)"
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)

echo "Creating storage account: $NAME"

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  "https://management.azure.com/subscriptions/${SUB}/resourceGroups/${RG}/providers/Microsoft.Storage/storageAccounts/${NAME}?api-version=2023-05-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "westeurope",
    "sku": { "name": "Standard_LRS" },
    "kind": "StorageV2",
    "properties": {
      "allowBlobPublicAccess": false,
      "minimumTlsVersion": "TLS1_2",
      "supportsHttpsTrafficOnly": true
    },
    "tags": { "owner": "albert", "env": "lab" }
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)

if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "201" ]]; then
  echo "Created. Waiting for provisioning..."
  while true; do
    STATE=$(curl -s \
      "https://management.azure.com/subscriptions/${SUB}/resourceGroups/${RG}/providers/Microsoft.Storage/storageAccounts/${NAME}?api-version=2023-05-01" \
      -H "Authorization: Bearer ${TOKEN}" \
      | jq -r '.properties.provisioningState')
    echo "  State: $STATE"
    [[ "$STATE" == "Succeeded" ]] && break
    sleep 5
  done
  echo "Done: $NAME is ready"
else
  echo "Error ($HTTP_CODE)"
fi
```

**PowerShell**

```powershell
$sub  = "7a2969bb-37f1-4ab0-87ce-9fae9309b394"
$rg   = "az104"
$name = "albertstor$([System.DateTimeOffset]::Now.ToUnixTimeSeconds().ToString().Substring(7))"
$token = (az account get-access-token --resource https://management.azure.com/ | ConvertFrom-Json).accessToken
$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

$body = @{
  location = "westeurope"
  sku      = @{ name = "Standard_LRS" }
  kind     = "StorageV2"
  properties = @{
    allowBlobPublicAccess    = $false
    minimumTlsVersion        = "TLS1_2"
    supportsHttpsTrafficOnly = $true
  }
  tags = @{ owner = "albert"; env = "lab" }
} | ConvertTo-Json -Depth 5

Write-Host "Creating: $name"
$url = "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.Storage/storageAccounts/${name}?api-version=2023-05-01"

Invoke-RestMethod -Method PUT -Uri $url -Headers $headers -Body $body | Out-Null

do {
  Start-Sleep 5
  $state = (Invoke-RestMethod -Method GET -Uri $url -Headers $headers).properties.provisioningState
  Write-Host "  State: $state"
} while ($state -ne "Succeeded")

Write-Host "Done: $name is ready" -ForegroundColor Green
```

---

## Example 5 — Handling async (202) responses

Long-running ARM operations (delete RG, deallocate VM, etc.) return HTTP 202 with an `Azure-AsyncOperation` header. You must poll that URL until the status is `Succeeded`, `Failed`, or `Canceled`.

**bash — reusable poller function**

```bash
#!/usr/bin/env bash
SUB="7a2969bb-37f1-4ab0-87ce-9fae9309b394"
TOKEN=$(az account get-access-token --resource https://management.azure.com/ --query accessToken -o tsv)

poll_async() {
  local ASYNC_URL="$1"
  echo "Polling: $ASYNC_URL"
  while true; do
    RESULT=$(curl -s "$ASYNC_URL" -H "Authorization: Bearer ${TOKEN}")
    STATUS=$(echo "$RESULT" | jq -r '.status')
    echo "  → $STATUS"
    case "$STATUS" in
      Succeeded) echo "Operation complete"; return 0 ;;
      Failed)    echo "Failed: $(echo "$RESULT" | jq -r '.error.message')"; return 1 ;;
      Canceled)  echo "Canceled"; return 1 ;;
      *)         sleep 10 ;;
    esac
  done
}

# Example: delete a resource group
RG_TO_DELETE="my-old-rg"
HEADERS=$(curl -sI -X DELETE \
  "https://management.azure.com/subscriptions/${SUB}/resourceGroups/${RG_TO_DELETE}?api-version=2024-03-01" \
  -H "Authorization: Bearer ${TOKEN}")

HTTP_CODE=$(echo "$HEADERS" | grep -i "^HTTP" | awk '{print $2}')
echo "HTTP $HTTP_CODE"

if [[ "$HTTP_CODE" == "202" ]]; then
  ASYNC_URL=$(echo "$HEADERS" | grep -i "Azure-AsyncOperation:" | awk '{print $2}' | tr -d '\r')
  poll_async "$ASYNC_URL"
elif [[ "$HTTP_CODE" == "200" ]]; then
  echo "Completed synchronously"
fi
```

**PowerShell — reusable Wait-ArmOperation function**

```powershell
$sub  = "7a2969bb-37f1-4ab0-87ce-9fae9309b394"
$token = (az account get-access-token --resource https://management.azure.com/ | ConvertFrom-Json).accessToken
$headers = @{ Authorization = "Bearer $token" }

function Wait-ArmOperation {
  param([string]$AsyncUrl)
  Write-Host "Polling: $AsyncUrl"
  do {
    Start-Sleep 10
    $result = Invoke-RestMethod -Method GET -Uri $AsyncUrl -Headers $headers
    Write-Host "  → $($result.status)"
  } while ($result.status -notin @("Succeeded","Failed","Canceled"))

  if ($result.status -ne "Succeeded") {
    throw "Operation $($result.status): $($result.error?.message)"
  }
  Write-Host "Operation complete" -ForegroundColor Green
}

# Example: delete a resource group
$rgToDelete = "my-old-rg"
$deleteUrl  = "https://management.azure.com/subscriptions/$sub/resourceGroups/${rgToDelete}?api-version=2024-03-01"

try {
  $resp = Invoke-WebRequest -Method DELETE -Uri $deleteUrl -Headers $headers
  if ($resp.StatusCode -eq 202) {
    $asyncUrl = $resp.Headers["Azure-AsyncOperation"]
    Wait-ArmOperation -AsyncUrl $asyncUrl
  } else {
    Write-Host "Completed synchronously (HTTP $($resp.StatusCode))"
  }
} catch { Write-Host "Error: $_" -ForegroundColor Red }
```

---

## Gotchas and tips

|Issue|Notes|
|---|---|
|Wrong api-version|Each resource type has its own version list. Use `az provider show` to find valid versions.|
|403 on policy write|SP needs `Microsoft.Authorization/policyDefinitions/write` — Owner or Policy Contributor role at the scope.|
|202 instead of 200|Long-running ops return 202. Poll the `Azure-AsyncOperation` header URL until status is `Succeeded`.|
|Compliance delay|Policy effects are immediate on new resources, but compliance scans of existing resources run every 24h or on-demand trigger.|
|deployIfNotExists|Requires a Managed Identity on the assignment — add `"identity": {"type": "SystemAssigned"}` to the assignment body.|
|Decode a JWT (debug 403s)|`echo $TOKEN \| cut -d'.' -f2 \| base64 -d 2>/dev/null \| jq .`|

---

## Policy-specific endpoints

### Create a custom policy definition

```bash
POLICY_ID=$(uuidgen)

curl -s -X PUT \
  "https://management.azure.com/subscriptions/${SUB}/providers/Microsoft.Authorization/policyDefinitions/${POLICY_ID}?api-version=2023-04-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "displayName": "Require minimum TLS 1.2 on Storage Accounts",
      "policyType": "Custom",
      "mode": "All",
      "parameters": {},
      "policyRule": {
        "if": {
          "allOf": [
            { "field": "type", "equals": "Microsoft.Storage/storageAccounts" },
            { "field": "Microsoft.Storage/storageAccounts/minimumTlsVersion", "notEquals": "TLS1_2" }
          ]
        },
        "then": { "effect": "deny" }
      }
    }
  }'
```

### Assign a policy to a scope

```bash
ASSIGNMENT_NAME="require-tls12-storage"
SCOPE="/subscriptions/${SUB}/resourceGroups/az104"
POLICY_DEF_ID="/subscriptions/${SUB}/providers/Microsoft.Authorization/policyDefinitions/${POLICY_ID}"

curl -s -X PUT \
  "https://management.azure.com${SCOPE}/providers/Microsoft.Authorization/policyAssignments/${ASSIGNMENT_NAME}?api-version=2023-04-01" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"properties\": {
      \"displayName\": \"Require TLS 1.2 on Storage (az104 RG)\",
      \"policyDefinitionId\": \"${POLICY_DEF_ID}\",
      \"enforcementMode\": \"Default\",
      \"parameters\": {}
    }
  }"
```

> Use `"enforcementMode": "DoNotEnforce"` to audit without blocking while testing.

### Common policy effects

`deny` · `audit` · `auditIfNotExists` · `deployIfNotExists` · `append` · `modify` · `disabled`