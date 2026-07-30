
![[Pasted image 20260213114918.png]]
![[Pasted image 20260213115102.png]]
![[Pasted image 20260213115234.png]]


# Azure Monitor

Think of Azure Monitor as the **central nervous system for observability in Azure**. It's the unified platform that collects, analyzes, and acts on telemetry data from your Azure resources, applications, and infrastructure — all in one place.

---

## The Core Concept

When something goes wrong in production — or before it does — you need three things: **metrics** (what's happening right now), **logs** (what happened and why), and **alerts** (tell me when something is wrong). Azure Monitor is the platform that delivers all three, and it pulls data from virtually every Azure service automatically.

The data flow looks like this:

```
Data Sources                  Azure Monitor                    Actions
────────────                  ─────────────                    ───────
Azure Resources    ──────►   Metrics Store    ──────►   Dashboards
Applications       ──────►   Log Analytics    ──────►   Alerts
Virtual Machines   ──────►   (Workspace)      ──────►   Autoscale
Containers         ──────►                    ──────►   Logic Apps
Custom Sources     ──────►                    ──────►   Webhooks
```

---

## The Two Data Stores

Everything in Azure Monitor flows into one of two stores, and understanding the distinction is foundational.

### Metrics Store

Metrics are **lightweight, numerical, time-series data points** collected at regular intervals. CPU percentage, memory usage, request count, response time — all metrics. They're stored in a dedicated time-series database optimized for fast retrieval and real-time dashboards.

Key characteristics of metrics:

- Collected automatically for most Azure resources with no configuration
- Retained for **93 days** by default
- Near real-time — typically available within 1 minute
- Queryable with simple filters and aggregations in the portal
- Cheaper to store and query than logs
- Great for alerting on current state

### Log Analytics Workspace

Logs are **rich, structured records of events** — not just numbers but full context about what happened. Application traces, dependency calls, exceptions, audit events, diagnostic data. Stored in a Log Analytics workspace and queried with **KQL (Kusto Query Language)**.

Key characteristics of logs:

- Require configuration to collect (diagnostics settings, agents, SDKs)
- Retention configurable from 30 days to 2 years (longer with archive tier)
- Slightly delayed — typically available within a few minutes
- Extremely powerful querying with KQL
- Can correlate data across multiple resources and services
- Foundation for Application Insights

---

## Data Collection Methods

### Diagnostic Settings

For Azure resources (App Service, Cosmos DB, Key Vault, etc.), you enable **Diagnostic Settings** to route platform logs and metrics to a destination. You choose what to collect and where to send it.

Destinations:

- **Log Analytics Workspace** — for querying and alerting
- **Azure Storage** — for long-term archival
- **Event Hubs** — for streaming to external systems (SIEM tools, Splunk, etc.)

```bash
# Enable diagnostic settings on a Cosmos DB account
az monitor diagnostic-settings create \
  --name myDiagSettings \
  --resource $(az cosmosdb show --name myaccount --resource-group myRG --query id -o tsv) \
  --workspace $(az monitor log-analytics workspace show \
      --workspace-name myworkspace \
      --resource-group myRG --query id -o tsv) \
  --logs '[
    {"category": "DataPlaneRequests", "enabled": true},
    {"category": "QueryRuntimeStatistics", "enabled": true},
    {"category": "PartitionKeyStatistics", "enabled": true}
  ]' \
  --metrics '[
    {"category": "Requests", "enabled": true}
  ]'
```

```bash
# Enable on App Service
az monitor diagnostic-settings create \
  --name appDiagSettings \
  --resource $(az webapp show --name myapp --resource-group myRG --query id -o tsv) \
  --workspace $(az monitor log-analytics workspace show \
      --workspace-name myworkspace \
      --resource-group myRG --query id -o tsv) \
  --logs '[
    {"category": "AppServiceHTTPLogs", "enabled": true},
    {"category": "AppServiceConsoleLogs", "enabled": true},
    {"category": "AppServiceAppLogs", "enabled": true}
  ]'
```

### Azure Monitor Agent

For virtual machines and on-premises servers, the **Azure Monitor Agent (AMA)** collects OS-level data — event logs, performance counters, syslog. It replaces the older Log Analytics agent and the Diagnostics extension. Configured via **Data Collection Rules (DCRs)** which define what to collect and where to send it.

```bash
# Create a data collection rule for Windows VMs
az monitor data-collection rule create \
  --resource-group myRG \
  --name myDCR \
  --location eastus \
  --data-flows '[{
    "streams": ["Microsoft-Event", "Microsoft-Perf"],
    "destinations": ["myworkspace"]
  }]' \
  --destinations '{
    "logAnalytics": [{
      "workspaceResourceId": "/subscriptions/.../myworkspace",
      "name": "myworkspace"
    }]
  }' \
  --data-sources '{
    "performanceCounters": [{
      "name": "cpuCounter",
      "streams": ["Microsoft-Perf"],
      "samplingFrequencyInSeconds": 60,
      "counterSpecifiers": [
        "\\Processor(_Total)\\% Processor Time",
        "\\Memory\\Available Bytes"
      ]
    }],
    "windowsEventLogs": [{
      "name": "eventLogsDataSource",
      "streams": ["Microsoft-Event"],
      "xPathQueries": ["System!*[System[EventID=4625]]"]
    }]
  }'
```

---

## Application Insights

Application Insights is **Azure Monitor's application performance management (APM) layer**. It's the tool you use to monitor your actual code — request rates, response times, failure rates, dependency calls, custom events, and exceptions — all correlated into a single view of your application's health.

It sits on top of Log Analytics — all Application Insights data lands in a Log Analytics workspace and is queryable with KQL.

### SDK Integration (.NET)

```bash
dotnet add package Microsoft.ApplicationInsights.AspNetCore
```

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Add Application Insights — connection string from config
// APPLICATIONINSIGHTS_CONNECTION_STRING environment variable is automatically
// picked up when deployed to App Service with App Insights enabled
builder.Services.AddApplicationInsightsTelemetry();

var app = builder.Build();
```

```csharp
// In your services — injecting TelemetryClient for custom tracking
using Microsoft.ApplicationInsights;
using Microsoft.ApplicationInsights.DataContracts;

public class OrderService
{
    private readonly TelemetryClient _telemetry;

    public OrderService(TelemetryClient telemetry)
    {
        _telemetry = telemetry;
    }

    public async Task<Order> ProcessOrderAsync(string orderId, string customerId)
    {
        // Track a custom event — appears in Application Insights
        _telemetry.TrackEvent("OrderProcessingStarted", new Dictionary<string, string>
        {
            { "orderId", orderId },
            { "customerId", customerId }
        });

        var stopwatch = System.Diagnostics.Stopwatch.StartNew();

        try
        {
            // Track a dependency call (e.g. external payment API)
            using var dependencyTracking = new DependencyTelemetry
            {
                Name = "PaymentGateway",
                Target = "payments.example.com",
                Type = "HTTP",
                Data = $"POST /api/charge"
            };

            // ... call payment API ...
            dependencyTracking.Success = true;
            _telemetry.TrackDependency(dependencyTracking);

            // Track a custom metric
            stopwatch.Stop();
            _telemetry.TrackMetric("OrderProcessingDuration", stopwatch.ElapsedMilliseconds);

            // Track a page or request outcome
            _telemetry.TrackEvent("OrderProcessingCompleted", new Dictionary<string, string>
            {
                { "orderId", orderId }
            }, new Dictionary<string, double>
            {
                { "processingTimeMs", stopwatch.ElapsedMilliseconds }
            });

            return new Order();
        }
        catch (Exception ex)
        {
            // Track exceptions — these show up in the Failures blade
            _telemetry.TrackException(ex, new Dictionary<string, string>
            {
                { "orderId", orderId },
                { "operation", "ProcessOrder" }
            });

            throw;
        }
    }
}
```

### What Application Insights Collects Automatically

Once the SDK is installed, without any custom code you automatically get:

- **Requests** — every HTTP request with URL, method, status code, duration
- **Dependencies** — outbound calls to SQL, HTTP APIs, Storage, Service Bus, Redis
- **Exceptions** — unhandled and handled exceptions with full stack traces
- **Performance counters** — CPU, memory, request rate, exception rate
- **Custom events and metrics** — whatever you add with `TrackEvent` / `TrackMetric`
- **Live Metrics** — real-time streaming view of requests, failures, and performance

### Distributed Tracing and Correlation

When your app makes calls to other services (microservices, queues, databases), Application Insights **correlates all of those calls into a single end-to-end transaction trace** using a correlation ID that flows through HTTP headers automatically.

```csharp
// When you inject TelemetryClient and the SDK is configured,
// correlation IDs are automatically added to outbound HTTP calls
// and parsed from inbound requests.
// You can add custom properties to ALL telemetry in a request scope:

public class CorrelationMiddleware
{
    private readonly RequestDelegate _next;
    private readonly TelemetryClient _telemetry;

    public CorrelationMiddleware(RequestDelegate next, TelemetryClient telemetry)
    {
        _next = next;
        _telemetry = telemetry;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Add custom properties visible in all telemetry for this request
        using var operation = _telemetry.StartOperation<RequestTelemetry>("CustomOperation");
        operation.Telemetry.Properties["customerId"] = context.User?.Identity?.Name;
        operation.Telemetry.Properties["environment"] = "production";

        await _next(context);
    }
}
```

---

## KQL — Kusto Query Language

KQL is the query language for Log Analytics. It's a **pipe-based language** where each step transforms the data and passes it to the next. Once it clicks, it's extremely expressive and fast to write.

```kql
// Basic structure: TableName | operation | operation | ...

// ─────────────────────────────────────────────
// REQUESTS — HTTP requests to your application
// ─────────────────────────────────────────────

// All requests in the last hour
requests
| where timestamp > ago(1h)

// Failed requests only
requests
| where success == false
| project timestamp, name, resultCode, duration, url

// Request volume by hour
requests
| summarize count() by bin(timestamp, 1h)
| render timechart

// Slowest 10 requests
requests
| top 10 by duration desc
| project timestamp, name, duration, url

// P95 response time by operation
requests
| summarize percentile(duration, 95) by name
| order by percentile_duration_95 desc

// ─────────────────────────────────────────────
// EXCEPTIONS
// ─────────────────────────────────────────────

// All exceptions in last 24 hours
exceptions
| where timestamp > ago(24h)
| project timestamp, type, outerMessage, innermostMessage, operation_Name

// Exception count by type
exceptions
| summarize count() by type
| order by count_ desc

// Exceptions with full stack trace for a specific error
exceptions
| where type contains "SqlException"
| project timestamp, type, innermostMessage, details

// ─────────────────────────────────────────────
// DEPENDENCIES — outbound calls your app made
// ─────────────────────────────────────────────

// Failed dependency calls
dependencies
| where success == false
| project timestamp, name, target, type, resultCode, duration

// Slow database calls (over 1 second)
dependencies
| where type == "SQL" and duration > 1000
| project timestamp, name, data, duration
| order by duration desc

// ─────────────────────────────────────────────
// CUSTOM EVENTS and METRICS
// ─────────────────────────────────────────────

// Custom events you tracked with TrackEvent
customEvents
| where name == "OrderProcessingCompleted"
| project timestamp, customDimensions, customMeasurements

// Custom metrics
customMetrics
| where name == "OrderProcessingDuration"
| summarize avg(value), max(value), percentile(value, 95) by bin(timestamp, 1h)
| render timechart

// ─────────────────────────────────────────────
// JOINING TABLES — correlating requests with exceptions
// ─────────────────────────────────────────────

// Find requests that resulted in exceptions
requests
| where success == false
| join kind=inner (
    exceptions
    | project exceptionType = type, exceptionMessage = innermostMessage, operation_Id
) on operation_Id
| project timestamp, name, resultCode, exceptionType, exceptionMessage
| order by timestamp desc

// ─────────────────────────────────────────────
// PERFORMANCE COUNTERS
// ─────────────────────────────────────────────

// CPU usage over time
performanceCounters
| where name == "% Processor Time"
| summarize avg(value) by bin(timestamp, 5m)
| render timechart

// ─────────────────────────────────────────────
// AVAILABILITY — results of availability tests
// ─────────────────────────────────────────────

availabilityResults
| where success == false
| project timestamp, name, location, message, duration
| order by timestamp desc

// Availability percentage by test and location
availabilityResults
| summarize
    total = count(),
    passed = countif(success == true)
  by name, location
| extend availabilityPct = (passed * 100.0) / total
| order by availabilityPct asc

// ─────────────────────────────────────────────
// AZURE ACTIVITY LOG — control plane operations
// ─────────────────────────────────────────────

// Who deleted what resource recently
AzureActivity
| where OperationNameValue endswith "DELETE"
| where ActivityStatusValue == "Success"
| project TimeGenerated, Caller, ResourceGroup, ResourceId, OperationNameValue

// Failed deployments
AzureActivity
| where OperationNameValue contains "deployments"
| where ActivityStatusValue == "Failure"
| project TimeGenerated, Caller, Properties

// ─────────────────────────────────────────────
// COMMON KQL PATTERNS to memorize
// ─────────────────────────────────────────────

// ago() — relative time
// ago(1h), ago(24h), ago(7d), ago(30m)

// bin() — round timestamps to a bucket size for grouping
// bin(timestamp, 1h), bin(timestamp, 5m)

// summarize — aggregate
// summarize count(), avg(duration), max(duration), percentile(duration, 95)

// render — visualization hint
// render timechart, render barchart, render piechart

// project — select/rename columns
// project timestamp, name, duration

// extend — add computed column
// extend errorRate = (failedCount * 100.0) / totalCount

// where — filter
// where timestamp > ago(1h) and success == false

// order by / top
// order by duration desc
// top 10 by duration desc
```

---

## Alerts

Alerts are how Azure Monitor takes action when something crosses a threshold. Every alert has three parts: a **condition** (what to watch), an **action group** (what to do), and the **alert rule** itself.

### Alert Types

**Metric Alerts** — fire when a metric crosses a threshold. Near real-time, evaluated every 1-5 minutes. Best for operational alerting like CPU, memory, error rate.

**Log Alerts** — run a KQL query on a schedule and fire if results meet a condition. More powerful (can query across multiple resources, use complex logic) but slightly slower — evaluated every 1-60 minutes depending on configuration.

**Activity Log Alerts** — fire when specific Azure control-plane operations occur, like a resource being deleted or a role assignment being created. Great for security and compliance monitoring.

**Smart Detection Alerts** — Application Insights automatically detects anomalies in your telemetry (sudden spike in failure rate, unusual response time degradation) without you writing any rules. Powered by ML.

### Creating Alerts

```bash
# Create an action group — defines WHO gets notified and HOW
az monitor action-group create \
  --resource-group myRG \
  --name myActionGroup \
  --short-name myAG \
  --action email myEmail admin@company.com \
  --action sms mySMS 1 5551234567

# Metric alert — fire when App Service CPU > 80% for 5 minutes
az monitor metrics alert create \
  --resource-group myRG \
  --name HighCPUAlert \
  --scopes $(az webapp show --name myapp --resource-group myRG --query id -o tsv) \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action $(az monitor action-group show \
      --name myActionGroup \
      --resource-group myRG --query id -o tsv)

# Log alert — fire when error rate exceeds 5% over 15 minutes
az monitor scheduled-query create \
  --resource-group myRG \
  --name HighErrorRateAlert \
  --scopes $(az monitor log-analytics workspace show \
      --workspace-name myworkspace \
      --resource-group myRG --query id -o tsv) \
  --condition-query "
    requests
    | where timestamp > ago(15m)
    | summarize
        total = count(),
        failed = countif(success == false)
    | extend errorRate = (failed * 100.0) / total
    | where errorRate > 5" \
  --condition-time-aggregation Count \
  --condition-operator GreaterThan \
  --condition-threshold 0 \
  --evaluation-frequency 5m \
  --window-duration 15m \
  --severity 1 \
  --action-groups $(az monitor action-group show \
      --name myActionGroup \
      --resource-group myRG --query id -o tsv)
```

### Action Groups

Action groups define what happens when an alert fires. A single action group can have multiple actions and can be reused across many alert rules.

Supported action types:

- **Email / SMS / Push notification** — notify people directly
- **Voice call** — phone call for critical alerts
- **Webhook** — POST to any HTTPS endpoint (integrate with PagerDuty, Slack, etc.)
- **Logic App** — trigger a workflow for complex automated responses
- **Azure Function** — trigger a function for custom remediation code
- **Automation Runbook** — trigger PowerShell automation (e.g., auto-restart a service)
- **ITSM** — create tickets in ServiceNow or similar tools
- **Event Hub** — stream alert data for custom processing

---

## Autoscale

Azure Monitor Autoscale is what actually executes scale-out and scale-in decisions for App Service, VM Scale Sets, and other resources. You define rules based on metrics, and Monitor adjusts the instance count automatically.

```bash
# Create autoscale settings for an App Service Plan
az monitor autoscale create \
  --resource-group myRG \
  --resource myplan \
  --resource-type Microsoft.Web/serverfarms \
  --name myAutoscale \
  --min-count 2 \
  --max-count 10 \
  --count 2   # default instance count

# Scale OUT rule: add 2 instances when CPU > 70% for 10 minutes
az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name myAutoscale \
  --condition "Percentage CPU > 70 avg 10m" \
  --scale out 2 \
  --cooldown 5   # minutes before another scale action can happen

# Scale IN rule: remove 1 instance when CPU < 30% for 10 minutes
az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name myAutoscale \
  --condition "Percentage CPU < 30 avg 10m" \
  --scale in 1 \
  --cooldown 10
```

### Autoscale Profiles

You can define different autoscale behaviors for different times — for example, pre-scale up before business hours or a known traffic spike:

```bash
# Create a scheduled profile for weekday business hours
az monitor autoscale profile create \
  --resource-group myRG \
  --autoscale-name myAutoscale \
  --name businessHours \
  --min-count 4 \
  --max-count 10 \
  --count 4 \
  --recurrence week mon tue wed thu fri \
  --start 08:00 \
  --end 18:00 \
  --timezone "Eastern Standard Time"
```

---

## Workbooks

Workbooks are **interactive, shareable reports** built on top of Azure Monitor data. You combine KQL queries, metrics charts, text, and parameters into a single document that your team can use for dashboards, incident investigation, or capacity planning. Built in the portal, no code required.

For the exam, know they exist and that they support **parameters** (dropdowns to filter the whole workbook by resource, time range, subscription, etc.) and can combine data from multiple Log Analytics workspaces.

---

## Availability Tests (Application Insights)

Availability tests are **synthetic monitoring** — Azure pings your application's endpoints from multiple locations around the world on a schedule and reports whether they're up, how fast they respond, and whether the response is correct.

```bash
# Create a URL ping test
az monitor app-insights web-test create \
  --resource-group myRG \
  --app-insights-name myAppInsights \
  --name homepagePingTest \
  --location eastus \
  --locations '["us-ca-sjc-azr", "us-tx-sn1-azr", "emea-nl-ams-azr"]' \
  --defined-web-test-name homepagePingTest \
  --url https://myapp.azurewebsites.net/health \
  --frequency 300 \      # test every 5 minutes
  --timeout 30           # fail if no response within 30 seconds
```

Three types:

- **URL ping test** — simple HTTP GET, check status code and optionally content
- **Standard test** — more control, supports POST, custom headers, certificate validation checks
- **Custom TrackAvailability test** — write code using the SDK to test complex multi-step flows (login, browse, checkout)

---

## Azure Monitor for Containers (Container Insights)

For AKS clusters, Container Insights collects detailed metrics and logs from your nodes and pods — CPU/memory per pod, container logs, cluster health — without you instrumenting your application code.

```bash
# Enable Container Insights on an AKS cluster
az aks enable-addons \
  --resource-group myRG \
  --name myakscluster \
  --addons monitoring \
  --workspace-resource-id $(az monitor log-analytics workspace show \
      --workspace-name myworkspace \
      --resource-group myRG --query id -o tsv)
```

Once enabled, a new set of tables appears in your Log Analytics workspace: `ContainerLog`, `KubePodInventory`, `KubeNodeInventory`, `InsightsMetrics` — all queryable with KQL.

---

## How It All Fits Together — Full Observability Picture

```
Your Application (App Service / AKS / Functions)
        │
        │  Application Insights SDK
        ▼
   App Insights ──────────────────────────────────────────────►┐
        │                                                       │
Azure Platform (Cosmos DB, Key Vault, Event Hubs, etc.)        │
        │                                                       │
        │  Diagnostic Settings                                  │
        ▼                                                       │
  Log Analytics Workspace ◄──────────────────────────────────►─┤
        │                                                       │
Virtual Machines                                                │
        │                                                       │
        │  Azure Monitor Agent + DCRs                          │
        └───────────────────────────────────────────────────►──┤
                                                               │
                                                               ▼
                                              KQL Queries, Dashboards,
                                              Workbooks, Alerts,
                                              Autoscale Actions
```

Everything flows into Log Analytics. One query language to rule them all.

---

## AZ-204 Exam Summary

The exam will test you on the distinction between **metrics and logs and when to use each**, how to configure **Diagnostic Settings** to route data from Azure resources, how to instrument applications with the **Application Insights SDK** (`TrackEvent`, `TrackException`, `TrackMetric`, `TrackDependency`), writing **KQL queries** for common scenarios (failures, performance, exceptions, custom events), creating **metric and log alert rules** with action groups, the difference between **alert types** (metric vs. log vs. activity log), and how **autoscale rules and profiles** work. You should also understand what **availability tests** are and the three types.


