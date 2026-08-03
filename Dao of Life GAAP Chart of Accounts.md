#daooflife

[[Dao of Life Hub]]

Full GAAP chart of accounts synced from Drive on 2026-08-03 (originals: https://drive.google.com/file/d/1kLq0VAXa8-CM-K52PWzKBdJjV_h-WA2m/view?usp=drivesdk and https://drive.google.com/file/d/1Q8khvkVrHkEHzdIpL5Fad8O5UA82GB3w/view?usp=drivesdk). Behind the tracking-dimensions summary in [[Dao of Life Finances]].

# Dao of Life — GAAP‑Ready Chart of Accounts (COA) & Tracking Framework

> Designed for nonprofit **fund accounting** under **FASB ASU 2016‑14** (two net asset classes: **With Donor Restrictions** and **Without Donor Restrictions**). Works with QuickBooks/Xero by using **Classes** for function and **Location** for branches; add **Projects/Grants** for restrictions.

---

## A) Tracking Dimensions (Strongly Recommended)
- **Class (Function):** `PG-Garden`, `PG-MutualAid`, `PG-Education`, `SUP-MgmtGeneral`, `SUP-Fundraising`  
- **Location (Geography):** `LOC-MD-HQ`, `LOC-MI-Branch`  
- **Project/Grant (Restrictions):** `GR-2025-XYZ`, `RSTR-Garden`, `RSTR-Education`, `TIME-Release-YYYY`

> Enter **every revenue and expense** with Class; use Location for branch; use Project/Grant for restricted funds. Use journal entries to record **Net Assets Released from Restrictions (NAR)** when purpose/time is met.

---

## B) Account Numbering Scheme
- **1xxx** Assets  
- **2xxx** Liabilities  
- **3xxx** Net Assets  
- **4xxx–5xxx** Revenue/Support & Releases  
- **6xxx–7xxx** Expenses (natural classification)  
- **8xxx** Other Income/Expense  
- **9xxx** Unrelated Business Income (UBI) & Direct Costs

---

## C) Detailed COA (Starter Set)

### 1xxx — Assets
- **1000** Assets (Roll‑up / Do Not Post)
- **1100** Cash & Cash Equivalents
  - **1110** Operating Checking — MD
  - **1115** Operating Checking — MI
  - **1120** Savings / Reserve
  - **1130** Petty Cash
- **1200** Receivables
  - **1210** Pledges Receivable (Net)
  - **1220** Grants Receivable
  - **1230** Other Receivables
- **1300** Prepaid Expenses
- **1400** Inventory — Program Supplies
- **1500** Property & Equipment
  - **1510** Land
  - **1520** Buildings & Improvements
  - **1530** Leasehold Improvements
  - **1540** Furniture & Equipment
  - **1550** Accumulated Depreciation (Contra)
- **1600** Security Deposits

### 2xxx — Liabilities
- **2000** Liabilities (Roll‑up / DNP)
- **2100** Accounts Payable
- **2200** Accrued Expenses
  - **2210** Accrued Payroll
  - **2220** Payroll Taxes Payable
  - **2230** Sales/Use Tax Payable (if applicable)
- **2300** Deferred Revenue (Exchange/Events)
- **2400** Deferred Rent / Lease Liability
- **2500** Notes Payable

### 3xxx — Net Assets
- **3000** Net Assets — Without Donor Restrictions
  - **3010** Board‑Designated Reserve (WDR)
  - **3020** Board‑Designated Garden Expansion (WDR)
  - **3090** Net Investment in Property & Equipment (WDR)
- **3100** Net Assets — With Donor Restrictions

### 4xxx — Contributions, Grants & Earned Revenue
- **4000** Contributions — Without Donor Restrictions
  - **4010** Individual Contributions
  - **4020** Board/Staff Contributions
  - **4030** Corporate Contributions
- **4100** Contributions — With Donor Restrictions
  - **4110** Restricted — Garden Program
  - **4120** Restricted — Mutual Aid
  - **4130** Restricted — Education
  - **4140** Restricted — Capital/Facilities
- **4200** Foundation & DAF Grants
  - **4210** Foundation Grants (WDR)
  - **4220** Foundation Grants (With Restrictions)
  - **4230** DAF Grants
- **4300** Government Grants/Contracts (specify exchange vs contribution)
- **4400** Program Service Revenue (Workshops/Events)
- **4500** Special Events Revenue (Gross)
  - **4510** Less: Direct Event Costs (Contra Revenues or show separately in Expenses — choose one policy and be consistent)
- **4600** In‑Kind Contributions — Goods
- **4610** In‑Kind Contributions — Services (GAAP-recognized; donors cannot deduct value of services)
- **4700** Investment & Interest Income

### 5xxx — Net Assets Released from Restrictions (NAR)
- **5000** NAR — Purpose Restrictions Satisfied
- **5010** NAR — Time Restrictions Expired
- **5020** NAR — Capital Assets Placed in Service

### 6xxx — Expenses (Natural Classification)
- **6000** Salaries & Wages
- **6100** Payroll Taxes
- **6150** Employee Benefits
- **6200** Professional & Contracted Services
- **6300** Supplies & Materials
  - **6310** Garden Supplies & Seeds
  - **6320** Food Distribution Supplies
- **6400** Occupancy (Rent, Utilities, Maintenance)
- **6500** Insurance
- **6600** Printing, Publications & Advertising
- **6700** Postage & Shipping
- **6800** Technology & Software
- **6900** Travel, Meetings & Training
- **6950** Volunteer Support (Non‑cash)
- **7000** Depreciation & Amortization
- **7100** Grants & Assistance to Individuals (Mutual Aid)
- **7200** Outreach & Education
- **7300** Dues & Subscriptions
- **7400** Bank & Merchant Fees
- **7500** Fundraising Expenses (if tracked separately by nature)

### 8xxx — Other Income/Expense
- **8000** Other Income
- **8100** Interest Expense
- **8200** Miscellaneous Expense

### 9xxx — Unrelated Business Income (UBI)
- **9000** UBI — Gross Receipts
- **9010** UBI — Direct Expenses
- **9020** UBI — Net (Calculated/Reporting)

---

## D) Functional Expense Statement — Mapping Guide
Record each transaction with a **Class** to enable the Statement of Functional Expenses:
- **Programs:** PG‑Garden, PG‑MutualAid, PG‑Education  
- **Supporting:** SUP‑MgmtGeneral, SUP‑Fundraising

Example: A seed purchase for the Michigan garden = Account **6310** (Garden Supplies) + Class **PG‑Garden** + Location **LOC‑MI‑Branch** + Project **RSTR‑Garden** (if restricted).

---

## E) Journal Entry Example — Release from Restriction
When a restricted garden grant is spent:

1. **Dr.** 5000 NAR — Purpose Satisfied (WDR) — Class to program used (e.g., PG‑Garden)  
2. **Cr.** 3100 Net Assets — With Donor Restrictions

---

## F) Naming Conventions
- **Classes:** `PG-<>` for programs, `SUP-<>` for supporting.  
- **Locations:** `LOC-STATE-Branch`.  
- **Grants/Projects:** `GR-YYYY-ShortName` or `RSTR-Program` for purpose restrictions.

---

*This starter COA can be expanded as operations grow. Stay consistent, avoid duplicate or overlapping accounts, and document any changes in a COA log.*


---

## Import CSV (Dao_of_Life_Chart_of_Accounts_Import.csv)

```csv
Number,Name,Type,Notes
1110,Operating Checking — MD,Bank,Cash & Cash Equivalents
1115,Operating Checking — MI,Bank,Cash & Cash Equivalents
1210,Pledges Receivable (Net),Other Current Asset,Allow for doubtful accounts
1220,Grants Receivable,Other Current Asset,
1300,Prepaid Expenses,Other Current Asset,
1400,Inventory — Program Supplies,Other Current Asset,
1510,Land,Fixed Asset,
1520,Buildings & Improvements,Fixed Asset,
1540,Furniture & Equipment,Fixed Asset,
1550,Accumulated Depreciation (Contra),Fixed Asset,Contra-asset
2100,Accounts Payable,Accounts Payable,
2210,Accrued Payroll,Other Current Liability,
2220,Payroll Taxes Payable,Other Current Liability,
2300,Deferred Revenue,Other Current Liability,Exchange/Events
3000,Net Assets — Without Donor Restrictions,Equity,
3100,Net Assets — With Donor Restrictions,Equity,
4010,Individual Contributions (WDR),Income,
4100,Contributions — With Donor Restrictions,Income,Purpose/Time restrictions
4210,Foundation Grants (WDR),Income,
4220,Foundation Grants (Restricted),Income,
4230,DAF Grants,Income,
4300,Program Service Revenue,Income,Workshops/fees
4500,Special Events Revenue (Gross),Income,
4510,Direct Event Costs (Contra),Income,If netting per policy
4600,In-Kind Contributions — Goods,Income,Describe only in receipts
4610,In-Kind Contributions — Services,Income,GAAP-recognized only
4700,Investment & Interest Income,Income,
5000,Net Assets Released — Purpose,Income,WDR
5010,Net Assets Released — Time,Income,WDR
5020,Net Assets Released — Capital Placed in Service,Income,WDR
6000,Salaries & Wages,Expense,
6100,Payroll Taxes,Expense,
6150,Employee Benefits,Expense,
6200,Professional & Contracted Services,Expense,
6310,Garden Supplies & Seeds,Expense,
6320,Food Distribution Supplies,Expense,
6400,"Occupancy (Rent, Utilities)",Expense,
6500,Insurance,Expense,
6600,"Printing, Publications & Advertising",Expense,
6700,Postage & Shipping,Expense,
6800,Technology & Software,Expense,
6900,"Travel, Meetings & Training",Expense,
6950,Volunteer Support (Non-cash),Expense,
7000,Depreciation & Amortization,Expense,
7100,Grants & Assistance to Individuals (Mutual Aid),Expense,
7200,Outreach & Education,Expense,
7300,Dues & Subscriptions,Expense,
7400,Bank & Merchant Fees,Expense,
7500,Fundraising Expenses,Expense,
8000,Other Income,Other Income,
8100,Interest Expense,Other Expense,
9000,Unrelated Business Income (UBI) — Gross,Income,
9010,UBI — Direct Expenses,Expense,

```

