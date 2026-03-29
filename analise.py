from models import Session, Produto, TipoProduto, IPCA

session = Session()

# PADRONIZAR
def converter_preco(preco_str):
    if not preco_str:
        return None
    
    try:
        preco_str = preco_str.replace(",", ".")
        return float(preco_str)
    except:
        return None

# BUSCA
def get_produtos(tipo_nome):
    return (
        session.query(Produto)
        .join(TipoProduto)
        .filter(TipoProduto.nome == tipo_nome)
        .all()
    )


def menor_preco(tipo):
    produtos = get_produtos(tipo)
    
    produtos_validos = [
        p for p in produtos if converter_preco(p.preco) is not None
    ]

    return min(produtos_validos, key=lambda x: converter_preco(x.preco))


def maior_preco(tipo):
    produtos = get_produtos(tipo)
    
    produtos_validos = [
        p for p in produtos if converter_preco(p.preco) is not None
    ]

    return max(produtos_validos, key=lambda x: converter_preco(x.preco))

# MONTAR CESTAS
cesta_min = {
    "arroz": menor_preco("arroz"),
    "feijao": menor_preco("feijao"),
    "oleo": menor_preco("oleo"),
    "acucar": menor_preco("acucar"),
    "cafe": menor_preco("cafe"),
}

cesta_max = {
    "arroz": maior_preco("arroz"),
    "feijao": maior_preco("feijao"),
    "oleo": maior_preco("oleo"),
    "acucar": maior_preco("acucar"),
    "cafe": maior_preco("cafe"),
}

# CÁLCULO DE TOTAL
def total(cesta):
    valores = []

    for tipo, produto in cesta.items():
        preco = converter_preco(produto.preco)
        if preco is None:
            continue

        # quantidade correta
        if tipo == "feijao":
            preco *= 2

        valores.append(preco)

    return sum(valores)

# IPCA
def calcular_ipca_acumulado(ano):
    dados = session.query(IPCA).order_by(IPCA.data).all()
    
    acumulado = 1

    for d in dados:
        try:
            ano_dado = int(d.data.split("-")[0])
        except:
            continue

        if ano_dado >= ano:
            acumulado *= (1 + d.valor)

    return acumulado - 1

# AJUSTE (DEFLAÇÃO)
def ajustar_preco(preco_atual, ipca):
    return preco_atual / (1 + ipca)

# RELATÓRIOS
def imprimir_cesta(nome, cesta):
    print(f"\n===== {nome} =====")
    total_cesta = 0

    for tipo, produto in cesta.items():
        preco = converter_preco(produto.preco)

        if preco is None:
            continue

        if tipo == "feijao":
            preco *= 2

        total_cesta += preco
        
        print(f"{tipo.upper()}: {produto.nome} - R$ {preco:.2f}")

    print(f"TOTAL: R$ {total_cesta:.2f}")
    return total_cesta


def relatorio_ipca(cesta_total):
    print("\n===== VALOR DA CESTA EM ANOS ANTERIORES =====")
    
    for ano in range(2015, 2025):
        ipca = calcular_ipca_acumulado(ano)
        valor = ajustar_preco(cesta_total, ipca)
        
        print(f"{ano}: R$ {valor:.2f} (IPCA acumulado: {ipca*100:.2f}%)")

# EXECUTAR
if __name__ == "__main__":
    total_min = imprimir_cesta("CESTA MAIS BARATA", cesta_min)
    total_max = imprimir_cesta("CESTA MAIS CARA", cesta_max)

    print("\n--- CESTA MAIS BARATA ---")
    relatorio_ipca(total_min)

    print("\n--- CESTA MAIS CARA ---")
    relatorio_ipca(total_max)

    session.close()