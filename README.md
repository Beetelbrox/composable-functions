# Composable functions
F#-style function composition for Python. Compose functions using bitshift operators `>>` & `<<`
## Installation
TBD

## Usage
You can wrap any `Callable` with `composable` to make it a composable function. Composable functions can be composed with other `Callable` objects using the bit shift operators (`<<` & `>>`):
```python
from composable.functions import composable as c

def add_one(x: int) -> int:
    return x + 1

def add_two(x: int) -> int:
    return x + 2

c_add_one = c(add_one)
c_add_two = c(add_two)

# You can compose with other composables:
add_three = c_add_one >> c_add_two
# Equivalent to:
# add_three = lambda x: add_two(add_one(x))
add_three(5)  # == 8

# Or with any `Callable` object
add_five = c_add_one >> add_two >> add_two
# Equivalent to:
# add_five = lambda x: add_two(add_two(add_one(x)))
add_five(5)  # == 10
```
It also works as a decorator:
```python
from composable.functions import composable

@composable
def add_one(x: int) -> int:
    return x + 1

add_three = add_one >> add_one >> add_one
```
Complex pipelines can be built by reusing simple functions:
```python
from composable.functions import compose
import io

fake_stream
word_counter = (
    I >> str.strip
    >> str.split
    >> len
)
word_counter(line) == 6
```

You can also compose multiple functions at once with `compose`:

This can be useful to programatically build complex functions
