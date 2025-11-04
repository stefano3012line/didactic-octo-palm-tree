def sieve_of_atkin(limit):
    # Initialize the sieve array
    sieve = [False] * (limit + 1)

    # Set up the basic patterns for the algorithm
    for x in range(1, int(limit ** 0.5) + 1):
        for y in range(1, int(limit ** 0.5) + 1):
            n = 4 * x**2 + y**2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                sieve[n] = not sieve[n]

            n = 3 * x**2 + y**2
            if n <= limit and n % 12 == 7:
                sieve[n] = not sieve[n]

            n = 3 * x**2 - y**2
            if x > y and n <= limit and n % 12 == 11:
                sieve[n] = not sieve[n]

    # Mark all multiples of squares as non-prime
    for x in range(5, int(limit ** 0.5) + 1):
        if sieve[x]:
            for y in range(x**2, limit + 1, x**2):
                sieve[y] = False

    # Add 2 and 3 to the list of primes
    primes = [2, 3]

    # Add other primes found in the sieve
    for n in range(5, limit + 1):
        if sieve[n]:
            primes.append(n)

    return primes

# Example usage:
limit =3000000
result = sieve_of_atkin(limit)
print(f"Prime numbers up to {limit}: {result}")
print(len(result))
