from config import Settings
from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
# Инициализация базы данных
# main_engine = sa.create_engine(url=Settings.DATABASE_URL_psycopg,
#     echo=True,
#     pool_size=5,
#     max_overflow=10


# Инициализация настроек
settings = Settings()

# Инициализация базы данных
Base = declarative_base()
# Важно! Нужно вызвать свойство DATABASE_URL_psycopg, а не передавать его как объект
main_engine = sa.create_engine(settings.DATABASE_URL_psycopg,echo=True,
    pool_size=5,
    max_overflow=10)

# Создание сессии
DBSession = sessionmaker(bind=main_engine, expire_on_commit=False)

@contextmanager
def session_scope():
    """Обеспечивает транзакционный контекст для операций."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == '__main__':
    with session_scope() as s:
        # Выполнение простого запроса для проверки соединения
        try:
            result = s.execute(sa.text('SELECT version()'))
            # print(result.all())
        except Exception as e:
            print(f"Не удалось подключиться к базе данных: {e}")


