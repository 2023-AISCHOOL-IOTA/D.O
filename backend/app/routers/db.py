from fastapi import FastAPI, Request, Form, APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pydantic import BaseModel #보내고 받아오기 위해
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyCookie, APIKeyHeader
from pymongo import MongoClient
import hashlib


router = APIRouter()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")


class login(BaseModel):
     id: str
     password: str
   
class User(BaseModel):
    id: str
    password: str
    name: str

class only(BaseModel):
    id: str


client = MongoClient("mongodb://localhost:27017/")
db = client["chat"]
collection_user = db["User"]
collection_login = db["login"]
collection_Dialog = db['Dialog']



@router.get('/login')
def gologin(request: Request):
    # 로그인
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/login')
def login(user: login):
    user_in_db = collection_user.find_one({"id": user.id})
    password = user.password

# 비밀번호를 sha256으로 해싱
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user_in_db is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
     
    elif user_in_db["password"] != hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    
    login_log_data = {
        "id": user_in_db["id"],
        "password":hashed_password}
    
    collection_login.insert_one(login_log_data)

    return {"message": "로그인 성공"}

    

@router.get('/join')
def gojoin(request: Request):
    # 회원가입
    return templates.TemplateResponse("join.html", {"request": request})

@router.post('/join')
def join(user: User):
     existing_user = collection_user.find_one({"id": user.id})
     if existing_user:
        return {"message": "이미 아이디가 존재합니다"}
      # 비밀번호 해시화
     hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    
     new_user = {
        "id": user.id,
        "password": hashed_password,
        "nickname": user.name
    }
     collection_user.insert_one(new_user)
     
     return {"message": "Data added successfully"}



@router.get('/review')
def review_get(request: Request):
    top_login = collection_login.find_one()  # collection_login에서 최상위 아이디 값 가져오기
    if top_login:  # 값이 존재하는 경우
        login_id = top_login.get("id")  # 가져온 로그인 정보의 ID

        # collection_Dialog에서 해당 ID와 일치하는 모든 정보 찾기
        dialog_documents = collection_Dialog.find({"id": login_id})
        
        user_info_list = []  # 대화 목록을 저장할 리스트 초기화

        if dialog_documents:  # 정보가 존재하는 경우
            for dialog_document in dialog_documents:
                # 각 대화의 정보를 가져와 user_info에 저장
                user_info = {
                    "user_message": dialog_document.get("message"),
                    "user_answer": dialog_document.get("answer"),
                    "user_date": dialog_document.get("date"),
                    # 필요한 정보들을 dialog_document로부터 가져와 user_info에 저장
                }
                user_info_list.append(user_info)  # 대화 목록에 추가

            return templates.TemplateResponse("review.html", {"request": request, "user_info_list": user_info_list})
        else:
            return templates.TemplateResponse("review.html", {"request": request, "user_info_list": []})
            # 일치하는 정보가 없는 경우 또는 처리할 정보가 없을 경우에 대한 처리
    else:
        return templates.TemplateResponse("review.html", {"request": request, "user_info_list": []})


    

@router.post('/check')
def check_id(only: only, request: Request):
    # request를 이용한 작업 수행
    user_in_db = collection_user.find_one({"id": only.id})
    if user_in_db:
        # 이미 존재하는 아이디인 경우
        raise HTTPException(status_code=400, detail="exists")
    
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/user_info')
def get_user_info(request: Request):
    top_login = collection_login.find_one()  # collection_login에서 최상위 아이디 값 가져오기
    if top_login:  # 값이 존재하는 경우
        login_id = top_login.get("id")  # 가져온 로그인 정보의 ID

        # collection_user에서 해당 ID와 일치하는 정보 찾기
        user_document = collection_user.find_one({"id": login_id})

        if user_document:  # 정보가 존재하는 경우
            # 사용자 정보 가져오기
            user_info = {
                "id": user_document.get("id"),
                "password": user_document.get("password"),
                "nickname": user_document.get("nickname"),
                # 필요한 정보들을 user_document로부터 가져와 user_info에 저장
            }

            return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info})
        else:
            return templates.TemplateResponse("user_info.html", {"request": request, "user_info": None})
            # 일치하는 정보가 없는 경우 또는 처리할 정보가 없을 경우에 대한 처리
    else:
        return templates.TemplateResponse("user_info.html", {"request": request, "user_info": None})
        # 로그인 정보가 없는 경우에 대한 처리