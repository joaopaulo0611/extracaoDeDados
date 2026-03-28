from models import Session, TipoProduto, Produto


class SQLAlchemyPipeline:
    """Pipeline que salva os produtos no banco de dados"""

    def __init__(self, tipo_nome):
        self.tipo_nome = tipo_nome
        self.session = None
        self.tipo = None

    @classmethod
    def from_crawler(cls, crawler):
        tipo_nome = crawler.spider.name
        return cls(tipo_nome)

    def open_spider(self, spider):
        """Executado quando o spider inicia"""
        self.session = Session()
        self.tipo = self.session.query(TipoProduto).filter_by(nome=self.tipo_nome).first()

        if not self.tipo:
            self.tipo = TipoProduto(nome=self.tipo_nome)
            self.session.add(self.tipo)
            self.session.commit()
            print(f'Tipo "{self.tipo_nome}" criado no banco!')
        else:
            print(f'Tipo "{self.tipo_nome}" já existe no banco.')

    def close_spider(self, spider):
        """Executado quando o spider termina"""
        self.session.close()
        print(f'Conexão com banco fechada.')

    def process_item(self, item, spider):
        """Executado para cada item coletado pelo spider"""
        produto = Produto(
            nome=item['produto'],
            preco=item['preco'],
            url=item['url'],
            tipo_id=self.tipo.id
        )
        self.session.add(produto)
        self.session.commit()

        print(f'Salvo: {item["produto"]}')
        return item
