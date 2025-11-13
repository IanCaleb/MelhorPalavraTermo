import math
from collections import Counter

# Carregar lista de palavras de 5 letras
# With - Abre e fecha o arquivo mesmo se der algum erro
# Open - Abre o arquivo passado de parâmetro com a função de read passada tbm no parâmetro R
# As f - guarda o valor disso tudo na variavel f
# f agora é uma string gigante com todas as palavras do arquivo
with open("palavras_5letras.txt", "r", encoding="utf-8") as f:
    # Vai jogar cada palavra do arquivo dentro de uma lista chamada palavras
    palavras = [p.strip().lower() for p in f]

# Função para gerar padrão
# Compara a palavra tentada com a palavra correta e gera uma pontuação de acordo com a proximidade
# Ex: gerar_feedback("casas", "sacos")  →  "11001"

def gerar_feedback(tentativa, alvo):
    # Cria uma lista com 5 zeros que vai ser substituido por o valor do feedback
    resultado = ["0"] * 5

    # Cria uma lista com a palavra alvo
    # alvo = "sacos" -> ['s', 'a', 'c', 'o', 's']
    alvo_restante = list(alvo)

    # Verdes

    # Percorre cada letra da palavra tentativa
    for i, c in enumerate(tentativa):
        # Se a letra da tentativa no indice i for igual a letra do mesmo indice na palavra alvo
        if c == alvo[i]:
            # Vai marcar que deu verde na lista do resultado 
            resultado[i] = "2"

            # Vai marcar a letra testada como None para não ser testada dnv no amarelo
            alvo_restante[i] = None

    # Amarelos

    # Percorre cada letra da palavra tentativa
    for i, c in enumerate(tentativa):
        # Se a letra ainda não tiver sido testada e a letra tiver em algum outro lugar
        if resultado[i] == "0" and c in alvo_restante:

            # Vai marcar que a deu amarelo na lista do resultado
            resultado[i] = "1"

            # Remove a letra que foi encontrada em algum outro lugar para ela não ser testada dnv
            alvo_restante[alvo_restante.index(c)] = None

    # Gera uma string com a lista do resultado 
    # Ex: "12102"
    return "".join(resultado)

# Calcular entropia de uma palavra
def entropia(palavra, lista):
    # Vai contar quantas vezes o padrão aparece
    contagem = Counter(gerar_feedback(palavra, alvo) for alvo in lista)
    total = len(lista)
    # Converte em probabilidade (Se esse padão aparece x vezes e tem y palavras, qual a probabilidade dele aprecer)
    probs = [v / total for v in contagem.values()]
    # A formula da entropia
    return -sum(p * math.log2(p) for p in probs)

# --- 4. Avaliar todas as palavras ---
# Vai aplicar a formula de entropia para cada palavra
resultados = [(p, entropia(p, palavras)) for p in palavras]

# --- 5. Ordenar por entropia ---
# Orenar as palavras pelo resultado que deu na formula
resultados.sort(key=lambda x: x[1], reverse=True)

# --- 6. Exibir as melhores e piores ---
print("Melhores palavras:")
for p, h in resultados[:10]:
    print(f"{p}: {h:.3f} bits")

print("\nPiores palavras:")
for p, h in resultados[-10:]:
    print(f"{p}: {h:.3f} bits")