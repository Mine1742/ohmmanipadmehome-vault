[[Database Hub]]
# 🔗 Understanding SQL Joins in Relational Databases

Joins are used in SQL to combine rows from two or more tables based on a related column between them.

---

## 🟦 1. INNER JOIN

### 📌 Description:
Returns **only the rows** that have matching values in **both** tables.

### 🧠 Example:
```sql
SELECT employees.name, departments.name
FROM employees
INNER JOIN departments ON employees.dept_id = departments.id;
```

### 🔄 Use Case:
Retrieve employees **with** a department assigned.

---

## 🟩 2. LEFT JOIN (or LEFT OUTER JOIN)

### 📌 Description:
Returns **all rows from the left table**, and matched rows from the right table. Returns `NULL` for no match.

### 🧠 Example:
```sql
SELECT employees.name, departments.name
FROM employees
LEFT JOIN departments ON employees.dept_id = departments.id;
```

### 🔄 Use Case:
Get all employees, **even if** they don't belong to a department.

---

## 🟥 3. RIGHT JOIN (or RIGHT OUTER JOIN)

### 📌 Description:
Returns **all rows from the right table**, and matched rows from the left. Returns `NULL` where there is no match.

### 🧠 Example:
```sql
SELECT employees.name, departments.name
FROM employees
RIGHT JOIN departments ON employees.dept_id = departments.id;
```

### 🔄 Use Case:
See all departments, **even if** they have no employees.

---

## 🟨 4. FULL OUTER JOIN

### 📌 Description:
Returns **all rows** from both tables. `NULL` is shown where there is no match.

### 🧠 Example:
```sql
SELECT employees.name, departments.name
FROM employees
FULL OUTER JOIN departments ON employees.dept_id = departments.id;
```

### 🔄 Use Case:
Combine data to see all employees and all departments, regardless of relationships.

---

## 🟪 5. CROSS JOIN

### 📌 Description:
Returns the **Cartesian product** of both tables — every row from the first table paired with every row from the second.

### 🧠 Example:
```sql
SELECT employees.name, shifts.name
FROM employees
CROSS JOIN shifts;
```

### 🔄 Use Case:
Generate combinations, like assigning all employees to every shift option.

---

## 🔍 Bonus: SELF JOIN

### 📌 Description:
A table joins to itself to compare rows within the same table.

### 🧠 Example:
```sql
SELECT a.name AS Employee, b.name AS Manager
FROM employees a
JOIN employees b ON a.manager_id = b.id;
```

---

## 📌 Summary Table

| Join Type       | Includes Unmatched Left | Includes Unmatched Right | All Combinations |
|------------------|--------------------------|---------------------------|------------------|
| INNER JOIN        | ❌                       | ❌                        | ❌               |
| LEFT JOIN         | ✅                       | ❌                        | ❌               |
| RIGHT JOIN        | ❌                       | ✅                        | ❌               |
| FULL OUTER JOIN   | ✅                       | ✅                        | ❌               |
| CROSS JOIN        | ❌                       | ❌                        | ✅               |

---
