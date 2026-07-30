Here's the walkthrough for your local laptop:

## Step-by-Step: Container → ACR → ACI (Local Laptop)

### Step 1: Install Docker Desktop

**Windows:**

- Download from: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Install and restart
- Open Docker Desktop and make sure it's running

**Mac:**

- Download from: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- Install and start Docker Desktop

**Linux:**

bash

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
```

Verify installation:

bash

```bash
docker --version
docker run hello-world
```

### Step 2: Install Azure CLI

**Windows (PowerShell as Administrator):**

powershell

```powershell
winget install Microsoft.AzureCLI
```

Or download installer from: [https://aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows)

**Mac:**

bash

```bash
brew update && brew install azure-cli
```

**Linux:**

bash

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Verify:**

bash

```bash
az --version
az login
```

### Step 3: Create Your Application

Open your terminal/PowerShell and create a project folder:

bash

```bash
# Create and navigate to project folder
mkdir az204-container-demo
cd az204-container-demo
```

**Create app.js:**

bash

```bash
# For Mac/Linux:
cat > app.js << 'EOF'
const http = require('http');
const os = require('os');

const PORT = 8080;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <h1>AZ-204 Container Demo</h1>
    <p>Container is running successfully!</p>
    <p>Hostname: ${os.hostname()}</p>
    <p>Platform: ${os.platform()}</p>
    <p>Time: ${new Date().toISOString()}</p>
  `);
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
EOF
```

**For Windows PowerShell, create files manually or use:**

powershell

```powershell
@"
const http = require('http');
const os = require('os');

const PORT = 8080;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <h1>AZ-204 Container Demo</h1>
    <p>Container is running successfully!</p>
    <p>Hostname: `${os.hostname()}</p>
    <p>Platform: `${os.platform()}</p>
    <p>Time: `${new Date().toISOString()}</p>
  `);
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
"@ | Out-File -FilePath app.js -Encoding utf8
```

**Create package.json:**

bash

```bash
# Mac/Linux:
cat > package.json << 'EOF'
{
  "name": "az204-demo",
  "version": "1.0.0",
  "description": "AZ-204 Container Demo",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {}
}
EOF
```

**Windows PowerShell:**

powershell

```powershell
@"
{
  "name": "az204-demo",
  "version": "1.0.0",
  "description": "AZ-204 Container Demo",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {}
}
"@ | Out-File -FilePath package.json -Encoding utf8
```

### Step 4: Create Dockerfile

**Mac/Linux:**

bash

```bash
cat > Dockerfile << 'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080
ENV NAME=AZ204Student
CMD ["npm", "start"]
EOF
```

**Windows PowerShell:**

powershell

```powershell
@"
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080
ENV NAME=AZ204Student
CMD ["npm", "start"]
"@ | Out-File -FilePath Dockerfile -Encoding utf8
```

Or just use VS Code/Notepad to create these 3 files manually.

### Step 5: Build and Test Locally

bash

```bash
# Build the image
docker build -t az204-demo:v1 .

# List images
docker images

# Run locally
docker run -d -p 8080:8080 --name az204-test az204-demo:v1

# Test it - open browser to http://localhost:8080
# Or use curl:
curl http://localhost:8080

# View logs
docker logs az204-test

# Stop and remove
docker stop az204-test
docker rm az204-test
```

### Step 6: Create Azure Container Registry

bash

```bash
# Login to Azure
az login

# Set variables (change the ACR name to something unique)
RESOURCE_GROUP="Az204"
ACR_NAME="az204studiesralph"  # Change this - must be globally unique
LOCATION="canadaeast"

# Create ACR
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --location $LOCATION

# Enable admin account
az acr update -n $ACR_NAME --admin-enabled true
```

**For Windows PowerShell, use:**

powershell

```powershell
$RESOURCE_GROUP = "Az204"
$ACR_NAME = "az204studiesralph"  # Change this
$LOCATION = "canadaeast"

az acr create `
  --resource-group $RESOURCE_GROUP `
  --name $ACR_NAME `
  --sku Basic `
  --location $LOCATION

az acr update -n $ACR_NAME --admin-enabled true
```

### Step 7: Push Image to ACR

**Option A: Push from Local Docker**

bash

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Tag image
docker tag az204-demo:v1 ${ACR_NAME}.azurecr.io/az204-demo:v1

# Push
docker push ${ACR_NAME}.azurecr.io/az204-demo:v1

# Verify
az acr repository list --name $ACR_NAME --output table
```

**Windows PowerShell:**

powershell

```powershell
az acr login --name $ACR_NAME
docker tag az204-demo:v1 "$ACR_NAME.azurecr.io/az204-demo:v1"
docker push "$ACR_NAME.azurecr.io/az204-demo:v1"
az acr repository list --name $ACR_NAME --output table
```

**Option B: Build Directly in ACR (Recommended - no Docker needed!)**

bash

```bash
# Build and push in one command
az acr build \
  --registry $ACR_NAME \
  --image az204-demo:v1 \
  .

# List images
az acr repository show-tags --name $ACR_NAME --repository az204-demo --output table
```

### Step 8: Deploy to Azure Container Instance

bash

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)

# Create ACI
az container create \
  --resource-group $RESOURCE_GROUP \
  --name az204-demo-aci \
  --image ${ACR_NAME}.azurecr.io/az204-demo:v1 \
  --cpu 1 \
  --memory 1 \
  --registry-login-server ${ACR_NAME}.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label az204-demo-ralph \
  --ports 8080

# Get the public URL
az container show \
  --resource-group $RESOURCE_GROUP \
  --name az204-demo-aci \
  --query ipAddress.fqdn \
  --output tsv
```

**Windows PowerShell:**

powershell

```powershell
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username --output tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv

az container create `
  --resource-group $RESOURCE_GROUP `
  --name az204-demo-aci `
  --image "$ACR_NAME.azurecr.io/az204-demo:v1" `
  --cpu 1 `
  --memory 1 `
  --registry-login-server "$ACR_NAME.azurecr.io" `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --dns-name-label az204-demo-ralph `
  --ports 8080

$FQDN = az container show --resource-group $RESOURCE_GROUP --name az204-demo-aci --query ipAddress.fqdn --output tsv
echo "Your app is at: http://${FQDN}:8080"
```

### Step 9: Test Your Deployment

bash

```bash
# Get the URL
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name az204-demo-aci --query ipAddress.fqdn --output tsv)
echo "Visit: http://${FQDN}:8080"

# View logs
az container logs --resource-group $RESOURCE_GROUP --name az204-demo-aci

# Stream logs
az container attach --resource-group $RESOURCE_GROUP --name az204-demo-aci
```

Open your browser and visit the URL!

### Step 10: Update and Redeploy

When you make changes:

bash

```bash
# 1. Update your code (edit app.js)

# 2. Build new version
az acr build --registry $ACR_NAME --image az204-demo:v2 .

# 3. Delete old container
az container delete --resource-group $RESOURCE_GROUP --name az204-demo-aci --yes

# 4. Create new container with v2
az container create \
  --resource-group $RESOURCE_GROUP \
  --name az204-demo-aci \
  --image ${ACR_NAME}.azurecr.io/az204-demo:v2 \
  --cpu 1 --memory 1 \
  --registry-login-server ${ACR_NAME}.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label az204-demo-ralph \
  --ports 8080
```

### Step 11: Clean Up

bash

```bash
# Delete container instance
az container delete --resource-group $RESOURCE_GROUP --name az204-demo-aci --yes

# Delete ACR (optional - costs about $5/month for Basic)
az acr delete --name $ACR_NAME --yes

# Delete local images
docker rmi az204-demo:v1
docker rmi ${ACR_NAME}.azurecr.io/az204-demo:v1
```

---

## Quick Reference Commands

bash

```bash
# Build locally
docker build -t myapp:v1 .

# Run locally
docker run -d -p 8080:8080 myapp:v1

# Build in ACR
az acr build --registry myacr --image myapp:v1 .

# List ACR images
az acr repository list --name myacr

# Create ACI
az container create --name mycontainer --image myacr.azurecr.io/myapp:v1

# View logs
az container logs --name mycontainer --resource-group myRG
```


# Manage revisions and secrets in Azure Container Apps
	
	### Updating your container app
	
az containerapp update \
  --name <APPLICATION_NAME> \
  --resource-group <RESOURCE_GROUP_NAME> \
  --image <IMAGE_NAME>
az containerapp revision list \
  --name <APPLICATION_NAME> \
  --resource-group <RESOURCE_GROUP_NAME> \
  -o table
	
	
	## Manage secrets in Azure Container Apps
az containerapp create \
  --resource-group "my-resource-group" \
  --name queuereader \
  --environment "my-environment-name" \
  --image demos/queuereader:v1 \
  --secrets "queue-connection-string=$CONNECTION_STRING"

	declares a connection string at the application level.
az containerapp create \
  --resource-group "my-resource-group" \
  --name myQueueApp \
  --environment "my-environment-name" \
  --image demos/myQueueApp:v1 \
  --secrets "queue-connection-string=$CONNECTIONSTRING" \
  --env-vars "QueueName=myqueue" "ConnectionString=secretref:queue-connection-string"