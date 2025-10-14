from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database import Base

# 用户角色枚举
class UserRole(str, enum.Enum):
    ADMIN = "管理员"       # 管理员 - 拥有所有权限
    MEMBER = "会员"        # 会员 - 拥有部分高级权限
    USER = "普通用户"      # 普通用户 - 基础权限

# 日志级别枚举
class LogLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, comment="用户名")
    email = Column(String(100), unique=True, index=True, comment="邮箱")
    hashed_password = Column(String(255), comment="密码哈希")
    full_name = Column(String(100), nullable=True, comment="用户姓名")
    role = Column(Enum(UserRole), default=UserRole.USER, comment="用户角色")
    is_active = Column(Boolean, default=True, comment="账号是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关联日志记录（移除comment参数）
    logs = relationship("LogEntry", back_populates="user")

# 日志模型
class LogEntry(Base):
    __tablename__ = "log_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), index=True, comment="日志来源")
    level = Column(Enum(LogLevel), index=True, comment="日志级别")
    message = Column(Text, comment="日志内容")
    module = Column(String(100), nullable=True, comment="产生日志的模块")
    line_number = Column(Integer, nullable=True, comment="行号")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="时间")
    extra = Column(Text, nullable=True, comment="额外信息")
    
    # 用户关联
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True, comment="用户ID")
    # 移除relationship中的comment参数
    user = relationship("User", back_populates="logs")
    