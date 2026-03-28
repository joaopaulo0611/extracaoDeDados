from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class TipoProduto(Base):
    """Tabela de tipos de produto (arroz, café, açúcar, etc)"""
    __tablename__ = 'tipo_produto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    produtos = relationship('Produto', back_populates='tipo')

    def __repr__(self):
        return f'<TipoProduto(id={self.id}, nome={self.nome})>'


class Produto(Base):
    """Tabela de produtos"""
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    preco = Column(String(50))
    url = Column(String(500))
    tipo_id = Column(Integer, ForeignKey('tipo_produto.id'), nullable=False)
    tipo = relationship('TipoProduto', back_populates='produtos')

    def __repr__(self):
        return f'<Produto(id={self.id}, nome={self.nome}, preco={self.preco})>'

class IPCA(Base):
    __tablename__ = 'ipca'

    id = Column(Integer, primary_key=True)
    data = Column(String(10), nullable=False)
    valor = Column(Float, nullable=False)

    def __repr__(self):
        return f'<IPCA(data={self.data}, valor={self.valor})>'

engine = create_engine('sqlite:///produtos.db', echo=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
