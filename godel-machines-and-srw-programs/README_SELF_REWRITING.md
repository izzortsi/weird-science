# Minimal Self-Rewriting Lisp Program

This is a demonstration of a self-modifying program in Common Lisp, showcasing Lisp's homoiconic nature (code as data).

## Concept

The program `self-rewriting.lisp` demonstrates self-modification by:

1. **Reading itself**: Opens and reads its own source code as a string
2. **Modifying itself**: Finds and increments a generation counter in its own code
3. **Writing itself**: Overwrites its source file with the modified version

Each time you run it, the `*generation*` parameter increases by 1.

## How It Works

```lisp
(defparameter *generation* 0)  ; This number increments each run
```

The program:
- Searches for the line `(defparameter *generation* N)`
- Parses the current number `N`
- Increments it to `N+1`
- Rewrites the entire source file with the new value

## Running the Program

### Prerequisites

You need a Common Lisp implementation installed:
- **SBCL** (Steel Bank Common Lisp): `sudo apt install sbcl`
- **CLISP**: `sudo apt install clisp`
- **CCL** (Clozure Common Lisp)
- **ECL** (Embeddable Common Lisp)

### Execution

With SBCL:
```bash
sbcl --script self-rewriting.lisp
```

With CLISP:
```bash
clisp self-rewriting.lisp
```

Or make it executable:
```bash
chmod +x self-rewriting.lisp
./self-rewriting.lisp
```

### Example Output

```
Current generation: 0
Rewriting myself...
Done! Next generation will be: 1
```

Run it again:
```
Current generation: 1
Rewriting myself...
Done! Next generation will be: 2
```

## Why This Works in Lisp

Lisp is **homoiconic**: code and data share the same representation (S-expressions). This makes self-modification natural:

1. Lisp code is just lists
2. Lists can be manipulated as data
3. Modified data can be written back as code

This is harder in most languages where code and data are fundamentally different.

## Educational Value

This demonstrates:
- **Homoiconicity**: Code as data
- **Metaprogramming**: Programs that modify programs
- **File I/O**: Reading and writing source files
- **String manipulation**: Parsing and modifying code text
- **Self-reference**: A program that knows itself

## Limitations

This simple version uses string manipulation rather than proper S-expression parsing. A more robust version would:
- Use `read` to parse the code into S-expressions
- Modify the S-expression structure
- Use `print` to write it back formatted

But that would be less "minimal"!

## Variations

Try modifying it to:
- Count total number of times run (across multiple parameters)
- Add timestamps to track execution history
- Generate new functions on each run
- Evolve its own behavior based on results
