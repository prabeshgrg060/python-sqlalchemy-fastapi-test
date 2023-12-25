from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db_con import engine
from app.db.db_schema import user
from app.db.data_models import Usermodel, userget
import logging
from datetime import datetime, time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger(__name__)

total_sessions = 0

def check_time_range():

    current_time = datetime.now().time()

    start_time = time(20, 35)  # 8:10 PM
    end_time = time(20, 36)     # 9:00 PM

    if start_time <= current_time <= end_time:
        return False

    return True


async def get_db():
    global total_sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,class_=AsyncSession)
    async with SessionLocal() as db:
        total_sessions+=1
        try:
            if total_sessions >9 and check_time_range() :
                await asyncio.sleep(120)
            yield db
        finally:
            await db.close()
            total_sessions-=1
            print(f'total connection are {total_sessions}')

@router.post('/user/')
async def create_user(user_data: Usermodel, db: Session = Depends(get_db)):
    try:
        new_user = user(name=user_data.name, age=user_data.age)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except Exception as e:
        logger.error(f"Error occurred while creating user: {e}")
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{name}", response_model=Usermodel)
async def read_user_me(name: str, db: Session = Depends(get_db)):
    try:
        user_data = await db.execute(select(user).where(user.name == name))
        user_instance = user_data.scalars().first()
        if user_instance is None:
            raise HTTPException(status_code=404, detail="User not found")

        return Usermodel(name=user_instance.name, age=user_instance.age)

    except Exception as e:
        logger.error(f"Error occurred while reading user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
