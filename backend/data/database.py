from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import select
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# --- CRUD функции ---

# async def get_user_by_email(db: AsyncSession, email: str):
#     result = await db.execute(select(User).where(User.email == email))
#     return result.scalar_one_or_none()

# async def create_user(db: AsyncSession, name: str, email: str, password: str):
#     user = User(name=name, email=email, password=password)
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user

# async def get_all_users(db: AsyncSession):
#     result = await db.execute(select(User))
#     return result.scalars().all()

# async def delete_user(db: AsyncSession, user_id: int):
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalar_one_or_none()
#     if user:
#         await db.delete(user)
#         await db.commit()
#     return user

async def create_valentine(db: AsyncSession, text: str, recipient_email: str, dispatch_date: datetime = None):
    from data.models import Valentine
    if dispatch_date is None:
        dispatch_date = datetime.now()
    valentine = Valentine(text=text, recipient_email=recipient_email, dispatch_date=dispatch_date)
    db.add(valentine)
    await db.commit()
    await db.refresh(valentine)
    return valentine