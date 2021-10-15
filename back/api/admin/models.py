from sqlalchemy import  MetaData, Table, Column, Integer,VARCHAR
from sqlalchemy.dialects.mysql import \
        DECIMAL, DECIMAL,SMALLINT, \
        TINYTEXT, VARCHAR,TINYINT,BIGINT
from sqlalchemy.sql.expression import true
from api import engine

meta = MetaData()
projetoEstoque = Table(
    'projetoEstoque' , meta,   
    Column('idProduto',Integer, primary_key=True, nullable=False,autoincrement=True),
    Column('produto' ,BIGINT,nullable=False),
    Column('endereco',BIGINT,nullable=False),
    Column('status',TINYINT(0),nullable=True)
)
meta.create_all(engine)