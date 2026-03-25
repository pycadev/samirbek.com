```python
def tub(val: int) -> bool:
    if val <= 1:
        return False
    for i in range(2, int(val ** 0.5) + 1):
        if val % i == 0:
            return False
    return True
n = int(input())
print(tub(n))
```