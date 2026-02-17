# === Recursivitate: Fibonacci Recursiv ===
# Fibonacci - calculat recursiv (ineficient pentru n mare)
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

# Exemplu de utilizare pentru Fibonacci Recursiv
n = 6
print(f"Fibonacci({n}) =", fibonacci(n))  # Output: 8


# === Recursivitate: Factorial ===
# Factorial - calculat recursiv
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Exemplu de utilizare pentru Factorial
n = 5
print(f"Factorial({n}) =", factorial(n))  # Output: 120


