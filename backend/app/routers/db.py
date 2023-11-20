from fastapi import FastAPI, Request, Form, APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pydantic import BaseModel #보내고 받아오기 위해
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyCookie, APIKeyHeader
from pymongo import MongoClient


router = APIRouter()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")


class login(BaseModel):
    login: list
   
class User(BaseModel):
    id: str
    password: str
    name: str

client = MongoClient("mongodb://localhost:27017/")
db = client["new"]
collection_user = db["User"]
collection_dialog = db["Dialog"]
session_dict = {}



@router.get('/login')
def gologin(request: Request):
    # 로그인
    return templates.TemplateResponse("login.html", {"request": request})

@router.post('/login')
def login(user: login):
     login = user.login[0]
     password = user.login[1]
     user_in_db = collection_user.find_one({"User_id": login})
     if user_in_db is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
     
     elif user_in_db["password"] != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
     return {"message": "로그인 성공"}

@router.get('/join')
def gojoin(request: Request):
    # 삭제할 문서들의 쿼리
    return templates.TemplateResponse("join.html", {"request": request})

@router.post('/join')
def join(user: User):
    
     new_user = {
        "User_id": user.id,
        "password": user.password,
        "name": user.name
    }
     collection_user.insert_one(new_user)
     collection_dialog.update_one({"User_id": user.id}, upsert=True)
     return {"message": "Data added successfully"}


"""
@router.get('/review', response_class=HTMLResponse)
def review_get(request: Request):
    return templates.TemplateResponse("review.html", {"request": request})

@router.post('/log')
def review_post(user_id: str):
    user_data = collection_user.find_one({"User_id": user_id})
    if user_data:
        # 해당 사용자가 존재하는 경우, 대화 데이터 가져오기
        user_dialogue = collection_dialog.find({"User_id": user_id}, {"_id": 0, "message": 1, 'answer': 1})
        return user_dialogue
    else:
        return {"message": "사용자를 찾을 수 없습니다."} """

