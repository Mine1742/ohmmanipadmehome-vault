#google #cloud #shell
[[Google Hub]]
initiate GCS:

gcloud init
 gcloud config set project PROJECT_ID
gcloud auth login

[`gcloud auth login`](https://cloud.google.com/sdk/gcloud/reference/auth/login)|Authorize with a user account without setting up a configuration.
[`gcloud auth activate-service-account`](https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account)|Authorize with a service account instead of a user account.  Useful for authorizing non-interactively and without a web browser.
[`gcloud config [COMMAND]`](https://cloud.google.com/sdk/gcloud/reference/config)  <br>[`gcloud config configurations [COMMAND]`](https://cloud.google.com/sdk/gcloud/reference/config/configurations)|Create and manage gcloud CLI configurations and properties.

Authorize the gcloud CLI:
user account or a service account
 
| [`gcloud init`](https://cloud.google.com/sdk/gcloud/reference/init)             | Authorizes access and performs other common setup steps. |
| ------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [`gcloud auth login`](https://cloud.google.com/sdk/gcloud/reference/auth/login) | Authorizes access only.                                  |

gcloud init --console-only

- If you already have an access token, use one of the following methods to pass the access token to the gcloud CLI:
    
    - Store the access token in a file and set its path through the [--access-token-file](https://cloud.google.com/sdk/gcloud/reference#--access-token-file) flag.
    - Store the access token in a file and set its path in the [auth/access_token_file](https://cloud.google.com/sdk/gcloud/reference/config/set#:%7E:text=access_token_file,no%20other%20information.) property.
    - Set the `CLOUDSDK_AUTH_ACCESS_TOKEN` environment variable to the access token value.

List accounts:
gcloud auth list

Switch the active account:
gcloud config set account ACCOUNT
	where `[ACCOUNT]` is the full email address of the account.







To enable the **Cloud Build API** in your Google Cloud project, follow these steps:

---

### 🔧 Option 1: Enable via Google Cloud Console (UI)

1. Go to the **Cloud Build API page**: 👉 [https://console.cloud.google.com/apis/library/cloudbuild.googleapis.com](https://console.cloud.google.com/apis/library/cloudbuild.googleapis.com)
    
2. Select your project from the **project selector dropdown** (top bar).
    
3. Click the **"Enable"** button.
    

---

### 🖥️ Option 2: Enable via `gcloud` CLI

Make sure you’ve initialized `gcloud` and selected your project:

```bash
gcloud init
```

Then run:

```bash
gcloud services enable cloudbuild.googleapis.com
```

> 💡 You can specify a project explicitly:

```bash
gcloud services enable cloudbuild.googleapis.com --project=your-project-id
```

---

Let me know if you want help setting up a Cloud Build trigger or deploying from GitHub!



Build the image:
gcloud builds submit --tag gcr.io/certtracker-454718/certtrack-app

**Deploy to Cloud Run**
gcloud run deploy certtrack-service --image gcr.io/certtracker-454718/certtrack-app --region us-central1 --platform managed --allow-unauthenticated --set-env-vars=NOTION_DATABASE_ID_LOGIN=1b110be901fb8121af11e4ec9233014f,NOTION_DATABASE_ID_STU_INFO=1b110be9-01fb-81e6-902b-d0ef6adfd7a4,NOTION_DATABASE_ID_CERT_ATTEMPTS=1b110be901fb819ab84ae3d334f1cb35,NOTION_DATABASE_ID_CERTS=1b110be9-01fb-81f4-b17e-dff4975f8bbf,NOTION_DATABASE_ID_PROGRAMS=1b110be9-01fb-81f1-9e83-cb1c1cd3ba09,NOTION_DATABASE_ID_ADMIN_ACTIVITY=1bc10be901fb8089808dc4c63575f537,NOTION_SECRET=ntn_e4494787067bhZc8uWpN6Tgs94OJ9dUolTuIOrjRZEgelH,SECRET_KEY=supersecretflaskkey,FLASK_APP=app.py,FLASK_ENV=development


`gcloud run deploy` command will output a URL.


on code edit:
gcloud builds submit --tag gcr.io/certtracker-454718/certtrack-app

gcloud run deploy certtrack-service \
  --image gcr.io/certtracker-454718/certtrack-app \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars=NOTION_DATABASE_ID_LOGIN=1b110be901fb8121af11e4ec9233014f,NOTION_DATABASE_ID_STU_INFO=1b110be9-01fb-81e6-902b-d0ef6adfd7a4,NOTION_DATABASE_ID_CERT_ATTEMPTS=1b110be901fb819ab84ae3d334f1cb35,NOTION_DATABASE_ID_CERTS=1b110be9-01fb-81f4-b17e-dff4975f8bbf,NOTION_DATABASE_ID_PROGRAMS=1b110be9-01fb-81f1-9e83-cb1c1cd3ba09,NOTION_DATABASE_ID_ADMIN_ACTIVITY=1bc10be901fb8089808dc4c63575f537,NOTION_SECRET=ntn_e4494787067bhZc8uWpN6Tgs94OJ9dUolTuIOrjRZEgelH,SECRET_KEY=supersecretflaskkey,FLASK_APP=app.py,FLASK_ENV=development