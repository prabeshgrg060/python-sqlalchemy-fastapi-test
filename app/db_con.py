from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine('mysql+aiomysql://root:toor@127.0.0.1:3306/test',pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,class_=AsyncSession)

Base = declarative_base()
