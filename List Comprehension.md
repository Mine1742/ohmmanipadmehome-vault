#Python 

# Python List Comprehension Guide

## What Is a List Comprehension?

A list comprehension is a concise way to create a new list by applying an expression to each item in an iterable, with an optional filter condition — all in a single line.

**Basic Syntax:**

```python
[expression for item in iterable if condition]
```

---

## 1. Basic List Comprehension

**Traditional loop:**

```python
squares = []
for x in range(5):
    squares.append(x ** 2)
# [0, 1, 4, 9, 16]
```

**List comprehension equivalent:**

```python
squares = [x ** 2 for x in range(5)]
# [0, 1, 4, 9, 16]
```

---

## 2. With a Filter Condition (`if`)

Only include items that pass the condition.

```python
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

long_words = [word for word in ["hi", "hello", "hey", "howdy"] if len(word) > 3]
# ['hello', 'howdy']
```

---

## 3. With `if / else` (Ternary Expression)

Apply different transformations based on a condition.

> Note: The `if/else` goes **before** the `for`, not after.

```python
result = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']
```

---

## 4. Nested List Comprehensions

Flatten a 2D list or generate combinations.

```python
# Flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# All (x, y) pairs where x != y
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
# [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
```

---

## 5. With Functions

Call a function on each item.

```python
names = ["alice", "bob", "carol"]
capitalized = [name.capitalize() for name in names]
# ['Alice', 'Bob', 'Carol']

import math
roots = [math.sqrt(x) for x in [4, 9, 16, 25]]
# [2.0, 3.0, 4.0, 5.0]
```

---

## 6. Dictionary and Set Comprehensions

The same pattern works for `dict` and `set`.

```python
# Dict comprehension
squares_dict = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Set comprehension (removes duplicates)
unique_lengths = {len(word) for word in ["cat", "dog", "elephant", "ox"]}
# {2, 3, 8}
```

---

## 7. Walrus Operator (`:=`) in Comprehensions (Python 3.8+)

Compute a value once and use it in both the condition and expression.

```python
results = [y for x in range(10) if (y := x ** 2) > 10]
# [16, 25, 36, 49, 64, 81]
```

---

## When to Use vs. Avoid

|Use list comprehensions when...|Avoid when...|
|---|---|
|The logic is simple and readable|The expression is long or complex|
|You want a concise one-liner|You need multiple statements per item|
|Performance matters (faster than `append` loops)|Nesting is 3+ levels deep|
|Replacing `map()` + `filter()` with lambdas|Side effects are needed (logging, mutation)|

---

## Performance Note

List comprehensions are generally **faster** than equivalent `for` loops with `.append()` because they are optimized at the C level in CPython. However, if you only need to iterate (not store), a **generator expression** is more memory-efficient:

```python
# Generator — lazy evaluation, no list created in memory
total = sum(x ** 2 for x in range(1_000_000))
```

---

## Quick Reference

```python
# Basic
[expr for item in iterable]

# Filtered
[expr for item in iterable if condition]

# Conditional expression
[a if condition else b for item in iterable]

# Nested loops
[expr for x in iter1 for y in iter2]

# Dict comprehension
{key: value for item in iterable}

# Set comprehension
{expr for item in iterable}

# Generator expression
(expr for item in iterable)
```