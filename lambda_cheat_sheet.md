# Lambda Expressions Cheat Sheet

Lambda expressions are anonymous functions that are defined without a name. They are useful for short, throwaway functions, especially in cases where you don't want to formally define a full function with `def`.

---

## ✅ Python Syntax

```python
lambda arguments: expression
```

- `lambda` is the keyword
- Takes any number of arguments
- Only one expression (no statements, no return keyword)

---

## 📦 Basic Examples

```python
add = lambda x, y: x + y
print(add(3, 4))  # Output: 7

square = lambda x: x ** 2
print(square(5))  # Output: 25

is_even = lambda x: x % 2 == 0
print(is_even(6))  # Output: True
```

---

## 🔁 Used with `map()`

```python
nums = [1, 2, 3, 4]
squared = list(map(lambda x: x**2, nums))
print(squared)  # [1, 4, 9, 16]
```

---

## 🧹 Used with `filter()`

```python
nums = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4]
```

---

## 🧮 Used with `reduce()`

```python
from functools import reduce
nums = [1, 2, 3, 4]
summed = reduce(lambda x, y: x + y, nums)
print(summed)  # 10
```

---

## 📌 Sorting Custom Keys

```python
words = ['banana', 'apple', 'cherry']
words.sort(key=lambda x: len(x))
print(words)  # ['apple', 'banana', 'cherry']
```

---

## 🎛 Conditional Expressions

```python
max_value = lambda x, y: x if x > y else y
print(max_value(5, 8))  # Output: 8
```

---

## 🪜 Nested Lambdas

```python
power = lambda x: (lambda y: y ** x)
square = power(2)
print(square(4))  # Output: 16
```

---

## 🧱 Dictionary Sorting

```python
data = {'a': 5, 'b': 2, 'c': 8}
sorted_items = sorted(data.items(), key=lambda item: item[1])
print(sorted_items)  # [('b', 2), ('a', 5), ('c', 8)]
```

---

## ⏱ Timed Delay (Used with `time.sleep`)

```python
import time
delayed_print = lambda msg: time.sleep(1) or print(msg)
delayed_print("Hello after 1 second")
```

---

## 🧪 Inside List Comprehensions

```python
funcs = [lambda x: x + i for i in range(3)]
print([f(0) for f in funcs])  # [2, 2, 2] due to late binding
```

### Fix:
```python
funcs = [lambda x, i=i: x + i for i in range(3)]
print([f(0) for f in funcs])  # [0, 1, 2]
```

---

## 🔐 Lambda with Default Arguments

```python
greet = lambda name="World": f"Hello, {name}!"
print(greet())        # Hello, World!
print(greet("Alice")) # Hello, Alice!
```

---

## ❌ Limitations

- Only one expression (no multiple lines, no complex logic)
- Hard to debug
- Not reusable like named functions

---

## 📚 Good Use Cases

- Small callbacks
- One-liners for `map`, `filter`, `reduce`
- Temporary or inline functions
- Sorting or custom key functions

---

## 🤔 When Not to Use

- When logic is complex
- When function needs to be reused
- When readability is important

---

## 💬 In Other Languages

### JavaScript

```javascript
const add = (x, y) => x + y;
```

### Java (Java 8+)

```java
(x, y) -> x + y
```

### C#

```csharp
(x, y) => x + y
```

---

## 📚 References

- [Python Lambdas - Official Docs](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions)
- [PEP 8 - Lambda Guidelines](https://peps.python.org/pep-0008/#programming-recommendations)
