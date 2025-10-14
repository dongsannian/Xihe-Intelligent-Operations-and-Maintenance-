# models.py
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database import Base

# 用户表
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)  # 存哈希
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    role: Mapped[str] = mapped_column(String(20), default="user")
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

# 监控任务表
class PollTask(Base):
    __tablename__ = "poll_task"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    hardware_type: Mapped[Optional[str]] = mapped_column(String(32))
    group_name: Mapped[Optional[str]] = mapped_column(String(64))
    status: Mapped[Optional[str]] = mapped_column(String(16))
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    records: Mapped[List["PollRecord"]] = relationship(back_populates="task")

# 监控任务记录表
class PollRecord(Base):
    __tablename__ = "poll_record"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("poll_task.id"))
    device_param: Mapped[Optional[str]] = mapped_column(String(128))
    status: Mapped[Optional[str]] = mapped_column(String(16))
    record_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
    task: Mapped["PollTask"] = relationship(back_populates="records")

# 系统状态快照表
class StatusSnapshot(Base):
    __tablename__ = "status_snapshot"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gpu_usage: Mapped[Optional[str]] = mapped_column(String(16))
    cpu_usage: Mapped[Optional[str]] = mapped_column(String(16))
    memory_usage: Mapped[Optional[str]] = mapped_column(String(16))
    disk_usage: Mapped[Optional[str]] = mapped_column(String(16))
    network_status: Mapped[Optional[str]] = mapped_column(String(32))
    temperature: Mapped[Optional[str]] = mapped_column(String(16))
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    gpu_details: Mapped[List["GpuDetails"]] = relationship(back_populates="snapshot")
    cpu_details: Mapped[List["CpuDetails"]] = relationship(back_populates="snapshot")
    memory_details: Mapped[List["MemoryDetails"]] = relationship(back_populates="snapshot")
    disk_details: Mapped[List["DiskDetails"]] = relationship(back_populates="snapshot")
    network_details: Mapped[List["NetworkDetails"]] = relationship(back_populates="snapshot")

# GPU详情
class GpuDetails(Base):
    __tablename__ = "gpu_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_snapshot.id"))
    utilization: Mapped[Optional[str]] = mapped_column(String(16))
    memory_usage: Mapped[Optional[str]] = mapped_column(String(16))
    memory_used: Mapped[Optional[str]] = mapped_column(String(32))
    memory_free: Mapped[Optional[str]] = mapped_column(String(32))
    encode_utilization: Mapped[Optional[str]] = mapped_column(String(16))
    decode_utilization: Mapped[Optional[str]] = mapped_column(String(16))
    snapshot: Mapped["StatusSnapshot"] = relationship(back_populates="gpu_details")

# CPU详情
class CpuDetails(Base):
    __tablename__ = "cpu_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_snapshot.id"))
    total_usage: Mapped[Optional[str]] = mapped_column(String(16))
    core_usage: Mapped[Optional[str]] = mapped_column(String(64))
    user_usage: Mapped[Optional[str]] = mapped_column(String(16))
    kernel_usage: Mapped[Optional[str]] = mapped_column(String(16))
    io_wait: Mapped[Optional[str]] = mapped_column(String(16))
    snapshot: Mapped["StatusSnapshot"] = relationship(back_populates="cpu_details")

# 内存详情
class MemoryDetails(Base):
    __tablename__ = "memory_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_snapshot.id"))
    total: Mapped[Optional[str]] = mapped_column(String(16))
    used: Mapped[Optional[str]] = mapped_column(String(16))
    free: Mapped[Optional[str]] = mapped_column(String(16))
    buffers_cache: Mapped[Optional[str]] = mapped_column(String(16))
    swap_usage: Mapped[Optional[str]] = mapped_column(String(32))
    snapshot: Mapped["StatusSnapshot"] = relationship(back_populates="memory_details")

# 硬盘详情
class DiskDetails(Base):
    __tablename__ = "disk_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_snapshot.id"))
    read_rate: Mapped[Optional[str]] = mapped_column(String(16))
    write_rate: Mapped[Optional[str]] = mapped_column(String(16))
    io_wait: Mapped[Optional[str]] = mapped_column(String(16))
    usage: Mapped[Optional[str]] = mapped_column(String(16))
    free_space: Mapped[Optional[str]] = mapped_column(String(32))
    snapshot: Mapped["StatusSnapshot"] = relationship(back_populates="disk_details")

# 网络详情
class NetworkDetails(Base):
    __tablename__ = "network_details"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_snapshot.id"))
    upload: Mapped[Optional[str]] = mapped_column(String(16))
    download: Mapped[Optional[str]] = mapped_column(String(16))
    packet_loss: Mapped[Optional[str]] = mapped_column(String(16))
    latency: Mapped[Optional[str]] = mapped_column(String(16))
    snapshot: Mapped["StatusSnapshot"] = relationship(back_populates="network_details")

# 服务概览
class Overview(Base):
    __tablename__ = "overview"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(String(64))
    description: Mapped[Optional[str]] = mapped_column(String(128))
    menu_key: Mapped[Optional[str]] = mapped_column(String(32))

# 系统日志
class SysLog(Base):
    __tablename__ = "sys_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"))
    action: Mapped[Optional[str]] = mapped_column(String(128))
    log_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

# 告警
class Alarm(Base):
    __tablename__ = "alarm"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[Optional[str]] = mapped_column(String(32))
    content: Mapped[Optional[str]] = mapped_column(String(256))
    status: Mapped[Optional[str]] = mapped_column(String(16))
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

