import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from core.workflow import run_repair_loop

test_case_1 = """
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def preorder(root, res):
    if not root:
        return
    
    preorder(root.left, res)
    res.append(root.val)
    preorder(root.right, res)

root = Node(1)
root.left = Node(2)
root.right = Node(3)

res = []
preorder(root, res)
print(res)
"""

test_case_2 = """
def fib(n, memo={}):
    if n <= 1:
        return n

    if n in memo:
        return memo[0]   # BUG: wrong key returned

    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

print(fib(10))
"""

print("--- Testing Case 1 (Recursion) ---")
history1 = run_repair_loop(test_case_1)
for step in history1:
    print(f"Iteration {step['iteration']}: {step['status']}")
    if step['patch'] and step['patch']['patch_applied']:
        print(f"  Patch: {step['patch']['explanation']}")
        print(f"  Diff: {step['patch']['diff']}")

print("\n--- Testing Case 2 (Memoization) ---")
history2 = run_repair_loop(test_case_2)
for step in history2:
    print(f"Iteration {step['iteration']}: {step['status']}")
    if step['patch'] and step['patch']['patch_applied']:
        print(f"  Patch: {step['patch']['explanation']}")
        print(f"  Diff: {step['patch']['diff']}")
