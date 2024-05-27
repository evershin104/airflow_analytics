from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модель пользователя
class RubRatesHistory(Base):
    __tablename__ = 'exchange_rates_rub'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    timestamp = Column(TIMESTAMP)
    value = Column(Float)

    def __repr__(self):
        return f"<RUB(timestamp='{self.timestamp}', value='{self.value}')>"