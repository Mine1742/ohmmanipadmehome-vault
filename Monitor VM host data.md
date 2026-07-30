#az104 
You want to monitor the VMs that host your website, so you decide to quickly create a VM in the Azure portal and evaluate its built-in monitoring capabilities. In this unit, you use the Azure portal to create a Linux VM with recommended alerts and boot diagnostics enabled. As soon as the VM starts up, Azure automatically begins collecting basic metrics and activity logs. You can then view built-in metrics graphs, activity logs, and boot diagnostics.

## Create a VM and enable recommended alerts

1. Sign in to the [Azure portal](https://portal.azure.com/), and in the Search field, enter _virtual machines_.
    
2. On the **Virtual machines** page, select **Create**, and then select **Azure virtual machine**.
    
3. On the **Basics** tab of the **Create a virtual machine** page:
    
    - In the **Subscription** field, select the correct subscription if not already selected.
    - Under **Resource group**:
        1. Select **Create new**.
        2. Under **Name**, enter _learn-monitor-vm-rg_.
        3. Select **OK**.
    - For **Virtual machine name**, enter _monitored-linux-vm_.
    - For **Image**, select **Ubuntu Server 20.04 LTS - x64 Gen2**.
4. Leave the other settings at their current values, and select the **Monitoring** tab.
    
    [![Screenshot that shows the Basics tab of the Create a virtual machine page.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/create-vm-basic.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/create-vm-basic.png#lightbox)
    
5. On the **Monitoring** tab, select the checkbox next to **Enable recommended alert rules**.
    
6. On the **Set up recommended alert rules** screen:
    
    1. Select all the listed alert rules if not already selected, and adjust the values if desired.
    2. Under **Notify me by**, select the checkbox next to **Email**, and enter an email address to receive alert notifications.
    3. Select **Save**.
7. Under **Diagnostics**, for **Boot diagnostics**, ensure that **Enable with managed storage account (recommended)** is selected.
    
     Note
    
    Don't select **Enable OS guest diagnostics**. The Linux Diagnostics Agent (LAD) is deprecated, and you can enable OS guest and client monitoring later.
    
8. Select **Review + create** at the bottom of the page, and when validation passes, select **Create**.
    
    [![Screenshot that shows the Monitoring tab and alert rule configuration screen of the Create a virtual machine page.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/create-vm-monitoring.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/create-vm-monitoring.png#lightbox)
    
9. On the **Generate new key pair** popup dialog box, select **Download private key and create resource**.
    

It can take a few minutes to create the VM. When you get the notification that the VM is created, select **Go to resource** to see basic metrics data.

## View built-in metrics graphs

Once your VM is created, Azure starts collecting basic metrics data automatically. Built-in metrics graphs, along with the recommended alerts you enabled, can help you monitor whether and when your VM encounters health or performance issues. You can then use more advanced monitoring and analytics capabilities to investigate issue causes and remediation.

1. To view basic metrics graphs, on the VMs **Overview** page, select the **Monitoring** tab.
    
    [![Screenshot that shows Monitoring tab on a VMs Overview screen.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/select-monitoring.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/select-monitoring.png#lightbox)
    
2. Under **Performance and utilization** > **Platform metrics**, review the following metrics graphs related to the VMs performance and utilization. Select **Show more metrics** if all the graphs don't appear immediately.
    
    - **VM Availability**
    - **CPU (average)**
    - **Disk bytes (total)**
    - **Network (total)**
    - **Disk operations/sec (average)**
    
    [![Screenshot that shows the platform metrics graphics on the VM Overview page.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/platform-metrics.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/platform-metrics.png#lightbox)
    
3. Under **Guest OS metrics**, notice that guest OS metrics aren't being collected yet. In the next units, you configure VM insights and data collection rules to collect guest OS metrics.
    

## View the activity log

You can view the VMs activity log by selecting **Activity log** from the VMs left navigation menu. You can also retrieve entries by using PowerShell or the Azure CLI.

[![Screenshot of the activity log for a VM.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/activity-log.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/activity-log.png#lightbox)

## View boot diagnostics

You enabled boot diagnostics when you created the VM. You can view boot diagnostics to view boot data and troubleshoot startup issues.

1. In the left navigation menu for the VM, select **Boot diagnostics** under **Help**.
    
2. On the **Boot diagnostics** page, select **Screenshot** to see a startup screenshot from the VMs hypervisor. Select **Serial log** to view log messages created when the VM started.
    
    [![Screenshot that shows the boot diagnostic image captured.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/3-boot-diagnostics.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/3-boot-diagnostics.png#lightbox)

# Use Metrics Explorer to view detailed host metrics

200 XP

- 5 minutes

You want to investigate how traffic flowing into your VM affects its CPU capability. If the built-in metrics charts for a VM don't already show the data you need, you can use Metrics Explorer to create customized metrics charts. In this unit, you plot a graph that displays your VM's maximum percentage CPU and average inbound flow data together.

Azure Monitor Metrics Explorer offers a UI for exploring and analyzing VM metrics. You can use Metrics Explorer to view and create custom charts for many VM host metrics in addition to the metrics shown on the built-in graphs.

## Understand Metrics Explorer

To open Metrics Explorer, you can:

- Select **Metrics** from the VM's left navigation menu under **Monitoring**.
- Select the **See all Metrics** link next to **Platform metrics** on the **Monitoring** tab of the VM's **Overview** page.
- Select **Metrics** from the left navigation menu on the Azure Monitor **Overview** page.

[![Screenshot that shows Metrics Explorer.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/metrics-explorer.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/metrics-explorer.png#lightbox)

In Metrics Explorer, you can select the following values from the dropdown fields:

- **Scope:** If you open Metrics Explorer from a VM, this field is prepopulated with the VM name. You can add more items with the same resource type (VMs) and location.
- **Metric Namespace**: Most resource types have only one namespace, but for some types, you must pick a namespace. For example, storage accounts have separate namespaces for files, tables, blobs, and queues.
- **Metric**: Each metrics namespace has many metrics available to choose from.
- **Aggregation**: For each metric, Metrics Explorer applies a default aggregation. You can use a different aggregation to get different information about the metric.

You can apply the following aggregation functions to metrics:

- **Count**: Counts the number of data points.
- **Average (Avg)**: Calculates the arithmetic mean of values.
- **Maximum (Max)**: Identifies the highest value.
- **Minimum (Min)**: Identifies the lowest value.
- **Sum**: Adds up all the values.

You can select flexible time ranges for graphs from the past 30 minutes to the last 30 days, or custom ranges. You can specify time interval granularity from one minute to one month.

## Create a metrics graph

To create a Metrics Explorer graph that shows host VM maximum percentage CPU and inbound flows together for the past 30 minutes:

1. Open **Metrics Explorer** by selecting **See all Metrics** on the VM's **Monitoring** tab or selecting **Metrics** from the VM's left navigation menu.
    
2. **Scope** and **Metric Namespace** are already populated for the host VM. Select **Percentage CPU** from the **Metrics** dropdown list.
    
3. **Aggregation** is automatically populated with **Avg**, but change it to **Max**.
    
    [![Screenshot of the Percentage CPU metrics graph for a VM.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/3-view-host-level-metrics.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/3-view-host-level-metrics.png#lightbox)
    
4. Select **Add metric** at upper left.
    
5. Under **Metric**, select **Inbound Flows**. Leave **Aggregation** at **Avg**.
    
6. At upper right, select **Local Time: Last 24 hours (Automatic - 15 minutes)**, change it to **Last 30 minutes**, and select **Apply**.
    

Your graph should look similar to the following screenshot:

[![Screenshot that shows a graph of CPU usage and inbound traffic.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/3-metric-graph.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/3-metric-graph.png#lightbox)

# Collect client performance counters by using VM insights

Besides monitoring your VM host's health, utilization, and performance, you need to monitor the software and processes running on your VM. These are called the VM guest or client. In this unit, you enable the Azure Monitor VM insights feature, which offers a quick way to start monitoring the VM client.

The VM client includes the operating system and other workloads and applications. To monitor the software running on your VM, you install the Azure Monitor Agent, which collects data from inside the VM. VM insights:

- Installs Azure Monitor Agent on your VM.
- Creates a DCR that collects and sends a predefined set of client performance data to a Log Analytics workspace.
- Presents the data in curated workbooks.

Although you don't need to use VM insights to install Azure Monitor Agent, create DCRs, or set up workbooks, VM insights makes setting up VM client monitoring easy. VM insights provides you with a basis for monitoring the performance of your VM client and mapping the processes running on your machine.

## Enable VM insights

1. In the Azure portal, on your VM's **Overview** page, select **Insights** from the left navigation menu under **Monitoring**.
    
2. On the **Insights** page, select **Enable**.
    
3. Under **Data collection rule**, note the properties of the DCR that VM insights creates. In the DCR description, **Processes and dependencies (Map)** is set to **Disabled**, which you can change to **Enabled** or review [this article on how-to](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/vminsights-maps) if greyed out. Also a default **Log Analytics workspace** is created or assigned.
    
4. Select **Configure**.
    
    [![Screenshot that shows enabling and configuring VM insights.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/enable-insights.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/enable-insights.png#lightbox)
    
    Configuration of the workspace and the agent installation typically takes 5 to 10 minutes. It can take another 5 to 10 minutes for data to become available to view in the portal.
    
5. When the deployment finishes, confirm that the Azure Monitor Agent is installed by looking on the **Properties** tab of the VM's **Overview** page under **Extensions + applications**.
    
    On the **Monitoring** tab of the **Overview** page, under **Performance and utilization**, you can see that **Guest OS metrics** are now being collected.
    
    [![Screenshot that shows Guest OS metrics on the VM's Monitoring tab.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/guest-os-metrics.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/guest-os-metrics.png#lightbox)
    

## View VM insights

VM insights creates a DCR that sends client VM performance counters to Azure Monitor Logs. Because the DCR sends its metrics to Azure Monitor Logs, you don't use Metrics Explorer to view the metrics data that VM insights collects.

To view the VM insights performance graphs and maps:

1. Select **Insights** from the VM's left navigation menu under **Monitoring**.
    
2. Near the top of the **Insights** page, select the **Performance** tab. The prebuilt VM insights Performance workbook shows charts and graphs with performance-related data for the current VM.
    
    [![Screenshot that shows the prebuilt VM insights Performance workbook.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/vm-insights-performance.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/vm-insights-performance.png#lightbox)
    
    - You can customize the view by specifying a different **Time range** at the top of the page and different aggregations at the top of each graph.
        
    - Select **View Workbooks** to select from other available prebuilt VM insights workbooks. Select **Go To Gallery** to select from a gallery of other VM insights workbooks and workbook templates, or to edit and create your own workbooks.
        
3. If enabled earlier, select the **Map** tab on the **Insights** page to see the workbook for the Map feature. The map visualizes the VM's dependencies by discovering running process groups and processes that have active network connections over a specified time range.
    
    [![Screenshot that shows a dependency map on the Map tab of VM insights.](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/dependency-map.png)](https://learn.microsoft.com/en-us/training/modules/monitor-azure-vm-using-diagnostic-data/media/dependency-map.png#lightbox)