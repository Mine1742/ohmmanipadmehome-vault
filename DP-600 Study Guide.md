# DP-600: Implementing Analytics Solutions Using Microsoft Fabric
## Study Guide — Fabric Analytics Engineer Associate

[[Azure Hub]] | prompted by the Capital Area Food Bank BI Analyst application, 2026-08-05

---

## Table of Contents
1. [Exam Overview](#exam-overview)
2. [Where You Already Stand](#where-you-already-stand)
3. [Study Timeline](#study-timeline)
4. [Skills Measured Breakdown](#skills-measured-breakdown)
5. [Study Resources](#study-resources)
6. [Hands-On Lab Plan](#hands-on-lab-plan)
7. [Exam Day Logistics](#exam-day-logistics)

---

## Exam Overview

**Exam Code:** DP-600
**Certification:** Microsoft Certified: Fabric Analytics Engineer Associate
**Skills measured version:** as of 2026-07-21 (three-domain outline — older prep material still floating around online references an outdated four-domain version with a separate "Plan" area; ignore those)
**Exam Cost:** $165 USD
**Duration:** 100 minutes
**Passing Score:** 700/1000
**Languages:** English, Japanese, Chinese (Simplified), German, French, Spanish, Portuguese (Brazil)
**Format:** Proctored, may include interactive components

### What This Certification Validates
Subject-matter expertise in designing, creating, and managing analytical assets — semantic models, warehouses, lakehouses — including querying/analyzing data with SQL, KQL, and DAX, and partnering with architects/analysts/engineers/admins on business requirements.

Source: [Official DP-600 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/dp-600), [Exam page](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-600/)

---

## Where You Already Stand

Coming into this with real advantages from current experience — this isn't a cold start:

- **Power BI** — built dashboards/presentations at Just AJs Foods. Semantic modeling and DAX in DP-600 build directly on this.
- **SQL** — used in the CRM integration project and generally. Covers most of the "Query and analyze data by using SQL" sub-skill already.
- **PowerShell / automation mindset** — from Azure Monitor scripting at DENPRO; transfers to Fabric's deployment-pipeline and version-control concepts.
- **Python + data migration** — the Vir-Gin project (unstructured data → PostgreSQL) is conceptually identical to Fabric's "prepare data" domain (transform, deduplicate, resolve nulls, convert types).
- **AZ-900 + AZ-104** — already fluent in Microsoft cert exam format and cloud fundamentals.

**Genuinely new territory:**
- KQL (Kusto Query Language) — no prior exposure.
- Fabric-specific mechanics: OneLake, Direct Lake mode, deployment pipelines, workspace/item-level security, XMLA endpoint deployment.
- Deeper DAX (calculation groups, dynamic format strings, field parameters, iterators/windowing functions) beyond whatever you've used in basic Power BI reports.

---

## Study Timeline

Given the existing SQL/Power BI/Python base, this is closer to an **8-week** plan than the 12-16 weeks a complete beginner would need. Adjust to your actual pace — the DENPRO job and job search take priority.

- **Weeks 1-2 — Prepare data (45-50% of the exam, so start here):** OneLake, Lakehouse vs. Warehouse, Dataflow Gen2, star schema design, data transformation (dedupe, nulls, type conversion). Do the Vir-Gin recreation lab (below) during this window.
- **Weeks 3-4 — Query and analyze data:** SQL in Fabric (mostly review), then KQL from scratch, then DAX query view basics.
- **Weeks 5-6 — Implement and manage semantic models (25-30%):** storage modes, Direct Lake configuration, relationships/composite models, calculation groups, performance tuning.
- **Week 7 — Maintain a data analytics solution (25-30%):** security/governance (workspace and item-level access, sensitivity labels), version control, deployment pipelines, .pbip/.pbit/.pbids files.
- **Week 8 — Practice assessment + review:** take the official practice assessment, drill weak domains, review the change log for anything that shifted close to your exam date.

---

## Skills Measured Breakdown

### Maintain a data analytics solution (25–30%)

**Implement security and governance**
- Workspace-level access controls
- Item-level access controls
- Row-level, column-level, object-level, and file-level access control
- Apply sensitivity labels to items
- Endorse items

**Maintain the analytics development lifecycle**
- Configure version control for a workspace
- Create and manage a Power BI Desktop project (.pbip)
- Create and configure deployment pipelines
- Perform impact analysis of downstream dependencies (lakehouses, warehouses, dataflows, semantic models)
- Deploy and manage semantic models via the XMLA endpoint
- Create/update reusable assets: .pbit, .pbids, shared semantic models

### Prepare data (45–50% — the largest domain, prioritize accordingly)

**Get data**
- Create a data connection
- Discover data via OneLake catalog and Real-Time hub
- Ingest or access data as needed
- Choose between data stores
- Implement OneLake integration for Eventhouse and semantic models

**Transform data**
- Create views, functions, stored procedures
- Enrich data (new columns/tables)
- Implement a star schema for a lakehouse or warehouse
- Denormalize data
- Aggregate data
- Merge/join data
- Identify and resolve duplicate, missing, or null data
- Convert column data types
- Filter data

**Query and analyze data**
- Visual Query Editor
- SQL
- KQL
- DAX

### Implement and manage semantic models (25–30%)

**Design and build semantic models**
- Choose a storage mode
- Implement a star schema for a semantic model
- Relationships (bridge tables, many-to-many)
- DAX calculations: variables, functions, iterators, table filtering, windowing, information functions
- Calculation groups, dynamic format strings, field parameters
- Large semantic model storage format — when to use it
- Composite models

**Optimize enterprise-scale semantic models**
- Query and report visual performance improvements
- DAX performance tuning
- Configure Direct Lake, including default fallback and refresh behavior
- Direct Lake on OneLake vs. Direct Lake on SQL analytics endpoint
- Incremental refresh

---

## Study Resources

| Resource | Link |
|---|---|
| Official study guide | [learn.microsoft.com DP-600 study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/dp-600) |
| Exam page / scheduling | [DP-600 exam page](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-600/) |
| Free practice assessment | Linked from the exam page (assessmentId=90) |
| Exam sandbox (UI walkthrough) | [aka.ms/examdemo](https://aka.ms/examdemo) |
| Microsoft Fabric docs | [learn.microsoft.com/fabric](https://learn.microsoft.com/en-us/fabric/) |
| Lakehouse overview | [What is a lakehouse?](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview) |
| Data warehousing overview | [What is data warehousing?](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing) |
| Video prep | [Exam Readiness Zone — DP-600](https://learn.microsoft.com/en-us/shows/exam-readiness-zone/preparing-for-dp-600-plan-implement-and-manage-a-solution-for-data-analytics), [Data Exposed](https://learn.microsoft.com/en-us/shows/data-exposed/) |
| Community | [Analytics on Azure — Tech Community](https://techcommunity.microsoft.com/t5/analytics-on-azure/bd-p/AnalyticsonAzureDiscussion), [Microsoft Fabric Blog](https://www.microsoft.com/microsoft-fabric/blog/) |

---

## Hands-On Lab Plan

Fabric has a free trial capacity tied to a Power BI account — no employer sign-off needed.

1. **Recreate the Vir-Gin Memorabilia project inside Fabric.** Land the same Google Sheets/Excel source data as a Bronze table in a Lakehouse, clean/dedupe/type-convert it into Silver via Dataflow Gen2, aggregate into a Gold table, then build a Power BI report against it using **Direct Lake mode**. This single project touches Get Data, Transform Data, star schema design, and Direct Lake configuration — most of the "Prepare data" domain plus a chunk of "Implement semantic models."
2. **Practice KQL** against a sample Eventhouse (Fabric's real-time analytics sample data works fine) since this is the one query language with zero prior exposure.
3. **Build one semantic model with calculation groups and a field parameter**, then deliberately misconfigure Direct Lake fallback behavior once to see what triggers it — the exam tests understanding of *why* fallback happens, not just the happy path.
4. **Set up a deployment pipeline** (Dev → Test → Prod) for the practice workspace and configure workspace/item-level security — the "Maintain" domain is easy to under-practice since it's not flashy, but it's 25-30% of the exam.

Once any of this is real (even a small version), report back — `Resume - Master.md` and the CAFB application materials get updated with genuine, specific language at that point, not before.

---

## Exam Day Logistics

- Register with a personal MSA account, not a work/school AAD account — org accounts lose exam history if you leave the organization.
- 100 minutes, ~40-60 items, scaled score out of 1000, need 700 to pass.
- Failed attempts can be retaken 24 hours later (longer waits for subsequent retakes).
- Given the domain weighting, if time-constrained during study, prioritize **Prepare data (45-50%)** over the other two domains — it's worth almost as much as the other two combined.
