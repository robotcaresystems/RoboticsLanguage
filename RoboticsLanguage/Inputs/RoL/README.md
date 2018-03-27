# The Robotics Language


## Language notation

prefix
- `-` (`-a`)
- `+` (`+a`)

infix
- `-`  (`a-b`)
- `+`  (`a+b`)
- `*`  (`a*b`)
- `/`  (`a/b`)
- `:`  (`a:b`)

postfix


bracketing
- `{`, `}`   (`{1,2,3}`)
- `[`, `]`   (`[1,2]`)

generic
- **functionDefinition:** `define(` word `:` expression `->`expression `,` expression `|->` expression `)`
- **string:** `'` anything `'` -> `<string> anything </string>`



special
- **functions:** word `(` expression, `)` -> `<word> expression </word>`
- **languages:** word `<{` anything `}>` -> replaced using different parser

- **parenthesis:** `(` expression `)` -> expression
- **real:** `-` digits `.` digits `e`  `-` digits
- **integer:** `-` digits
