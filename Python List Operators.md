| Operation            | Syntax              | Example                    | Result                 | Type              |
| -------------------- | ------------------- | -------------------------- | ---------------------- | ----------------- |
| Creating & combining |                     |                            |                        |                   |
| Concatenate          | `a + b`             | `[1,2] + [3,4]`            | `[1, 2, 3, 4]`         | operator          |
| Repeat               | `a * n`             | `[0] * 3`                  | `[0, 0, 0]`            | operator          |
| Repeat (right)       | `n * a`             | `2 * [1,2]`                | `[1, 2, 1, 2]`         | operator          |
| Accessing elements   |                     |                            |                        |                   |
| Index                | `a[i]`              | `a[0]`                     | first item             | operator          |
| Negative index       | `a[-i]`             | `a[-1]`                    | last item              | operator          |
| Slice                | `a[i:j]`            | `a[1:3]`                   | items at index 1, 2    | operator          |
| Slice with step      | `a[i:j:k]`          | `a[::2]`                   | every other item       | operator          |
| Reverse slice        | `a[::-1]`           | `a[::-1]`                  | reversed copy          | operator          |
| Modifying in-place   |                     |                            |                        |                   |
| Assign item          | `a[i] = x`          | `a[0] = 9`                 | replaces index 0       | mutates list      |
| Assign slice         | `a[i:j] = b`        | `a[1:3] = [7,8]`           | replaces slice         | mutates list      |
| Delete item          | `del a[i]`          | `del a[0]`                 | removes index 0        | mutates list      |
| Delete slice         | `del a[i:j]`        | `del a[1:3]`               | removes slice          | mutates list      |
| Extend in-place      | `a += b`            | `a += [5,6]`               | appends b to a         | mutates list      |
| Repeat in-place      | `a *= n`            | `a *= 2`                   | doubles a in-place     | mutates list      |
| Testing membership   |                     |                            |                        |                   |
| Contains             | `x in a`            | `3 in [1,2,3]`             | `True`                 | operator          |
| Not contains         | `x not in a`        | `5 not in [1,2,3]`         | `True`                 | operator          |
| Comparing lists      |                     |                            |                        |                   |
| Equality             | `a == b`            | `[1,2] == [1,2]`           | `True`                 | operator          |
| Inequality           | `a != b`            | `[1,2] != [1,3]`           | `True`                 | operator          |
| Less than            | `a < b`             | `[1,2] < [1,3]`            | `True` (lexicographic) | operator          |
| Identity             | `a is b`            | `a is a`                   | same object in memory  | operator          |
| Useful built-ins     |                     |                            |                        |                   |
| Length               | `len(a)`            | `len([1,2,3])`             | `3`                    | method / function |
| Min / Max            | `min(a)` `max(a)`   | `min([3,1,2])`             | `1`                    | method / function |
| Sum                  | `sum(a)`            | `sum([1,2,3])`             | `6`                    | method / function |
| Sorted copy          | `sorted(a)`         | `sorted([3,1,2])`          | `[1, 2, 3]`            | method / function |
| Reversed copy        | `list(reversed(a))` | `list(reversed([1,2,3]))`  | `[3, 2, 1]`            | method / function |
| Enumerate            | `enumerate(a)`      | `for i, v in enumerate(a)` | index + value pairs    | method / function |
| Zip                  | `zip(a, b)`         | `zip([1,2],[3,4])`         | `(1,3), (2,4)`         | method / function |

The **mutates list** ones are easy to trip up on — operations like `a += b` modify the original list in-place, while `a + b` returns a new list and leaves both originals unchanged. This matters a lot when lists are passed into functions.

The **slice operators** are the most powerful and worth drilling — `a[::2]`, `a[::-1]`, and `a[i:j:k]` cover a huge range of real-world list manipulation without needing any loops.

**Lexicographic comparison** (`<`, `>`) compares lists element by element left to right, the same way Python compares strings — so `[1, 3] > [1, 2]` is `True` even though the first elements are equal.