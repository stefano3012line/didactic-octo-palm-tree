def trova_numeri_primi(n):
    numeri_primi = []
    numero = 2

    while len(numeri_primi) < n:
        is_primo = True
        for primo in numeri_primi:
            if primo * primo > numero:
                break
            if numero % primo == 0:
                is_primo = False
                break
        if is_primo:
            numeri_primi.append(numero)
        numero += 1

    return numeri_primi

n = int(input("Inserisci il numero di numeri primi da trovare: "))
primi_trovati = trova_numeri_primi(n)
print(f"I primi {n} numeri primi sono: {primi_trovati}")
