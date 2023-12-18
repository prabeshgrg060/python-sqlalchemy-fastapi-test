from sqlalchemy import create_engine, Column, String , Integer , CHAR, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('mysql+mysqlconnector://root:toor@127.0.0.1:3306/test')

Base = declarative_base()

class user(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key = True)
    name = Column(String(255),index = True)
    age = Column(Integer)

# class bill(Base):
#     __tablename__ = "bill"
#     user_id = Column(Integer , ForeignKey('user.id'))
#     id = Column(Integer , primary_key = True)
#     product_name = Column(String(255))
#     total = Column(Integer)

Base.metadata.create_all(engine)

# session = sessionmaker(bind = engine)
# Session = session()

# new_user = user(name='Ben' , age = 30)

# Session.add(new_user)

# Session.commit()

# Session.close()
