
## Create a DNS zone in Azure DNS

Before you can host the wideworldimports.com domain on your servers, you need to create a DNS zone. The DNS zone holds all the configuration records associated with your domain.

To create your DNS zone:

1. Sign in to the [Azure portal](https://portal.azure.com/learn.docs.microsoft.com) with the account you used to activate the sandbox.
    
2. On the Azure **home** page, under **Azure services**, select **Create a resource**. The **Create a resource** pane appears.
    
3. In the _Search services and marketplace_ search box, search for and select **DNS zone** by Microsoft. The **DNS zone** pane appears.
    
4. Select **Create** > **DNS zone**.
    
    ![Screenshot of DNS zone, with Create highlighted.](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-dnszonecreate.png)
    
    The **Create DNS zone** pane appears.
    
5. On the **Basics** tab, enter the following values for each setting.
    
    |Setting|Value|
    |---|---|
    |**Project details**||
    |Subscription|Choose your subscription|
    |Resource group|From the dropdown list, select the resource group you want to use for this exercise.|
    |**Instance details**||
    |Name|The name needs to be unique in the sandbox. Use `wideworldimportsXXXX.com`, and replace the "Xs" with letters or numbers.|
    
    ![Screenshot of Create DNS zone page.](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-creatednszone.png)
    
6. Select **Review + create**.
    
7. After validation passes, select **Create**. It takes a few minutes to create the DNS zone.
    
8. When deployment is complete, select **Go to resource**. The **Overview** pane for your **DNS zone** appears.
    
9. Select **Record Sets** from the top menu bar.
    
    By default, the NS and SOA record sets are automatically created whenever a DNS zone is created, and automatically deleted whenever a DNS zone deleted. The NS record set defines the Azure DNS namespaces and contains the four Azure DNS records. You use all four records when you update the registrar.
    
    The SOA record represents your domain, and is used when other DNS servers are searching for your domain.
    
10. Make a note of the NS record values. You need them in the next section.
    

## Create a DNS record

Now that the DNS zone exists, you need to create the necessary records to support the domain.

The primary record set to create is the A record. The A record set is used to point traffic from a logical domain name to the hosting server's IP address. An A record set can have multiple records. In a record set, the domain name remains constant, while the IP addresses differ.

1. If you're not already on the **Record Sets** screen, then open the **DNS zone** pane for _wideworldimportsXXXX.com_. In the top menu bar, select **Record sets**.
    
2. On the **Record Sets** pane, select **+ Add** in the top menu bar.
    
3. Select **Add** at the top of the Record sets page.
    
    [![Screenshot of adding a record set.](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-add-a-record.png)](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-arecord.png#lightbox)
    
    The **Add record set** pane appears.
    
4. Enter the following values for each setting.
    
    |Setting|Value|Description|
    |---|---|---|
    |Name|www|The host name that you want to resolve to an IP address.|
    |Type|A|The **A** record is the most commonly used. If you're using IPv6, select the **AAAA** type.|
    |Alias record set|No|This setting can only be applied to A, AAAA, and CNAME record types.|
    |TTL|1|The time to live, which specifies the period of time each DNS server caches the resolution before being purged.|
    |TTL unit|Hours|This value can be seconds, minutes, hours, days, or weeks. Here, you're selecting hours.|
    |IP Address|10.10.10.10|The IP address the record name resolves to. In a real-world scenario, you'd enter the public IP address for your web server.|
    
5. Select **Add** to add the record to your zone.
    
    [![Screenshot of A record set.](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-arecord.png)](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-arecord.png#lightbox)
    

It's possible to have more than one IP address set up for your web server. In that case, you add all the associated IP addresses as records in the A record set. After the record set is created, you can update it with more IP addresses.

## Verify your global Azure DNS

In a real-world scenario, after you create the public DNS zone, you update the NS records of the domain-name registrar to delegate the domain to Azure.

Even though we don't have a registered domain, it's still possible to verify that the DNS zone works as expected by using the `nslookup` tool.

### Use nslookup to verify the configuration

Here's how to use `nslookup` to verify the DNS zone configuration.

1. Use Cloud Shell to run the following command. Replace the DNS zone name with the zone you created, and replace `<name server address>` with one of the NS values you copied after you created the DNS zone.
    
    Bash
    
    ```
    nslookup www.wideworldimportsXXXX.com <name server address>
    ```
    
    The command should look something like the following example:
    
    Bash
    
    ```
    nslookup www.wideworldimportsXXXX.com ns1-04.azure-dns.com
    ```
    
2. You should see that your host name `www.wideworldimportsXXXX.com` resolves to 10.10.10.10.
    
    ![Screenshot of Cloud Shell, showing the nslookup results.](https://learn.microsoft.com/en-us/training/modules/host-domain-azure-dns/media/4-nslookup.png)