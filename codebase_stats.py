"""
Firstly, install `uv` and `codegen` and initialize.
```
pip install uv
uv tool install codegen
codegen init
```

Then run this file:
```python codebase_stats.py```
"""

from codegen import Codebase

codebase = Codebase("./")

# Print overall stats
print("=========== Codebase Analysis ============")
print("")
print(f"📚 Total Classes: {len(codebase.classes)}")
print(f"⚡ Total Functions: {len(codebase.functions)}")
print(f"🔄 Total Imports: {len(codebase.imports)}")

# Find class with most inheritance
if codebase.classes:
    deepest_class = max(codebase.classes, key=lambda x: len(x.superclasses))
    print(f"\n🌳 Class with most inheritance: {deepest_class.name}")
    print(f"   📊 Chain Depth: {len(deepest_class.superclasses)}")
    print(f"   ⛓️ Chain: {' -> '.join(s.name for s in deepest_class.superclasses)}")

# Find first 5 recursive functions
recursive = [
    f
    for f in codebase.functions
    if any(call.name == f.name for call in f.function_calls)
][:5]
if recursive:
    print("\n🔄 Recursive functions:")
    for func in recursive:
        print(f"  - {func.name}")

# NOTE - the below is not at all accurate and flags used code as dead
# Find dead code
for func in codebase.functions:
    if len(func.usages) == 0:
        print(f"🗑️ Dead code: {func.name}")
        func.remove()
