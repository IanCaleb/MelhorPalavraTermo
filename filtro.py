from unidecode import unidecode

entrada = "lexico.txt"
saida = "palavras_5letras.txt"

# Pega todas as palavras com 5 letras (desconsiderando acentos)
with open(entrada, "r", encoding="utf-8") as f:
    palavras = [linha.strip() for linha in f if len(unidecode(linha.strip())) == 5]

# Salvar o novo arquivo
with open(saida, "w", encoding="utf-8") as f:
    for p in palavras:
        f.write(p + "\n")

print(f"{len(palavras)} palavras de 5 letras salvas em {saida}")