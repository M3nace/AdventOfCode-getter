# Advent of Code - Builder

![License](https://img.shields.io/badge/license-GPL-blue.svg)
![Python](https://img.shields.io/badge/python-%3E%3D%203.6-blue.svg)

Retrieve and build directories to achieve the problems from Advent of Code.

## Output

Schema is :

```
AdventOfCode{year}
   |
   + README.md      - Contains the introduction text from the day01 problem.
   + day01
       |
       + input      - Contains your input for this day
       + README.md  - The problem wording
   + day{n}
   + day{n + 2}
   + day25
```

## Usage

```python
from aocbuilder import AoCBuilder

# Retrieve from 2015 to now
builder = AoCBuilder("<your authentication token>")
builder.build()

# You already have folders from 2017 ? Easy
builder = AoCBuilder("<your authentication token>", 2018)
builder.build()
```

## Visit

Use https://github.com/gaojiuli/tomd to convert HTML to Markdown
