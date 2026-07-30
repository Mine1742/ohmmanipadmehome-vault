#az104 

## What is Azure Backup?

Azure Backup is a built-in Azure service that provides secure backup for all Azure-managed data assets. It uses zero-infrastructure solutions to enable self-service backups and restores, with at-scale management at a lower and predictable cost. Azure Backup currently offers specialized backup solutions for Azure and on-premises virtual machines (VMs). Azure Backup also gives workloads like SQL Server or SAP HANA (High-performance Analytic Appliance) running in Azure VMs enterprise-class backup and restore options.

In contrast to traditional backup solutions that can take considerable effort to set up, Azure Backup is easily managed through the Azure portal.

### Azure Backup versus Azure Site Recovery

Both Azure Backup and Azure Site Recovery aim to make the system more resilient to faults and failures, but they use two different approaches. The primary goal of Backup is to maintain copies of stateful data that allow you to go back in time. Site Recovery, however, replicates the data in almost real time and allows for a failover.

In that sense, if there are issues like network or power outages, you can use availability zones. For a region-wide disaster (such as natural disasters), Site Recovery is used. Backups are used in cases of accidental data loss, data corruption, or ransomware attacks.

Additionally, the choice of a recovery approach depends on the criticality of the application, recovery point objective (RPO) and recovery time objective (RTO) requirements, and the cost implications.

### Why use Azure Backup?

Traditional backup solutions, such as disk and tape, don't offer the highest level of integration with cloud-based solutions. Azure Backup has several benefits over more traditional backup solutions:

**Zero-infrastructure backup**: Azure Backup eliminates the need to deploy and manage any backup infrastructure or storage. There's no overhead in maintaining backup servers or scaling the storage up or down as the needs vary.

**Long-term retention**: Meet rigorous compliance and audit needs by retaining backups for many years, after which the built-in lifecycle management capability prunes the recovery points automatically.

**Security**: Azure Backup provides security to your backup environment, both when your data is in transit and at rest:

- **Azure role-based access control**: Role-based access control allows you to segregate duties within your team and grant only the amount of access to users necessary to do their jobs.
    
- **Encryption of backups**: Backup data is automatically encrypted using Microsoft-managed keys. Alternatively, you can encrypt your backed-up data using customer-managed keys stored in the Azure Key Vault. 
    
- **No internet connectivity required**: When you use Azure VMs, all the data transfer happens only on the Azure backbone network without needing to access your virtual network. So no access to any IPs or fully qualified domain names (FQDNs) is required.
    
- **Soft delete**: With soft delete, the backup data is retained for 14 more days even after the deletion of the backup item. This retention protects against accidental deletion or malicious deletion scenarios, allowing the recovery of those backups with no data loss. Azure Backup also provides **Enhanced soft delete** that enables you to retain a deleted item in the _soft deleted_ state for a longer duration.
    

Azure Backup also offers the ability to back up VMs encrypted with Azure Disk Encryption.

**High availability**: Azure Backup offers three types of replication:

- **Locally redundant storage (LRS)**: The lowest-cost option with basic protection against server rack and drive failures. We recommend it for noncritical scenarios.
    
- **Geo-redundant storage (GRS)**: The intermediate option has failover capabilities in a secondary region. We recommend it for backup scenarios.
    
- **Zone-redundant storage (ZRS)**: This option protects against datacenter-level failures by replicating your storage account synchronously across three Azure availability zones. We recommend it for high-availability scenarios.
    

**Centralized monitoring and management**: Azure Backup provides built-in monitoring and alerting capabilities in a Recovery Services vault. These capabilities are available without any other management infrastructure.

### Azure Backup supported scenarios

Azure Backup supports the following scenarios:

- **Azure VMs** - Back up Windows or Linux Azure VMs  
    Azure Backup provides independent and isolated backups to guard against unintended destruction of the data on your VMs. Backups are stored in a Recovery Services vault with built-in management of recovery points. Configuration and scaling are simple, backups are optimized, and you can easily restore as needed.
- **On-premises** - Back up files, folders, and system state using the [Microsoft Azure Recovery Services (MARS) agent](https://learn.microsoft.com/en-us/azure/backup/backup-support-matrix-mars-agent). Or use [Microsoft Azure Backup Server (MABS)](https://learn.microsoft.com/en-us/azure/backup/backup-support-matrix-mabs-dpm) or [Data Protection Manager (DPM) server](https://learn.microsoft.com/en-us/azure/backup/backup-support-matrix-mabs-dpm) to protect on-premises VMs (Hyper-V and VMware) and other on-premises workloads.
- **Azure Files shares** - Azure Files provides snapshot management by Azure Backup.
- **SQL Server in Azure VMs** and **SAP HANA databases in Azure VMs** - Azure Backup offers stream-based, specialized solutions to back up SQL Server, or SAP HANA running in Azure VMs. These solutions take workload-aware backups that support different backup types such as full, differential and log, 15-minute RPO, and point-in-time recovery.



# Back up an Azure virtual machine by using Azure Backup

You want to ensure that the backup and restore jobs you put in place offer a way to recover your company's servers. With this requirement in mind, you want to investigate the best way to implement backup for your virtual machines (VMs).

VMs that are hosted on Azure can take advantage of Azure Backup. You can easily back up and restore machines without installing extra software.

In this unit, you explore all the methods of backing up Azure VMs provided by Azure Backup and make a decision on which to implement.

**Azure VMs** are backed up by taking snapshots of the underlying disks at user-defined intervals and transferring those snapshots to the Recovery Services vault as per the customer-defined policy.

## Recovery Services vault

Azure Backup uses a Recovery Services vault to manage and store the backup data. A vault is a storage-management entity, which provides a simple experience to carry out and monitor backup and restore operations. With Azure Backup, you don't need to worry about deploying or managing storage accounts. In fact, all you need to specify is the vault that you want to back up the virtual machine (VM) to. The backup data is transferred to the Azure Backup storage accounts (in a separate fault domain) in the background. The vault also acts as a role-based access control boundary to allow secure access to the data.

![Screenshot that highlights the Recovery Services vaults that are available in context to the resources they're protecting.](https://learn.microsoft.com/en-us/training/modules/protect-virtual-machines-with-azure-backup/media/3-recovery-vault-in-context.png)

## Snapshots

A snapshot is a point-in-time backup of all disks on the VM. For Azure VMs, Azure Backup uses different extensions for each supporting operating system:

|Extension|OS|Description|
|---|---|---|
|VM Snapshot|Windows|The extension works with Volume Shadow Copy Service (VSS) to take a copy of the data on disk and in memory.|
|VM SnapshotLinux|Linux|The snapshot is a copy of the disk.|

Depending on how the snapshot is taken and what it includes, you can achieve different levels of consistency:

- **Application consistent**
    - The snapshot captures the VM as a whole. It uses VSS writers to capture the content of the machine memory and any pending I/O operations.
    - For Linux machines, you need to write custom pre or post scripts per app to capture the application state.
    - You can get complete consistency for the VM and all running applications.
- **File system consistent**
    - If VSS fails on Windows, or the pre and post scripts fail on Linux, Azure Backup still creates a file-system-consistent snapshot.
    - During a recovery, no corruption occurs within the machine. But installed applications need to do their own cleanup during startup to become consistent.
- **Crash consistent**
    - This level of consistency typically occurs if the VM is shut down at the time of the backup.
    - No I/O operations or memory contents are captured during this type of backup. This method doesn't guarantee data consistency for the OS or app.

## Backup policy

You can define the backup frequency and retention duration for your backups. Currently, the VM backup can be triggered daily or weekly, and can be stored for multiple years. The backup policy supports two access tiers: _snapshot tier_ and the _vault tier_. By using the Enhanced policy, you can trigger hourly backups.

**Selective disk backup**: Azure Backup provides **Selective Disk backup and restore** capability using **Enhanced policy**. By using this capability, you can selectively back up a subset of the data disks that are attached to your VM. Then, you can restore a subset of the disks that are available in a recovery point, both from instant restore and vault tier. It helps you manage critical data in a subset of the VM disks and use database backup solutions when you want to back up only their OS disk to reduce cost.

**Snapshot tier**: All the snapshots are stored locally for a maximum period of five days, in what is called the snapshot tier. For all types of operation recoveries, we recommended that you restore from the snapshots because it's faster to do so. This capability is called **instant restore**.

**Vault tier**: All snapshots are additionally transferred to the vault for more security and longer retention. At this point, the recovery point type changes to "snapshot and vault."

## Backup process for an Azure virtual machine

Here's how Azure Backup completes a backup for Azure VMs:

1. For Azure VMs that are selected for backup, Azure Backup starts a backup job according to the backup frequency you specify in the backup policy.
    
2. During the first backup, a backup extension is installed on the VM, if the VM is running:
    
    - For Windows VMs, the VM Snapshot extension is installed.
    - For Linux VMs, the VM SnapshotLinux extension is installed.
3. After the snapshot is taken, the data is stored locally and transferred to the vault.
    
    - The backup is optimized by backing up each VM disk in parallel.
    - For each disk that's being backed up, Azure Backup reads the blocks on the disk and identifies and transfers only the data blocks that changed (the delta) since the previous backup.
    - Snapshot data might not be immediately copied to the vault. It might take several hours at peak times. Total backup time for a VM is less than 24 hours for daily backup policies.

![Diagram that shows Azure Backup architecture.](https://learn.microsoft.com/en-us/training/modules/protect-virtual-machines-with-azure-backup/media/3-azure-vm-backup-architecture.png)

You can additionally enable [vault encryption with customer-managed keys (CMK)](https://learn.microsoft.com/en-us/azure/backup/encryption-at-rest-with-cmk#configuring-a-vault-to-encrypt-using-customer-managed-keys?azure-portal=true). By using **Enhanced soft delete** for a Recovery Services vault, you can protect backups from deletion. You can also keep Enhanced soft delete _always on_ to prevent turning it off, thus protecting your backups from accidental deletion or from malware attacks.


# Restore virtual machine data

Companies that have a business continuity and disaster recovery (BCDR) plan typically schedule test runs to ensure that the business can successfully recover from disasters. Now that you successfully backed up your virtual machines, you want to explore the options available for restoring them as part of your BCDR testing.

In this unit, you learn about the options for restoring an Azure virtual machine (VM) from a previous backup.

## Restore types

Azure Backup provides many ways to restore a VM. As explained earlier, you can either instantly restore from the snapshot tier (optimal for operational recoveries) or from the vault tier.

|Restore option|Details|
|---|---|
|**Create a new VM**|Quickly creates and gets a basic VM up and running from a restore point. The new VM must be created in the same region as the source VM.|
|**Restore disk**|Restores a VM disk, which can then be used to create a new VM. The disks are copied to the resource group you specify. Azure Backup provides a template to help you customize and create a VM. Alternatively, you can attach the disk to an existing VM, or create a new VM.  <br>  <br>This option is useful if you want to customize the VM, add configuration settings that weren't there at the time of backup. Or, add settings that must be configured using the template or PowerShell.|
|**Replace existing**|You can restore a disk and use it to replace a disk on the existing VM. Azure Backup takes a snapshot of the existing VM before replacing the disk and stores it in the staging location you specify. Existing disks connected to the VM are replaced with the selected restore point. The current VM must exist. You can't use this option if the VM is deleted.|
|**Cross region (secondary region)**|Cross region restore can be used to restore Azure VMs in the secondary region, which is an Azure paired region.  <br>This feature is available for the following options:  <br>- Create a VM<br>- Restore Disks  <br>    We don't currently support the Replace existing disks option.|
|**Cross Subscription Restore**|Backup Admins and App admins can perform the restore operation on secondary regions.  <br>Cross Subscription Restore:  <br>  <br>- Allows you to restore Azure Virtual Machines or disks to a different subscription within the same tenant as the source subscription. As per the Azure role-based access control capabilities from restore points.  <br>- Allowed only if the Cross Subscription Restore property is enabled for your Recovery Services vault.  <br>- Works with Cross Region Restore and Cross Zonal Restore.  <br>- You can trigger Cross Subscription Restore for managed virtual machines only.  <br>- Cross Subscription Restore is supported for Restore with Managed System Identities (MSI).  <br>- It's unsupported for snapshots tier recovery points.  <br>- It's unsupported for unmanaged VMs and VMs encrypted with Advanced Digital Encryption (ADE).|
|**Cross Zonal Restore**|Allows you to restore Azure Virtual Machines or disks pinned to any zone to different available zones (as per the Azure Role-based access control capabilities) from restore points. When you select a zone to restore, it selects the logical zone (and not the physical zone) as per the Azure subscription you use to restore to.  <br>- You can trigger Cross Zonal Restore for managed virtual machines only.  <br>- Cross Zonal Restore is supported for Restore with Managed System Identities (MSI).  <br>- Cross Zonal Restore supports restore of an Azure zone pinned/non-zone pinned VM from a vault with Zone-redundant storage (ZRS) enabled. Learn how to set Storage Redundancy.  <br>- You can only use Cross Zonal Restore to restore a VM pinned to an Azure zone from a vault with Cross Region Restore (CRR) under these conditions: The secondary region supports zones, or Zone Redundant Storage (ZRS) is enabled.  <br>- Cross Zonal Restore is supported from secondary regions.  <br>- It's unsupported from snapshots restore point.  <br>- It's unsupported for Encrypted Azure VMs.|
|**Selective disk backup**|Allows you to back up and restore selective VM disks through Enhanced policy. Using this capability, you can selectively back up a subset of the data disks that are attached to your VM. Then, you can restore a subset of the disks that are available in a recovery point, both from instant restore and vault tier.  <br>  <br>Selective disk backup is useful when you:  <br>  <br>- Manage critical data in a subset of the VM disks.  <br>- Use database backup solutions and want to back up only their OS disk to reduce cost.|

## Recover files from a backup

You can also recover individual files from a recovery point by mounting the snapshot on the target machine using the iSCSI initiator in the machine. To learn more, see [Recover files from Azure virtual machine backup](https://learn.microsoft.com/en-us/azure/backup/backup-azure-restore-files-from-vm).

## Restore an encrypted virtual machine

Azure Backup supports the backup and restore of machines encrypted through Azure Disk Encryption. Disk Encryption works with Azure Key Vault to manage the relevant secrets that are associated with the encrypted disk. For an extra layer of security, you can use key vault encryption keys (KEKs) to encrypt the secrets before they're written to the key vault.

Certain limitations apply when you restore encrypted VMs:

- Azure Backup supports only standalone key encryption. Any key that's part of a certificate isn't currently supported.
- File-level or folder-level restores aren't supported with encrypted VMs. To restore to that level of granularity, the entire VM has to be restored. You can then manually copy the file or folders.
- The **Replace existing VM** option isn't available for encrypted VMs.

# How Azure Backup works

Let's take a look at how Azure Backup works to provide the data protection you need. Particularly, let's look at how the different aspects of the backup service make it easy to back up various types of data, and how it offers security for your backups as well. In this unit, we cover the following aspects of the Azure Backup Service:

- **Workload integration layer - Backup Extension**: Integration with the actual workload, such as Azure virtual machines (VMs) or Azure Blobs, happens at this layer.
- **Data Plane - Access Tiers**: There are three access tiers where the backups could be stored:
    - Snapshot tier
    - Standard tier
    - Archive tier
- **Data Plane - Availability and Security**: The backup data is replicated across zones or regions, based on the redundancy the user specifies.
- **Management Plane – Recovery Services vault/Backup vault and Backup center**: The vault provides an interface for the user to interact with the backup service.

## What data is backed up and how?

The simplest explanation of Azure Backup is that it backs up data, machine state, and workloads running on on-premises machines and VM instances to the Azure cloud. Azure Backup stores the backed-up data in Recovery Services vaults and Backup vaults.

For on-premises Windows machines, you can back up directly to Azure with the Azure Backup Microsoft Azure Recovery Services (MARS) agent. Alternatively, you can back up these Windows machines to a backup server, perhaps a System Center Data Protection Manager (DPM) or Microsoft Azure Backup Server (MABS). You can then back that server up to a Recovery Services vault in Azure.

If you're using Azure VMs, you can back them up directly. Azure Backup installs a backup extension to the Azure VM agent that's running on the VM, which allows you to back up the entire VM. If you only want to back up the files and folders on the VM, you can do so by running the MARS agent.

Azure Backup stores backed-up data in vaults: Recovery Services vaults and Backup vaults. A vault is an online-storage entity in Azure that's used to hold data such as backup copies, recovery points, and backup policies.

### Supported backup types

Azure Backup supports full backups and incremental backups. Your initial backup is a full backup. DPM/MABS use the incremental backup for disk backups, and all backups to Azure also use incremental backups. As the name suggests, incremental backups only focus on the blocks of data that changed since the previous backup.

Azure Backup also supports SQL Server backup types. The following table outlines the support for SQL Server type backups:

| Type                     | Description                                                                                                                                                                                                                                                                                                                                                                      | Usage                                                                                                                                                         |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full                     | A full database backup backs up the entire database. It contains all the data in a specific database or in a set of filegroups or files. A full backup also contains enough logs to recover that data.                                                                                                                                                                           | At most, you can trigger one full backup per day. You can choose to make a full backup on a daily or weekly interval.                                         |
| Differential             | A differential backup is based on the most recent full-data backup. It captures only the data that changed since the full backup.                                                                                                                                                                                                                                                | At most, you can trigger one differential backup per day. You can't configure a full backup and a differential backup on the same day.                        |
| Multiple backups per day | Back up Azure VMs hourly with a minimum recovery point objective (RPO) of 4 hours and a maximum of 24 hours.                                                                                                                                                                                                                                                                     | You can use Enhanced backup policy to set the backup schedule to 4, 6, 8, 12, and 24 hours (respectively) for new Azure offerings, such as Trusted Launch VM. |
| Selective disk backup    | Selectively back up a subset of the data disks that are attached to your VM, then restore a subset of the disks that are available in a recovery point, both from instant restore and vault tier. Selective disk backup helps you manage critical data in a subset of the VM disks and use database backup solutions when you want to back up only their OS disk to reduce cost. | Azure Backup provides Selective Disk backup and restore capability using Enhanced backup policy.                                                              |
| Transaction Log          | A log backup enables point-in-time restoration up to a specific second.                                                                                                                                                                                                                                                                                                          | At most, you can configure transactional log backups every 15 minutes.                                                                                        |

## Workload integration layer - Backup Extension

A backup extension specific to each workload is installed on the source VM or a worker VM. At the time of backup (as defined by the user in the Backup Policy) the backup extension generates the backup, which could be:

- **Storage**: Snapshots when using an Azure VM or Azure Files.
    
- **Stream backup**: For databases like SQL or High-performance Analytic Appliance (HANA) running in VMs.
    

The backup data is eventually transferred to Azure Backup managed storage in the data plane by using secure Azure networks Network Security Groups (NSG), Firewalls, or more sophisticated private endpoints.

## Data Plane - Access Tiers

There are three access tiers where the backups can be stored:

- **Snapshot tier**: (Workload-specific term) In the first phase of a virtual machine backup, the snapshot is taken and stored along with the disk. This form of storage is referred to as a snapshot tier. Restoring a snapshot tier is faster than restoring from a vault, because it eliminates the wait time for snapshots to be copied from the vault before triggering the restore operation. The snapshots of the VM/Azure Files/Azure Blobs/and so on are retained in the customer's subscription in a specified resource group. This container ensures that restores are quick, because the backup/snapshot is available locally to the customer.
    
- **Vault-standard tier**: Backup data for all workloads supported by Azure Backup is stored in vaults, which hold backup storage, an autoscaling set of storage accounts managed by Azure Backup. The Vault-standard tier is an online storage tier that allows you to store an isolated copy of backup data in a Microsoft-managed tenant, thus creating an extra layer of protection. For workloads where snapshot tier is supported, there's a copy of the backup data in both the snapshot tier and the Vault-standard tier. The Vault-standard tier ensures that backup data is available even if the data source being backed up is deleted or compromised.
    
- **Archive tier**: Customers rely on Azure Backup for storing backup data, including their Long-Term Retention (LTR) backup data, with retention needs defined in the organization's compliance rules. In most cases, the older backup data is rarely accessed and is only stored for compliance needs.
    
    Azure Backup supports backup of long-term retention points in the archive tier.
    

All tiers offer different recovery time objectives (RTO) and are priced differently.

![Diagram of the various workloads such as on-premises server, Azure VMs, Azure files, etc. feeding into the data plane where the access tiers are located.](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-backup/media/data-plane.png)

## Data Plane - Availability and Security

The backup data is replicated across zones or regions, based on the redundancy you specify. You can choose from locally redundant storage (LRS), Geo-redundant storage (GRS), or zone-redundant storage (ZRS). These options provide you with highly available data storage capabilities.

The data is kept safe by encrypting it and implementing Azure role-based access control (RBAC). You choose who can perform backup and restore operations. Azure Backup also provides protection against malicious deletion of your backup by using soft-delete operations. A deleted backup is stored for 14 days, free of charge, which allows you to recover the backup if needed.

Azure Backup also supports a backup data lifecycle-management scenario that allows you to comply with retention policies.

![Graphic displaying the three security options of Azure RBAC, encryption, and soft delete as icons.](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-backup/media/built-in-security.png)

## Management Plane – Recovery Services vault/Backup vault and Backup center

Azure Backup uses Recovery Services vaults and Backup vaults to orchestrate and manage backups. It also uses vaults to store backed-up data. The vault provides an interface for the user to interact with the backup service. Azure Backup Policies within each vault define when the backups should get triggered and how long they need to be retained.

You can use a single vault or multiple vaults to organize and manage your backup. If you manage your workloads with a single subscription and single resource, you can use a single vault to monitor and manage your backup estate. If your workloads are spread across multiple subscriptions, you can create multiple vaults with one or more vaults per subscription.

![Diagram of the management plane. The recovery services vault shows the options for backup policies and management with the portal, SDK, or the Command-line interface (CLI).](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-backup/media/backup-vaults.png)

Backup center allows you to have a single pane of glass to manage all tasks related to backups. Backup center is designed to function well across a large and distributed Azure environment. You can use Backup center to efficiently manage backups spanning multiple workload types, vaults, subscriptions, regions, and Azure Lighthouse tenants.

![Screenshot of the Backup center user interface in the Azure portal displaying backup information for Azure Virtual machines related to jobs and backup instances.](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-backup/media/backup-center.png)


# When to use Azure Backup

Here, we discuss how you can decide if Azure Backup is the right choice for your data-protection needs. In this unit, we highlight common backup scenarios where Azure Backup provides benefits, such as:

- Ensuring availability of your data.
- Protecting your Azure workloads.
- Securing your data.

## Decision criteria

Azure Backup is an Azure service that provides secure and zero-infrastructure backup solutions for all Azure-managed data assets. It protects a wide range of enterprise workloads. Including, Azure Virtual Machines (VMs), Azure Disks, SQL and SAP databases, and Azure file shares and blobs.

The main criteria that we're evaluating are outlined in the following table. The table contains some key areas where Azure Backup can provide services to you for data protection.

|Criteria|Consideration|
|---|---|
|Azure workloads|Azure VMs, Azure Disks, SQL Server in Azure VMs, SAP HANA databases in Azure VMs, Azure Blobs, Azure Files shares, Azure Database for PostgreSQL.|
|Compliance|Customer-defined backup policy with long-term retention across multiple zones or regions.|
|Operational recoveries|With self-service backup and restores, the application administrator can take care of issues that might arise such as accidental deletion or data corruption.|

## Apply the criteria

In the introduction, we presented a scenario where your organization might have an application that relies on data from a back-end SQL Server installation. SQL Server is running on three Azure VMs. The data in the backup must be retained for up to 10 years to meet compliance requirements. You also want to be able to monitor the backups.

Before we dive into how Azure Backup can help meet these needs, it's important to understand what isn't currently supported. If your three Azure VMs are deployed across multiple subscriptions or regions, you should note that Azure Backup doesn’t support cross-region backup for most workloads. However, it does support cross-region restore in a paired secondary region.

### Can Azure Backup protect the Azure VMs hosting the SQL Server instances?

Azure Backup is able to back up entire Windows and Linux VMs using backup extensions. As a result, you can back up the entire VM that hosts SQL Server. If you only want to back up the files, folders, and system state on the Azure VMs, you can use the Microsoft Azure Recovery Services (MARS) agent.

If your main concern is to only back up the SQL Server data, Azure Backup provides support for that as well. Azure Backup offers a stream-based, specialized solution to back up SQL Servers running in Azure VMs. This solution aligns with Azure Backup's benefits of zero-infrastructure backup, long-term retention, and central management.

Additionally, Azure Backup provides the following advantages specifically for SQL Server:

- Workload aware backups that support all backup types: full, differential, and log
- 15-minute recovery point objective (RPO) with frequent log backups
- Point-in-time recovery up to a second
- Individual database-level backup and restore

![Diagram of SQL Server hosted on an Azure VM backed up to a Recovery Services Vaults in Azure Backup. Arrows indicate a two-way flow for the data path and control path flow from Azure Backup to the backup extension on the VM.](https://learn.microsoft.com/en-us/training/modules/intro-to-azure-backup/media/azure-backup-sql-overview.png)

### Does Azure Backup help with compliance?

You can implement required access-control mechanisms for your backups. Vaults (Recovery Services and Backup vaults) provide the management capabilities and are accessible via the Azure portal, Backup Center, Vault dashboards, SDK, CLI, and even REST APIs. It's also an Azure role-based access control (Azure RBAC) boundary, providing you with the option to restrict access to backups only to authorized Backup Admins.

Short-term retention can be _minutes_ or _daily_. Retention for _weekly_, _monthly_, or _yearly_ backup points is referred to as _Long-term retention_.

Long-term retention can be:

- **Planned (compliance requirements)**: If you know in advance that data is required years from the current time, use Long-term retention.
- **Unplanned (on-demand requirement)**: If you don't know in advance, then you can use on-demand backup with specific custom retention settings. Your policy settings don't impact these custom retention settings.
- **On-demand backup with custom retention**: If you need to take a backup not scheduled via backup policy, then you can use an on-demand backup. It can be useful for taking backups that don’t fit your scheduled backup or for taking granular backup (for example, multiple IaaS VM backups per day since scheduled backup permits only one backup per day). It's important to note that the retention policy defined in scheduled policy doesn't apply to on-demand backups.

You can also implement policy management to help with compliance. Azure Backup Policies within each vault define when the backups should be triggered and how long they need to be retained. You can also manage these policies and apply them across multiple items.

### Does Azure Backup simplify monitoring and administration?

Azure Backup integrates with Log Analytics for monitoring and reporting and provides reports via Workbooks.

Azure Backup provides in-built job monitoring for operations such as configuring backup, backing up, restoring, deleting backups, and so on. Azure Backup is scoped to the vault, making it ideal for monitoring a single vault.

If you need to monitor operational activities at scale, Backup Explorer provides an aggregated view of your entire backup estate, enabling detailed drill-down analysis and troubleshooting. It's a built-in Azure Monitor workbook that provides a single, central location to help you monitor operational activities across the entire backup estate on Azure, spanning tenants, locations, subscriptions, resource groups, and vaults.