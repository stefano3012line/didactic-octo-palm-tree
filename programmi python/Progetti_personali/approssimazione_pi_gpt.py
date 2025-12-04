import math

def gauss_legendre_pi(num_iterations):
    a = 1.0
    b = 1.0 / math.sqrt(2)
    t = 0.25
    p = 1.0

    for _ in range(num_iterations):
        a_next = (a + b) / 2
        b = math.sqrt(a * b)
        t -= p * (a - a_next) ** 2
        a = a_next
        p *= 2

    approx_pi = (a + b) ** 2 / (4 * t)
    return approx_pi

num_iterations = 1000000000 # Numero di iterazioni da utilizzare
approx_pi = gauss_legendre_pi(num_iterations)
print(f"Approssimazione di π con {num_iterations} iterazioni: {approx_pi}")

