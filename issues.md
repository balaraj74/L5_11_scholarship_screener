# Static Code Analysis Issue Tracking Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **B307 (eval)** | Security | 11 | Use of `eval()` on user-controlled merit formula permits arbitrary code execution | Replace `eval()` with a secure AST-based mathematical expression evaluator restricted to binary operations |
| **W0102 (dangerous-default-value)** | Bug / Logic | 14 | Mutable default argument `logs=[]` is shared across function invocations, causing state leakage | Replace default with `None` and instantiate a fresh list inside the function body |
| **W0702 (bare-except)** | Code Smell | 36 | Bare `except:` catch-all block silences critical system interrupts and runtime errors | Specify explicit exception tuple `(FileNotFoundError, json.JSONDecodeError, OSError)` |
| **R1732 / W1514 (file-handling)** | Resource Leak | 28, 34 | Raw `open()` calls without context managers or explicit UTF-8 character encoding | Wrap file I/O operations in `with open(..., encoding="utf-8")` context managers |
| **F401 (unused-import)** | Style | 2, 3 | Unused imports `math` and `sys` consume namespace overhead | Remove unused imports from top of script |
| **E712 (comparison-to-true)** | Style | 42 | Explicit comparison `== True` violates PEP 8 idiom | Refactor to idiomatic boolean test `if results[r]["eligible"]:` |
| **C0103 (invalid-name)** | Style | 39 | Function `printShortlist` does not conform to snake_case naming | Refactor to `print_shortlist` and assign backward-compatible alias |
| **C0114 / C0116 (missing-docstring)** | Documentation | 1, 11-39 | Missing module and function docstrings | Add comprehensive docstrings detailing contracts, args, and returns |
