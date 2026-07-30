#Python 
# Python Lambda Function Guide

  ## What Is a Lambda Function?


A lambda is an **anonymous, single-expression function** defined inline without a `def` statement. It's useful for short throwaway functions, especially as arguments to higher-order functions.

  

**Basic Syntax:**

```python

lambda parameters: expression

```

  

- Can have **zero or more** parameters

- Contains exactly **one expression** (which is implicitly returned)

- Cannot contain statements (`if/else` blocks, loops, `return`, `print`, etc.)

  

---

  

## 1. Basic Examples

  

```python

# Named lambda (assigned to a variable)

square = lambda x: x ** 2

square(5)   # 25

  

# Multi-parameter

add = lambda x, y: x + y

add(3, 4)   # 7

  

# No parameters

greet = lambda: "Hello, World!"

greet()     # 'Hello, World!'

```

  

> **Note:** PEP 8 discourages assigning lambdas to variables. Use `def` instead for named functions — lambdas shine when passed inline.

  

---

  

## 2. Lambdas as Arguments — `sorted()`

  

The most common real-world use: passing a lambda as a `key` function.

  

```python

words = ["banana", "apple", "kiwi", "cherry"]

  

# Sort by word length

sorted(words, key=lambda w: len(w))

# ['kiwi', 'apple', 'banana', 'cherry']

  

# Sort list of dicts by a field

people = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

sorted(people, key=lambda p: p["age"])

# [{'name': 'Bob', 'age': 25}, {'name': 'Alice', 'age': 30}]

  

# Reverse sort

sorted(words, key=lambda w: len(w), reverse=True)

# ['banana', 'cherry', 'apple', 'kiwi']

```

  

---

  

## 3. Lambdas with `map()`

  

Apply a function to every item in an iterable.

  

```python

numbers = [1, 2, 3, 4, 5]

  

squares = list(map(lambda x: x ** 2, numbers))

# [1, 4, 9, 16, 25]

  

# With two iterables

products = list(map(lambda x, y: x * y, [1, 2, 3], [10, 20, 30]))

# [10, 40, 90]

```

  

> **Modern Python tip:** A list comprehension is often preferred over `map()` + lambda for readability:

> ```python

> squares = [x ** 2 for x in numbers]

> ```

  

---

  

## 4. Lambdas with `filter()`

  

Keep only items where the function returns `True`.

  

```python

numbers = [1, 2, 3, 4, 5, 6, 7, 8]

  

evens = list(filter(lambda x: x % 2 == 0, numbers))

# [2, 4, 6, 8]

  

# Filter strings by length

words = ["cat", "elephant", "ox", "hippopotamus"]

short = list(filter(lambda w: len(w) <= 3, words))

# ['cat', 'ox']

```

  

---

  

## 5. Lambdas with `reduce()`

  

Cumulatively apply a function to reduce a sequence to a single value.

  

```python

from functools import reduce

  

numbers = [1, 2, 3, 4, 5]

  

total = reduce(lambda acc, x: acc + x, numbers)

# 15  (equivalent to sum())

  

product = reduce(lambda acc, x: acc * x, numbers)

# 120

```

  

---

  

## 6. Conditional Expression in a Lambda

  

You can use a ternary `if/else` expression (not a statement) inside a lambda.

  

```python

absolute = lambda x: x if x >= 0 else -x

absolute(-7)   # 7

absolute(3)    # 3

  

classify = lambda x: "positive" if x > 0 else ("zero" if x == 0 else "negative")

classify(-5)   # 'negative'

classify(0)    # 'zero'

```

  

---

  

## 7. Immediately Invoked Lambda (IIFE)

  

Call a lambda the moment it's defined.

  

```python

result = (lambda x, y: x + y)(10, 5)

# 15

```

  

Rarely used in practice, but useful to understand when reading others' code.

  

---

  

## 8. Lambdas Returning Lambdas (Closures)

  

A lambda can return another lambda, enabling partial application.

  

```python

multiplier = lambda factor: lambda x: x * factor

  

double = multiplier(2)

triple = multiplier(3)

  

double(5)   # 10

triple(5)   # 15

```

  

---

  

## 9. Using `operator` Module Instead of Lambdas

  

For common operations, Python's `operator` module provides pre-built functions that are faster and more readable than lambdas.

  

```python

import operator

  

# Instead of: sorted(pairs, key=lambda x: x[1])

sorted([(1, 'b'), (2, 'a')], key=operator.itemgetter(1))

# [(2, 'a'), (1, 'b')]

  

# Instead of: reduce(lambda a, b: a + b, nums)

from functools import reduce

reduce(operator.add, [1, 2, 3, 4])

# 10

```

  

---

  

## Lambda vs. `def` — When to Use Which

  

| Situation | Use |

|---|---|

| Short, throwaway inline function | `lambda` |

| Key function for `sorted()`, `min()`, `max()` | `lambda` |

| Passing a simple transformation to `map()`/`filter()` | `lambda` |

| Function needs a name, docstring, or reuse | `def` |

| Logic is more than one expression | `def` |

| Multiple return paths or statements needed | `def` |

| Debugging (lambdas show as `<lambda>` in tracebacks) | `def` |

  

---

  

## Common Gotcha — Late Binding in Loops

  

Lambda captures the **variable**, not its value at definition time.

  

```python

# Bug: all lambdas return 4 (the final value of i)

funcs = [lambda: i for i in range(5)]

funcs[0]()   # 4 ← NOT 0!

  

# Fix: use a default argument to capture the value

funcs = [lambda i=i: i for i in range(5)]

funcs[0]()   # 0 ✓

funcs[3]()   # 3 ✓

```

  

---

  

## Quick Reference

  

```python

# Basic

lambda x: x + 1

  

# Multiple params

lambda x, y: x * y

  

# No params

lambda: 42

  

# Conditional expression

lambda x: "yes" if x > 0 else "no"

  

# Default argument

lambda x, n=2: x ** n

  

# With sorted

sorted(items, key=lambda x: x.attr)

  

# With map

list(map(lambda x: x * 2, items))

  

# With filter

list(filter(lambda x: x > 0, items))

  

# Closure / currying

lambda a: lambda b: a + b

```