# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.hash import bcrypt
from database import get_db
from models import User

router = APIRouter()

@router.post("/register")
def register(payload: dict, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")
    phone = payload.get("phone", "")
    if not username or not password:
        raise HTTPException(400, "缺少用户名或密码")
    exists = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if exists:
        raise HTTPException(400, "用户名已存在")
    u = User(username=username, password=bcrypt.hash(password), phone=phone)
    db.add(u); db.commit()
    return {"message": "注册成功"}

@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        raise HTTPException(400, "缺少用户名或密码")
    u = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not u or not bcrypt.verify(password, u.password):
        raise HTTPException(400, "用户名或密码错误")
    return {"message": "登录成功"}

@router.post("/reset-password")
def reset_password(payload: dict, db: Session = Depends(get_db)):
    phone = payload.get("phone")
    new_password = payload.get("new_password")
    if not phone or not new_password:
        raise HTTPException(400, "缺少手机号或新密码")
    u = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not u:
        raise HTTPException(400, "手机号未注册")
    u.password = bcrypt.hash(new_password)
    db.commit()
    return {"message": "重置成功"}

