import requests
from models import Session, IPCA
from datetime import datetime

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"

def buscar_ipca():
    response = requests.get(URL)
    
    if response.status_code != 200:
        print("Erro ao acessar API")
        return []
    
    return response.json()


def salvar_ipca(dados):
    session = Session()

    for item in dados:
        data_original = item['data']
        data = datetime.strptime(data_original, "%d/%m/%Y").strftime("%Y-%m")
        valor = float(item['valor'].replace(',', '.')) / 100

        existe = session.query(IPCA).filter_by(data=data).first()
        
        if not existe:
            novo = IPCA(data=data, valor=valor)
            session.add(novo)

    session.commit()
    session.close()
    print("Dados do IPCA salvos com sucesso!")


if __name__ == "__main__":
    dados = buscar_ipca()
    salvar_ipca(dados)