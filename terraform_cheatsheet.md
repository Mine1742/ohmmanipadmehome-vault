# 🌍 Terraform Cheat Sheet

A reference for managing infrastructure as code with Terraform, from setup to deployment.

---

## ⚙️ SETUP & INITIALIZATION

```bash
terraform -version
terraform init                         # Initialize working directory
terraform validate                     # Validate configuration syntax
terraform fmt                          # Format .tf files
terraform providers                    # List providers used
```

### Directory Structure Example
```
main.tf
variables.tf
outputs.tf
terraform.tfvars
```

---

## 🧩 PROVIDERS & BACKENDS

### **Provider Block Example**
```hcl
provider "google" {
  project = "dao-of-life"
  region  = "us-east1"
}
```

### **Remote Backend Example**
```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "dao-infra/state"
  }
}
```

---

## 🏗️ CORE WORKFLOW

```bash
terraform plan                         # Show execution plan
terraform apply                        # Apply configuration
terraform destroy                      # Delete infrastructure
terraform refresh                      # Update state from real resources
terraform output                       # Display output variables
terraform show                         # Show current state
```

---

## 🧮 VARIABLES & OUTPUTS

### **variables.tf**
```hcl
variable "region" {
  type        = string
  description = "Deployment region"
  default     = "us-east1"
}
```

### **terraform.tfvars**
```hcl
region = "us-central1"
```

### **outputs.tf**
```hcl
output "instance_ip" {
  value = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip
}
```

---

## ☁️ RESOURCE EXAMPLES

### **Google Compute Engine**
```hcl
resource "google_compute_instance" "vm" {
  name         = "dao-vm"
  machine_type = "e2-medium"
  zone         = "us-east1-b"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
```

### **Azure Virtual Machine**
```hcl
resource "azurerm_linux_virtual_machine" "main" {
  name                = "dao-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B1s"
  admin_username      = "albert"
  disable_password_authentication = true
}
```

---

## 🧱 STATE MANAGEMENT

```bash
terraform state list                   # List tracked resources
terraform state show <resource>        # Show details
terraform state pull                   # View raw state
terraform state rm <resource>          # Remove from state
terraform taint <resource>             # Force recreation
```

---

## 🧮 DATA SOURCES

```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
```

Use with:
```hcl
ami = data.aws_ami.ubuntu.id
```

---

## 🔐 VARIABLES, SECRETS & ENVIRONMENT

```bash
export TF_VAR_region="us-east1"
export GOOGLE_APPLICATION_CREDENTIALS="key.json"
```

Store secrets securely using:
- `.tfvars` (gitignored)
- `terraform.tfstate` encryption
- `HashiCorp Vault` or `Secret Manager`

---

## 🪄 WORKSPACES

```bash
terraform workspace list
terraform workspace new dev
terraform workspace select dev
```

Workspaces allow parallel environments (e.g., dev, staging, prod).

---

## 🧾 MODULES

### **Usage Example**
```hcl
module "network" {
  source = "./modules/network"
  vpc_name = "dao-vpc"
}
```

### **Registry Example**
```hcl
module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "~> 7.0"
  project_id = "dao-of-life"
}
```

---

## 📦 IMPORTING EXISTING RESOURCES

```bash
terraform import google_compute_instance.vm dao-vm
```

---

## 🧰 DEBUGGING & TROUBLESHOOTING

```bash
TF_LOG=DEBUG terraform apply
TF_LOG_PATH=./terraform.log
terraform plan -out=planfile
terraform show planfile
```

---

## 🧾 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| Initialize project | `terraform init` |
| Plan changes | `terraform plan` |
| Apply changes | `terraform apply` |
| Destroy resources | `terraform destroy` |
| List state resources | `terraform state list` |
| Create workspace | `terraform workspace new dev` |
| Import resource | `terraform import` |

---

## 💡 TIPS

- Always run `terraform plan` before `apply`.  
- Commit `.tf` files but exclude `terraform.tfstate`.  
- Use modules for reusability and version control.  
- Use `depends_on` for explicit dependencies.  
- Version-lock your providers and backends.

---

**Created for:** Terraform and Infrastructure as Code workflows  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #terraform #iac #devops #googlecloud #azure #automation
