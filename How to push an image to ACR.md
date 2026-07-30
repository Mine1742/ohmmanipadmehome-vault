## Summary — commands I ran to push the image to ACR ✅

### 1) Create / confirm registry

- az acr create --resource-group AZ204 --name az204container1 --sku Basic --location canadaeast
    - Result: Registry created (loginServer = **az204container1.azurecr.io**)

### 2) Log in to the registry

- az acr login --name az204container1
    - Output: **Login Succeeded** ✅

### 3) Confirm local image exists

- docker images | findstr az204-demo
    - Found: **az204-demo:v1** (image id: a6ded4af936b)

### 4) Tag the image for ACR

- docker tag az204-demo:v1 az204container1.azurecr.io/az204-demo:v1
    - (Succeeds silently)

### 5) Push the image

- docker push az204container1.azurecr.io/az204-demo:v1
    - Output: image layers pushed, digest returned (e.g., `sha256:a6ded4af...`) ✅

### 6) Verify tag in ACR

- az acr repository show-tags --name az204container1 --repository az204-demo --output table
    - Result: shows **v1** present in the registry ✅