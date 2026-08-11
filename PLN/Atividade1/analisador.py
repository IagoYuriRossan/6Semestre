import re
DICIONARIO = {
    "o": ("artigo", "S"), "a": ("artigo", "S"), "um": ("artigo", "S"), "uma": ("artigo", "S"), "os": ("artigo", "P"), "as": ("artigo", "P"), "uns": ("artigo", "P"), "umas": ("artigo", "P"),
    "menino": ("substantivo", "S"), "meninos": ("substantivo", "P"), "menina": ("substantivo", "S"), "meninas": ("substantivo", "P"), "gato": ("substantivo", "S"), "gatos": ("substantivo", "P"), "professora": ("substantivo", "S"), "professoras": ("substantivo", "P"), "professor": ("substantivo", "S"), "professores": ("substantivo", "P"), "prova": ("substantivo", "S"), "provas": ("substantivo", "P"), "aluno": ("substantivo", "S"), "alunos": ("substantivo", "P"), "casa": ("substantivo", "S"), "casas": ("substantivo", "P"), "livro": ("substantivo", "S"), "livros": ("substantivo", "P"), "bola": ("substantivo", "S"), "bolas": ("substantivo", "P"), "cachorro": ("substantivo", "S"), "cachorros": ("substantivo", "P"),
    "corre": ("verbo", "S"), "correm": ("verbo", "P"), "estuda": ("verbo", "S"), "estudam": ("verbo", "P"), "dorme": ("verbo", "S"), "dormem": ("verbo", "P"), "corrigiu": ("verbo", "S"), "corrigiram": ("verbo", "P"), "leu": ("verbo", "S"), "leram": ("verbo", "P"), "brinca": ("verbo", "S"), "brincam": ("verbo", "P"), "late": ("verbo", "S"), "latem": ("verbo", "P"), "e": ("verbo", "S"), "sao": ("verbo", "P"),
    "bonito": ("adjetivo", "S"), "bonitos": ("adjetivo", "P"), "rapido": ("adjetivo", "S"), "rapidos": ("adjetivo", "P"), "novo": ("adjetivo", "S"), "novos": ("adjetivo", "P"),
    "de": ("preposicao", "-"), "em": ("preposicao", "-"), "no": ("preposicao", "S"), "na": ("preposicao", "S"), "para": ("preposicao", "-"), "com": ("preposicao", "-"), "muito": ("adverbio", "-"), "nao": ("adverbio", "-"),
}
ACENTOS = str.maketrans("áàâãéêíóôõúüç", "aaaaeeiooouuc")
def normalizar(palavra: str) -> str:
    return palavra.lower().translate(ACENTOS)
def tokenizar(frase: str) -> list[str]:
    return re.findall(r"\w+|[^\w\s]", frase, re.UNICODE)
def classificar(tokens: list[str]) -> list[dict]:
    anotados = []
    for token in tokens:
        if re.fullmatch(r"[^\w\s]", token):
            anotados.append({"token": token, "classe": "pontuacao", "numero": "-"})
            continue
        chave = normalizar(token)
        classe, numero = DICIONARIO.get(chave, ("desconhecida", "-"))
        anotados.append({"token": token, "classe": classe, "numero": numero})
    return anotados
def verificar_concordancia(anotados: list[dict]) -> list[str]:
    erros = []
    def numero_extenso(num: str) -> str:
        return "plural" if num == "P" else "singular"
    for i in range(len(anotados) - 1):
        art, sub = anotados[i], anotados[i + 1]
        if art["classe"] == "artigo" and sub["classe"] == "substantivo":
            if art["numero"] != sub["numero"]:
                erros.append(f"Concordância nominal: '{art['token']} {sub['token']}' — artigo no {numero_extenso(art['numero'])} com substantivo no {numero_extenso(sub['numero'])}.")
    for i, atual in enumerate(anotados):
        if atual["classe"] != "substantivo":
            continue
        for proximo in anotados[i + 1:]:
            if proximo["classe"] in ("adjetivo", "adverbio", "pontuacao"):
                continue
            if proximo["classe"] == "verbo":
                if atual["numero"] != proximo["numero"]:
                    erros.append(f"Concordância verbal: '{atual['token']} ... {proximo['token']}' — sujeito no {numero_extenso(atual['numero'])} com verbo no {numero_extenso(proximo['numero'])}.")
            break
    return erros
def analisar(frase: str) -> tuple[list[dict], list[str]]:
    anotados = classificar(tokenizar(frase))
    erros = verificar_concordancia(anotados)
    return anotados, erros
def exibir(frase: str) -> None:
    anotados, erros = analisar(frase)
    print(f'\nFrase: "{frase}"')
    print("-" * 60)
    print(f"{'TOKEN':<18}{'CLASSE':<16}{'NÚMERO'}")
    print("-" * 60)
    for a in anotados:
        numero = {"S": "singular", "P": "plural"}.get(a["numero"], "-")
        print(f"{a['token']:<18}{a['classe']:<16}{numero}")
    print("-" * 60)
    if erros:
        print(f"{len(erros)} erro(s) de concordância encontrado(s):")
        for erro in erros:
            print(f"  ✗ {erro}")
    else:
        print("Nenhum erro de concordância encontrado.  ✓")
FRASES_TESTE = ["A prova é nova.", "Os livros são rapidos.", "Os livro corre.", "Uma meninos estudam.", "O casas correm."]
if __name__ == "__main__":
    print("=" * 60)
    print("       ANALISADOR DE CONCORDÂNCIA EM PORTUGUÊS")
    print("=" * 60)
    for frase in FRASES_TESTE:
        exibir(frase)
