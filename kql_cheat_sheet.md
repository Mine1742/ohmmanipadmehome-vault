# KQL (Kusto Query Language) Cheat Sheet

Kusto Query Language (KQL) is used to query Azure Data Explorer, Log Analytics, Microsoft Sentinel, and Application Insights.

---

## 🧠 Basics

- **Statements end with a pipe `|`**
- **Case-sensitive**
- Queries work on **tables** and produce **tabular results**

---

## 📂 Basic Syntax

```kql
TableName
| take 10
| where Column == "value"
| project Column1, Column2
```

---

## 🔍 Filtering Data

| Operator | Description               |
|----------|---------------------------|
| `==`     | Equal                     |
| `!=`     | Not equal                 |
| `=~`     | Case-insensitive equal    |
| `contains` | String contains         |
| `startswith`, `endswith` | String match |
| `has`, `!has` | Tokenized match     |
| `in`     | Matches a list of values |

```kql
SecurityEvent
| where AccountType == "User"
| where TimeGenerated > ago(1d)
```

---

## 📊 Project & Summarize

### `project`: Select columns
```kql
Table
| project TimeGenerated, Computer, EventID
```

### `summarize`: Aggregation
```kql
Table
| summarize Count = count() by EventID
```

### Common Aggregates:
- `count()`
- `sum(Column)`
- `avg(Column)`
- `max()`, `min()`
- `countif(condition)`

---

## ⏱ Time Filtering

```kql
| where TimeGenerated > ago(24h)
| where TimeGenerated between (datetime(2024-01-01) .. datetime(2024-01-31))
```

---

## 📌 Sorting and Limiting

```kql
| order by TimeGenerated desc
| take 5
```

---

## 🔁 Joins

```kql
TableA
| join kind=inner TableB on CommonField
```

| Join Type     | Description               |
|---------------|---------------------------|
| `inner`       | Match in both             |
| `leftouter`   | All from left, matches from right |
| `rightouter`  | All from right, matches from left |
| `fullouter`   | All records from both     |
| `anti`        | Records only in left      |
| `innerunique` | 1:1 match only            |

---

## 🧱 Let Statements (Aliases)

```kql
let recent = Table | where TimeGenerated > ago(1d);
recent
| summarize count() by EventID
```

---

## 🧩 Useful Operators

| Operator     | Purpose                                 |
|--------------|------------------------------------------|
| `extend`     | Create new calculated columns            |
| `parse`      | Extract fields using patterns or regex   |
| `mv-expand`  | Flatten arrays or multi-value fields     |
| `top`        | Return top N rows by value               |
| `render`     | Visualize (e.g., piechart, barchart)     |

---

## 📈 Visualizations

```kql
| summarize count() by bin(TimeGenerated, 1h)
| render timechart
```

- `render barchart`
- `render piechart`
- `render columnchart`

---

## 🔐 Security Log Example

```kql
SecurityEvent
| where EventID == 4625
| summarize FailedAttempts = count() by Account, bin(TimeGenerated, 1h)
| order by FailedAttempts desc
```

---

## 📚 References

- [KQL Docs – Microsoft](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)
- [KQL Quick Reference](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/log-queries)
