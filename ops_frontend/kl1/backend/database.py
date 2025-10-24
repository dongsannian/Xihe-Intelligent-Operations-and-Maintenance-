from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 使用SQLite作为默认数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./logmanager.db"
# 如果使用MySQL，可替换为:
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/logmanager"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite特定参数
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
