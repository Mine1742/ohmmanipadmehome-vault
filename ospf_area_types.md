# Stub Area vs Totally Stubby Area vs Not-So-Stubby Area (NSSA)

## 🧭 First: What is an OSPF Area?

- OSPF (Open Shortest Path First) is a link-state routing protocol.
- Large OSPF networks are divided into areas to improve scalability.
- All areas must connect to **Area 0 (the backbone area)**.
- To optimize routing, certain areas can be configured as **Stub**, **Totally Stubby**, or **Not-So-Stubby**.

---

## 📦 1. Stub Area

### 🔹 What It Is:
A Stub Area blocks **external routes** (Type 5 LSAs) from entering the area.

### 🔧 How It Works:
- Instead of receiving external routes, the ABR injects a **default route (0.0.0.0)** into the area.
- Reduces routing table size and complexity.

### ✅ Use Case:
- Ideal for simple networks or branch offices that don't require full routing knowledge.

### ❌ Restrictions:
- No external routes allowed.
- All routers in the area must be configured as stub routers.

---

## 📦 2. Totally Stubby Area (TSA)

### 🔹 What It Is:
A Cisco-specific enhancement of the stub area. It blocks even more types of routes.

### 🔧 How It Works:
- Blocks both:
  - **External LSAs** (Type 5)
  - **Inter-area LSAs** (Type 3 & 4)
- ABR injects only a **default route**.

### ✅ Use Case:
- Ideal for very simple branch sites that only need a default route to reach everything.

---

## 📦 3. Not-So-Stubby Area (NSSA)

### 🔹 What It Is:
Allows limited external routing by letting internal ASBRs inject external routes.

### 🔧 How It Works:
- Blocks **external LSAs (Type 5)** from outside.
- Allows **internal ASBRs** to inject external routes using **Type 7 LSAs**.
- ABR translates Type 7 LSAs into Type 5 LSAs when forwarding them to other areas.

### ✅ Use Case:
- Ideal for branch sites that connect to external networks (e.g., partner networks or ISPs).

---

## 🔄 Summary Comparison Table

| Feature                    | Stub Area     | Totally Stubby Area | Not-So-Stubby Area |
|----------------------------|---------------|----------------------|--------------------|
| Allows External Routes In? | ❌ No (Type 5) | ❌ No (Type 5, 3, 4)  | ❌ No (Type 5), ✅ Type 7 inside |
| Allows Inter-Area Routes?  | ✅ Yes         | ❌ No                | ✅ Yes             |
| Allows Internal ASBR?      | ❌ No          | ❌ No                | ✅ Yes             |
| Injects Default Route?     | ✅ Yes         | ✅ Yes               | ✅ Yes             |
| Best For?                  | Small branches| Very simple sites    | Branches with external links |
