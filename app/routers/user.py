from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db_con import SessionLocal
from app.db.db_schema import user
from app.db.data_models import Usermodel, userget
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

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
