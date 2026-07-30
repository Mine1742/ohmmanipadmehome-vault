# Networking KB

## CCNA KB

### OSPF Knowledge Base

#### Stub Area vs Totally Stubby Area vs Not-So-Stubby Area (NSSA)

---

### 👉 First: What is an OSPF Area?

- OSPF (Open Shortest Path First) is a link-state routing protocol.
- Large OSPF networks are divided into areas to improve scalability.
- All areas must connect to **Area 0 (the backbone area)**.
- To optimize routing, certain areas can be configured as **Stub**, **Totally Stubby**, or **Not-So-Stubby**.

---

### 📦 1. Stub Area

#### 🔹 What It Is:
A Stub Area blocks **external routes** (Type 5 LSAs) from entering the area.

#### 🔧 How It Works:
- Instead of receiving external routes, the ABR injects a **default route (0.0.0.0)** into the area.
- Reduces routing table size and complexity.

#### ✅ Use Case:
- Ideal for simple networks or branch offices that don't require full routing knowledge.

#### ❌ Restrictions:
- No external routes allowed.
- All routers in the area must be configured as stub routers.

---

### 📦 2. Totally Stubby Area (TSA)

#### 🔹 What It Is:
A Cisco-specific enhancement of the stub area. It blocks even more types of routes.

#### 🔧 How It Works:
- Blocks both:
  - **External LSAs** (Type 5)
  - **Inter-area LSAs** (Type 3 & 4)
- ABR injects only a **default route**.

#### ✅ Use Case:
- Ideal for very simple branch sites that only need a default route to reach everything.

---

### 📦 3. Not-So-Stubby Area (NSSA)

#### 🔹 What It Is:
Allows limited external routing by letting internal ASBRs inject external routes.

#### 🔧 How It Works:
- Blocks **external LSAs (Type 5)** from outside.
- Allows **internal ASBRs** to inject external routes using **Type 7 LSAs**.
- ABR translates Type 7 LSAs into Type 5 LSAs when forwarding them to other areas.

#### ✅ Use Case:
- Ideal for branch sites that connect to external networks (e.g., partner networks or ISPs).

---

### 🔄 Summary Comparison Table

| Feature                    | Stub Area     | Totally Stubby Area | Not-So-Stubby Area |
|----------------------------|---------------|----------------------|--------------------|
| Allows External Routes In? | ❌ No (Type 5) | ❌ No (Type 5, 3, 4)  | ❌ No (Type 5), ✅ Type 7 inside |
| Allows Inter-Area Routes?  | ✅ Yes         | ❌ No                | ✅ Yes             |
| Allows Internal ASBR?      | ❌ No          | ❌ No                | ✅ Yes             |
| Injects Default Route?     | ✅ Yes         | ✅ Yes               | ✅ Yes             |
| Best For?                  | Small branches| Very simple sites    | Branches with external links |

---

## 🏋️ OSPF LSA Types

| LSA Type | Description                                 | Originator              |
|----------|---------------------------------------------|-------------------------|
| Type 1   | Router LSA - Lists directly connected links | All routers             |
| Type 2   | Network LSA - Multi-access networks         | DR (Designated Router)  |
| Type 3   | Summary LSA - Inter-area routes             | ABR                     |
| Type 4   | Summary ASBR - Info about ASBR              | ABR                     |
| Type 5   | External LSA - External routes (e.g., BGP)  | ASBR                    |
| Type 6   | Multicast OSPF (MOSPF)                      | (Rarely used)           |
| Type 7   | NSSA External - Used in NSSA areas          | ASBR inside NSSA        |

---

## 💡 OSPF Neighbor States

1. **Down** – No Hello packets seen.
2. **Init** – Hello received, but router ID not seen in it.
3. **2-Way** – Bidirectional communication established.
4. **ExStart** – Master/slave negotiation starts.
5. **Exchange** – Routers exchange DBDs (Database Descriptions).
6. **Loading** – Routers request missing LSAs.
7. **Full** – Full adjacency is formed.

> ✨ Only DRs and BDRs reach "Full" state with all routers in multi-access networks.

---

## 📈 OSPF Cost Metrics & Path Selection

- OSPF uses **cost** as its metric: `Cost = Reference Bandwidth / Interface Bandwidth`
- Default reference bandwidth is **100 Mbps**
- Lower cost = preferred path

### Example:
- FastEthernet (100 Mbps): `100 / 100 = 1`
- Gigabit Ethernet (1 Gbps): `100 / 1000 = 0.1 → rounded to 1` (appears same unless ref bandwidth is increased)

You can change the reference bandwidth to support high-speed links:
```bash
auto-cost reference-bandwidth 10000
```

---

## 🔐 OSPF Authentication

OSPF supports three types of authentication:
1. **None** – Default (no auth)
2. **Plaintext Password** – Simple but insecure
3. **MD5 Authentication** – Secure and widely used

### Config Example:
```bash
interface GigabitEthernet0/0
  ip ospf authentication message-digest
  ip ospf message-digest-key 1 md5 YourPassword
```

> Authentication must be consistent across all routers in the area.

