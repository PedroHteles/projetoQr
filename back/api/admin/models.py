from sqlalchemy import  MetaData, Table, Column, Integer,VARCHAR
from sqlalchemy.dialects.mysql import \
        DECIMAL, DECIMAL,SMALLINT, \
        TINYTEXT, VARCHAR,TINYINT
from api import engine

meta = MetaData()
projetoEstoque = Table(
    'projetoEstoque' , meta,   
    Column('idProduto',Integer, primary_key=True, nullable=False),
    Column('produto' ,Integer,nullable=False),
    Column('endereco',Integer,nullable=False),
    Column('status',TINYINT(0),nullable=False)
)

meta.create_all(engine)