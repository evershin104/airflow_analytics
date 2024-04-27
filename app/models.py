from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модель пользователя
class CatFacts(Base):
    __tablename__ = 'cat_facts'

    id = Column(Integer, primary_key=True)
    fact = Column(Text)
    length = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"