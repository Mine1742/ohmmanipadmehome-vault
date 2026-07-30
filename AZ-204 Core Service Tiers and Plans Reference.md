
### **AZ-204 Core Service Tiers and Plans Reference**

The following tables summarize the service tiers and plans most relevant to the AZ-204 exam, focusing on the trade-offs between cost, performance, and functionality required for production-ready solutions.

---

### **1. Develop Azure Compute Solutions**

#### **Azure App Service Plans**

The **App Service Plan** represents the compute capacity (the "gym membership"), while the **App** is the code (the "workout").

|Tier Group|Tier Name|Key Exam Characteristics|
|:--|:--|:--|
|**Shared**|**Free (F1), Shared**|Shared CPU; **no Linux support**; no custom domains/SSL; apps can "sleep".|
|**Dedicated**|**Basic (B1–B3)**|**Dedicated VM**; supports custom domains and SSL; **manual scaling only**; no deployment slots.|
|**Production**|**Standard (S1–S3)**|**Minimum production tier**; unlocks **Autoscaling**, **Deployment Slots** (staging/swap), and daily backups.|
|**Performance**|**Premium (P1–P3 v3)**|Faster CPUs, more memory, **Zone Redundancy**, and VNet integration at scale.|
|**Isolated**|**Isolated (I1–I3)**|Runs in an **App Service Environment (ASE)**; full network isolation; no "noisy neighbors"; highest cost.|

#### **Azure Functions Hosting**

Every Function App requires a **general-purpose Azure Storage account** to operate.

|Plan Name|Best Use Case|Billing & Scaling Logic|
|:--|:--|:--|
|**Consumption**|Spiky/unpredictable traffic|**True serverless**; pay only for execution time/memory; **scales to zero**; may experience **"cold starts"**.|
|**Premium**|Performance-sensitive apps|Uses **"warm instances"** to avoid cold starts; supports **VNet integration** and longer timeouts.|
|**Dedicated**|Existing resources|Runs on a standard **App Service Plan** at **no extra cost** if capacity is available.|

---

### **2. Develop for Azure Storage**

#### **Azure Cosmos DB Capacity Modes**

Cosmos DB costs are normalized into **Request Units (RUs)**, which abstract CPU, memory, and IOPS.

|Mode|Consistency & Cost Logic|Ideal Scenario|
|:--|:--|:--|
|**Provisioned**|Pay for a **guaranteed RU/s** hourly, even if idle.|Predictable, high-scale traffic with strict SLAs.|
|**Serverless**|Pay **per RU consumed**; 50GB storage limit per container.|Bursty, unpredictable, or low-volume traffic.|

#### **Azure Blob Storage Access Tiers**

Storage costs are balanced against access costs; cheaper storage equals more expensive access.

|Tier|Minimum Duration|Access & Cost Profile|
|:--|:--|:--|
|**Hot**|N/A|Optimized for **frequently accessed** data; highest storage cost, lowest access cost.|
|**Cool**|30 Days|Optimized for **infrequently accessed** data; lower storage cost, higher access cost.|
|**Cold**|90 Days|Optimized for **rarely accessed** data.|
|**Archive**|180 Days|**Lowest cost**; data is **offline** and requires **"rehydration"** (hours) to read.|

---

### **3. Connect to and Consume Azure Services**

#### **Azure API Management (APIM)**

APIM acts as a **facade/front door** for backend services, handling authentication and rate limiting.

|Tier|Target Use Case|Key Limitations / Features|
|:--|:--|:--|
|**Consumption**|Lightweight/Serverless|Pay-per-call; **scales to zero**; no Developer Portal or VNet support.|
|**Developer**|Full testing|Full feature set but **no SLA**; single unit only.|
|**Standard**|Production|Includes VNet integration (external mode).|
|**Premium**|Enterprise|Supports **multi-region**, **availability zones**, and internal VNet integration.|

#### **Azure Service Bus & Event Hub Tiers**

Choosing depends on whether you need **reliable messaging** (Service Bus) or **high-throughput ingestion** (Event Hubs).

|Service|Tier|Critical Differentiators|
|:--|:--|:--|
|**Service Bus**|**Basic**|**Queues only**; no topics, no sessions, no transactions.|
|**Service Bus**|**Standard**|Unlocks **Topics (Pub/Sub)** and sessions.|
|**Service Bus**|**Premium**|Fixed pricing; dedicated capacity; **100MB messages**; VNet support.|
|**Event Hubs**|**Standard**|Up to 20 consumer groups; **Kafka compatibility**; 7-day retention.|
|**Event Hubs**|**Premium**|**Dedicated resources**; up to 90-day retention; measured in **Processing Units (PUs)**.|

---

### **4. Security and Caching**

#### **Azure Cache for Redis**

An in-memory store for high-throughput, low-latency requirements.

|Tier|Best For|Exclusive Features|
|:--|:--|:--|
|**Basic**|Dev/Test|Single node; **no replication**; no SLA; data lost on restart.|
|**Standard**|Entry Production|Two nodes (Primary + Replica); **automatic failover**.|
|**Premium**|High Scale|**Persistence** (RDB/AOF), **Clustering**, and VNet integration.|

#### **Azure Key Vault**

Centralized management of secrets, keys, and certificates.

| Tier         | Protection Level   | Key Feature                                                                  |
| :----------- | :----------------- | :--------------------------------------------------------------------------- |
| **Standard** | Software-protected | Sufficient for most production secrets and keys.                             |
| **Premium**  | **HSM-backed**     | Keys stored in **Hardware Security Modules** (FIPS 140-2 Level 2 compliant). |