# ☁️ Google Cloud Shell & SDK Cheat Sheet

Essential `gcloud` commands and workflows for managing Google Cloud resources, deployments, and automation directly from Cloud Shell.

---

## 🚀 AUTHENTICATION & PROJECT SETUP

```bash
gcloud auth login                          # Authenticate user account
gcloud auth list                           # Show active credentials
gcloud config list                         # View current configuration
gcloud projects list                       # List all accessible projects
gcloud config set project PROJECT_ID       # Set default project
gcloud config set compute/region us-east1  # Set default region
gcloud config set compute/zone us-east1-b  # Set default zone
```

---

## 🧱 COMPUTE ENGINE

```bash
gcloud compute instances list
gcloud compute instances create my-vm --zone=us-east1-b --machine-type=e2-medium --image-family=debian-12 --image-project=debian-cloud
gcloud compute ssh my-vm --zone=us-east1-b
gcloud compute scp localfile.txt my-vm:~/ --zone=us-east1-b
gcloud compute instances stop my-vm
gcloud compute instances delete my-vm
```

---

## 🐳 CLOUD RUN

```bash
gcloud run deploy my-service --source . --region=us-east1 --platform=managed --allow-unauthenticated
gcloud run services list
gcloud run services describe my-service --region=us-east1
gcloud run revisions list --service my-service
gcloud run services delete my-service --region=us-east1
```

---

## 🧮 CLOUD SQL

```bash
gcloud sql instances create my-db --tier=db-f1-micro --region=us-east1
gcloud sql instances list
gcloud sql users set-password postgres --instance=my-db --password="StrongPassword123"
gcloud sql connect my-db --user=postgres
gcloud sql databases create dao_of_life --instance=my-db
gcloud sql export sql my-db gs://my-bucket/export.sql.gz --database=dao_of_life
```

---

## 🗄️ CLOUD STORAGE

```bash
gcloud storage buckets list
gcloud storage buckets create gs://my-data-bucket --location=us-east1
gcloud storage cp localfile.txt gs://my-data-bucket/
gcloud storage cp -r images/ gs://my-data-bucket/images/
gcloud storage ls gs://my-data-bucket
gcloud storage rm gs://my-data-bucket/oldfile.txt
```

### **gsutil Equivalents**
```bash
gsutil ls gs://my-data-bucket
gsutil cp file.txt gs://my-data-bucket/
gsutil -m rsync -r ./localdir gs://my-data-bucket/
```

---

## 🔐 IAM & SERVICE ACCOUNTS

```bash
gcloud iam service-accounts list
gcloud iam service-accounts create dao-service --display-name="DAO Service Account"
gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:dao-service@PROJECT_ID.iam.gserviceaccount.com" --role="roles/editor"
gcloud iam service-accounts keys create key.json --iam-account=dao-service@PROJECT_ID.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="key.json"
```

---

## 🧩 NETWORKING

```bash
gcloud compute networks list
gcloud compute networks create dao-vpc --subnet-mode=custom
gcloud compute networks subnets create dao-subnet --network=dao-vpc --region=us-east1 --range=10.0.0.0/24
gcloud compute firewall-rules create allow-http --allow tcp:80 --network=dao-vpc
```

---

## 📦 CLOUD BUILD & CONTAINERS

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/my-app
gcloud container images list
gcloud container clusters list
gcloud container clusters create dao-cluster --num-nodes=2 --zone=us-east1-b
gcloud container clusters get-credentials dao-cluster --zone=us-east1-b
kubectl get pods
```

---

## 💰 BILLING & QUOTAS

```bash
gcloud beta billing accounts list
gcloud beta billing accounts describe ACCOUNT_ID
gcloud beta billing projects link PROJECT_ID --billing-account=ACCOUNT_ID
gcloud compute regions describe us-east1 --format="value(quotas)"
```

---

## ⚙️ LOGGING & MONITORING

```bash
gcloud logging read "resource.type=gce_instance" --limit=10
gcloud logging logs list
gcloud monitoring metrics list
gcloud monitoring policies list
```

---

## 🧾 DEPLOYMENT MANAGER & INFRASTRUCTURE

```bash
gcloud deployment-manager deployments list
gcloud deployment-manager deployments create my-stack --config=config.yaml
gcloud deployment-manager deployments delete my-stack
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| Login & configure project | `gcloud auth login && gcloud config set project PROJECT_ID` |
| Create VM | `gcloud compute instances create my-vm` |
| Deploy Cloud Run service | `gcloud run deploy SERVICE_NAME --source .` |
| Create Cloud SQL instance | `gcloud sql instances create my-db` |
| Copy to GCS | `gcloud storage cp file.txt gs://bucket/` |
| Create service account | `gcloud iam service-accounts create NAME` |
| Submit Cloud Build | `gcloud builds submit --tag gcr.io/PROJECT_ID/image` |

---

## 💡 TIPS
- Cloud Shell comes preloaded with `gcloud`, `kubectl`, `bq`, and `gsutil`.
- Use `--format=json` or `--format=table` for readable outputs.
- Save frequently used configurations as named configs:
  ```bash
  gcloud config configurations create dev
  gcloud config configurations activate dev
  ```
- Combine with `jq` to parse JSON output:
  ```bash
  gcloud compute instances list --format=json | jq '.[].name'
  ```

---

**Created for:** Google Cloud engineers and DevOps workflows  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #gcloud #cloudshell #googlecloud #cloudrun #devops #automation
