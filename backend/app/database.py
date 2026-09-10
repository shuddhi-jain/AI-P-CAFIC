from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(settings.database_url, echo=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit= False
)

with engine.connect() as connection:
    print("Database connected successfully")


Base.metadata.create_all(bind=engine)

   