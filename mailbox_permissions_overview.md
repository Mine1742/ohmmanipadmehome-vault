---

## title: "Mailbox Permissions Overview" date: {{date\:YYYY-MM-DD}}

# Mailbox Permissions Overview

When you delegate access to an Exchange or Microsoft 365 mailbox, you can assign three distinct permission types. Each serves a different purpose:

## 1. Read and Manage Permissions

- **Also known as**: Full Access
- **What it does**:
  - Grants a delegate the ability to **open the mailbox** and **read**, **create**, **edit**, **move**, or **delete** items across email, calendar, contacts, and other folders.
- **Notes**:
  - Does *not* include sending rights. To send mail, you must also assign **Send As** or **Send on Behalf** permissions.

## 2. Send As Permissions

- **What it does**:
  - Allows the delegate to **send messages as if they came directly from the mailbox**. Recipients see the mailbox’s address in the **From:** field, with no indication of a delegate.
- **Use case**:
  - Ideal for shared service accounts, info@ addresses, or scenarios where the mailbox should appear to communicate in its own name.

## 3. Send on Behalf Of Permissions

- **What it does**:
  - Enables the delegate to **send messages on behalf of** the mailbox owner. Recipients see the sender formatted as:
    > `Delegate Name on behalf of Mailbox Name`
- **Use case**:
  - Useful for formal delegation where transparency is key (e.g., an assistant emailing on behalf of an executive).

---

## External References

- Microsoft Learn: Manage permissions in Exchange Online
  - [https://learn.microsoft.com/exchange/permissions-exo/manage-permissions](https://learn.microsoft.com/exchange/permissions-exo/manage-permissions)
- Microsoft 365: Assign mailbox permissions
  - [https://learn.microsoft.com/microsoft-365/admin/email/assign-permissions](https://learn.microsoft.com/microsoft-365/admin/email/assign-permissions)

---

## Internal Tags

```
#mailbox-permissions
#exchange-online
#helpdesk
#KB
```

