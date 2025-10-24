"""
MySQL 数据库初始化脚本
- 自动创建数据库（若不存在）
- 创建日志表结构（适配 LogEntry 模型）
- 插入初始测试数据
- 支持命令行参数配置数据库连接
"""
import argparse
import pymysql
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum

# ------------------------------
# 配置参数（请根据你的 MySQL 环境修改）
# ------------------------------
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3306
DEFAULT_USER = "root"  # 你的 MySQL 用户名
DEFAULT_PASSWORD = "666"  # 你的 MySQL 密码
DEFAULT_DB_NAME = "logmanager"  # 数据库名称
TABLE_NAME = "log_entries"  # 日志表名称


# ------------------------------
# 日志级别枚举（与 models.py 保持一致）
# ------------------------------
class LogLevel(enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ------------------------------
# 数据模型（与项目中的 LogEntry 同步）
# ------------------------------
Base = declarative_base()

class LogEntry(Base):
    """日志表结构定义"""
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True, autoincrement=True, comment="日志ID")
    source = Column(String(100), nullable=False, comment="日志来源（如服务名、模块名）")
    level = Column(SQLEnum(LogLevel), nullable=False, comment="日志级别")
    message = Column(String(1000), nullable=False, comment="日志内容")
    module = Column(String(100), nullable=True, comment="所属模块")
    line_number = Column(Integer, nullable=True, comment="行号")
    extra = Column(String(2000), nullable=True, comment="额外信息（JSON字符串等）")
    timestamp = Column(DateTime, default=datetime.utcnow, comment="日志时间戳（UTC）")

    def __repr__(self):
        return f"<LogEntry(id={self.id}, level={self.level}, message={self.message[:30]})>"


# ------------------------------
# 核心初始化函数
# ------------------------------
def create_database_if_not_exists(host, port, user, password, db_name):
    """创建数据库（如果不存在）"""
    try:
        # 先连接到 MySQL 服务器（不指定数据库）
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            cursorclass=DictCursor,
            charset="utf8mb4"
        )
        with conn.cursor() as cursor:
            # 检查数据库是否存在
            cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name}'")
            if not cursor.fetchone():
                # 创建数据库（指定字符集和排序规则）
                cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅ 数据库 '{db_name}' 已创建")
            else:
                print(f"ℹ️ 数据库 '{db_name}' 已存在，跳过创建")
        conn.close()
    except Exception as e:
        raise RuntimeError(f"创建数据库失败：{str(e)}")


def init_tables_and_data(host, port, user, password, db_name):
    """创建表结构并插入初始数据"""
    # 构建 MySQL 连接 URL
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    
    # 创建引擎和会话
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建所有表（基于 Base 定义的模型）
    Base.metadata.create_all(bind=engine)
    print(f"✅ 表结构已创建（表名：{TABLE_NAME}）")
    
    # 插入测试数据
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if not db.query(LogEntry).first():
            test_logs = [
                LogEntry(
                    source="system",
                    level=LogLevel.INFO,
                    message="数据库初始化完成，系统启动正常",
                    module="init_mysql_db.py",
                    line_number=100
                ),
                LogEntry(
                    source="user_service",
                    level=LogLevel.WARNING,
                    message="用户登录次数超限，暂时锁定",
                    module="auth.py",
                    line_number=45
                ),
                LogEntry(
                    source="db_connection",
                    level=LogLevel.ERROR,
                    message="连接超时，尝试重连成功",
                    module="database.py",
                    line_number=22,
                    extra='{"retry_count": 3, "duration": 5.2}'
                )
            ]
            db.add_all(test_logs)
            db.commit()
            print(f"✅ 已插入 {len(test_logs)} 条测试日志数据")
        else:
            print("ℹ️ 表中已存在数据，跳过测试数据插入")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"插入测试数据失败：{str(e)}")
    finally:
        db.close()


def main():
    # 解析命令行参数（允许运行时覆盖默认配置）
    parser = argparse.ArgumentParser(description="MySQL 数据库初始化脚本（日志管理系统）")
    parser.add_argument("--host", type=str, default=DEFAULT_HOST, help=f"MySQL 主机地址（默认：{DEFAULT_HOST}）")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"MySQL 端口（默认：{DEFAULT_PORT}）")
    parser.add_argument("--user", type=str, default=DEFAULT_USER, help=f"MySQL 用户名（默认：{DEFAULT_USER}）")
    parser.add_argument("--password", type=str, default=DEFAULT_PASSWORD, help=f"MySQL 密码（默认：{DEFAULT_PASSWORD}）")
    parser.add_argument("--db-name", type=str, default=DEFAULT_DB_NAME, help=f"数据库名称（默认：{DEFAULT_DB_NAME}）")
    
    args = parser.parse_args()
    
    try:
        # 步骤1：创建数据库（若不存在）
        create_database_if_not_exists(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            db_name=args.db_name
        )
        
        # 步骤2：创建表和初始数据
        init_tables_and_data(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            db_name=args.db_name
        )
        
        print("\n🎉 数据库初始化完成！可通过以下信息连接：")
        print(f"地址：{args.host}:{args.port}")
        print(f"数据库名：{args.db_name}")
        print(f"表名：{TABLE_NAME}")
    except Exception as e:
        print(f"\n❌ 初始化失败：{str(e)}")


if __name__ == "__main__":
    main()