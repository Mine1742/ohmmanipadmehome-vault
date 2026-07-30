#entra #domaincontroller [[Entra]]
# Cannot Add User from DC A to Group in DC B

When you cannot add a user from **Domain Controller (DC) A** to a security group in **DC B**, the issue typically stems from domain/forest boundaries, group scope limitations, or replication/configuration problems.

---

## 1. Trust Relationship Not Established

If DC A and DC B are in **different domains**, ensure that:

- A **two-way trust** exists between the domains.
- Trusts can be verified in **Active Directory Domains and Trusts**.
- Use `nltest /domain_trusts` or `Get-ADTrust` (PowerShell) to inspect trust configurations.

---

## 2. Cross-Forest Limitations

If the domains are in **different forests**:

- A **forest trust** is required for user/group integration.
- Ensure **Universal Groups** are used and **Global Catalog** servers are available.

---

## 3. Replication Issues

If DC A and DC B are in the same domain but different sites:

- Check for AD replication problems.
- Use `repadmin /replsummary` to assess replication status.

---

## 4. Permission Restrictions

- Ensure you have **delegated permissions** to manage group memberships in DC B.
- Certain groups (e.g., **Domain Admins**) are protected by **AdminSDHolder**, which may block changes.

---

## 5. Group Scope Compatibility

Group scope rules impact whether users from another domain can be added:

| Group Scope  | Can Contain Members From          |
| ------------ | --------------------------------- |
| Domain Local | Any domain (trust required)       |
| Global       | Same domain only                  |
| Universal    | Any domain within the same forest |

Attempting to add a user from Domain A to a **Global Group** in Domain B will fail.

---

## 6. SID Filtering

- **SID filtering** protects against SID spoofing but may block legitimate cross-domain group additions.
- Use `netdom trust` to inspect.
- Disable SID filtering if necessary using:
  ```
  netdom trust <target_domain> /domain:<source_domain> /enablesidhistory:yes
  ```

---

## Troubleshooting Checklist

-

