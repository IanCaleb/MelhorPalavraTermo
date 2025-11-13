"""
Avaliador de força de senha baseado em entropia de Shannon.

Ideia central (análoga ao seletor do Termo):
- Calculamos a distribuição empírica dos caracteres da senha (probabilidades p_i).
- Entropia por caractere: H = - Σ p_i * log2(p_i).
- Entropia total (em bits): H_total = len(senha) * H.
- Conversão para bytes: bytes = bits / 8.

Classificação (limiares simples, para apresentação):
- "ruim":     < 4 bytes  (~ < 32 bits)
- "média":    [4, 7)     (~ 32–56 bits)
- "boa":      [7, 10)    (~ 56–80 bits)
- "excelente":≥ 10 bytes (≥ 80 bits)

Observações importantes:
- Este cálculo assume independência entre caracteres e não detecta padrões comuns
  (ex.: "123456", data de nascimento, palavras de dicionário), podendo superestimar
  a segurança. Use como referência didática/estimativa rápida.
"""

import math
from collections import Counter


def shannon_entropy_bits(text: str) -> float:
    """
    Calcula a entropia de Shannon total (em bits) do texto.

    Passos:
    1) Conta a frequência de cada caractere em `text`.
    2) Converte frequências em probabilidades p_i = contagem/len(text).
    3) Calcula entropia por caractere: H_char = -Σ p_i * log2(p_i).
    4) Multiplica por n (= len(text)) para obter a entropia total: H_total = n * H_char.

    Parâmetros:
    - text: senha (ou texto) a avaliar.

    Retorno:
    - Entropia total estimada em bits (float). Retorna 0.0 se o texto estiver vazio.
    """
    if not text:
        return 0.0
    n = len(text)
    counts = Counter(text)
    probs = [c / n for c in counts.values()]
    h_per_char = -sum(p * math.log2(p) for p in probs)
    return h_per_char * n


essential_thresholds_bytes = {
    "ruim": 4.0,        # < 4 bytes (~32 bits)
    "media": 7.0,       # [4, 7) bytes
    "boa": 10.0,        # [7, 10) bytes
    # >= 10 bytes (~80 bits) -> excelente
}


def classify_password(entropy_bytes: float) -> str:
    """
    Converte a entropia (em bytes) em uma etiqueta de qualidade.

    Parâmetros:
    - entropy_bytes: entropia total estimada dividida por 8.

    Retorno:
    - Uma string entre {"ruim", "média", "boa", "excelente"}.
    """
    if entropy_bytes < essential_thresholds_bytes["ruim"]:
        return "ruim"
    if entropy_bytes < essential_thresholds_bytes["media"]:
        return "média"
    if entropy_bytes < essential_thresholds_bytes["boa"]:
        return "boa"
    return "excelente"


def main():
    """
    Fluxo principal de execução (modo interativo):
    - Lê a senha do usuário via input.
    - Calcula entropia total em bits e converte para bytes.
    - Imprime os valores e a classificação resultante.
    """
    # Entrada do usuário (não armazena nem exibe a senha, além do cálculo)
    senha = input("Digite a senha para avaliar: ")

    # Cálculo de entropia
    bits = shannon_entropy_bits(senha)
    bytes_val = bits / 8.0

    # Saída formatada para apresentação
    print(f"Entropia estimada: {bits:.2f} bits ({bytes_val:.2f} bytes)")
    print(f"Classificação: {classify_password(bytes_val)}")


if __name__ == "__main__":
    main()
