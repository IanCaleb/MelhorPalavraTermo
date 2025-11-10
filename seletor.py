import math
from collections import Counter

with open("palavras_5letras.txt", "r", encoding="utf-8") as f:
    palavras = [p.strip().lower() for p in f]

def gerar_feedback(tentativa, alvo):
    resultado = ["0"] * 5
    alvo_restante = list(alvo)

    # Verdes
    for i, c in enumerate(tentativa):
        if c == alvo[i]:
            resultado[i] = "2"
            alvo_restante[i] = None

    # Amarelos
    for i, c in enumerate(tentativa):
        if resultado[i] == "0" and c in alvo_restante:
            resultado[i] = "1"
            alvo_restante[alvo_restante.index(c)] = None
    return "".join(resultado)

# Calcular entropia de uma palavra
def entropia(palavra, lista):
    contagem = Counter(gerar_feedback(palavra, alvo) for alvo in lista)
    total = len(lista)
    probs = [v / total for v in contagem.values()]
    return -sum(p * math.log2(p) for p in probs)

# Avaliar todas as palavras 
resultados = [(p, entropia(p, palavras)) for p in palavras]

# Ordenar por entropia
resultados.sort(key=lambda x: x[1], reverse=True)

# Exibir as melhores e piores
print("Melhores palavras:")
for p, h in resultados[:10]:
    print(f"{p}: {h:.3f} bits")

print("\nPiores palavras:")
for p, h in resultados[-10:]:
    print(f"{p}: {h:.3f} bits")