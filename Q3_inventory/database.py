import os
from sqlalchemy import create_engine,Column,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:Kiran%402004@localhost:5432/inventory_system")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

Base = declarative_base()

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer,primary_key =True,index = True)
    name = Column(String,index = True)
    count = Column(Integer,default = 0)

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer,primary_key=True,index=True)
    item_id = Column(Integer)
    timestamp = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind =engine)
    db = SessionLocal()
    try:
        item = db.query(Inventory).filter(Inventory.id == 1).first()
        if not item:
            item = Inventory(id=1,name="item A",count=100)
            db.add(item)
        else:
            item.count=100
        db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()