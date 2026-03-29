# extracaoDeDados

## Tutorial Extração de Dados

O projeto pode ser encontrado em:
https://github.com/joaopaulo0611/extracaoDeDados

## Passo a passo:
1. Baixar o zip <br />
2. Se certificar que têm python baixado, os comandos vão variar como “python” ou “py” dependendo das configurações. Neste tutorial estamos usando “py”. <br />
3. Abrir o projeto em um ambiente de execução, como o Visual Studio Code <br />
4. Delete o arquivo “produtos.db”, já que o banco de dados está carregado com outros dados de testes prévios. <br />
5. Utilizar os seguintes comandos: <br />
py -m pip install sqlalchemy scrapy pandas requests beautifulsoup4 lxml <br />
py ipca_api.py <br />
py -m scrapy runspider acucar.py <br />
py -m scrapy runspider arroz.py <br />
py -m scrapy runspider feijao.py <br />
py -m scrapy runspider cafe.py <br />
py -m scrapy runspider oleo.py <br />
py analise.py
