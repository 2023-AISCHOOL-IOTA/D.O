from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyCookie, APIKeyHeader
from pymongo import MongoClient
import atexit


#그외 모아둔 라우터
router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client["chat"]
collection_user = db["User"]
collection_login = db["login"]


# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")


#  responsebody통해  받아옴 넘어오는 Request는  여기서 request라고 지정
#get방식
@router.get("/")
def read_home(request: Request):
    top_login = collection_login.find_one()  # 최상위 로그인 정보 가져오기
    if top_login:  # 값이 존재하는 경우
        login_id = top_login.get("id")  # 가져온 로그인 정보의 ID
        user_document = collection_user.find_one({"id": login_id})  # 해당 ID로 사용자 정보 찾기
        if user_document:  # 사용자 정보가 존재하는 경우
            user_name = user_document.get("nickname")  # 사용자 닉네임 가져오기
            message  = user_name+ "님 안녕하세요!"
            
        else:
              message = "로그인을 해주세요"
              
    else:
        message = "로그인을 해주세요"
    return templates.TemplateResponse("home.html",{"request": request, "message":message})
    
    

@router.get("/dobot")
def read_dobot(request: Request):
    top_login = collection_login.find_one()  # 최상위 로그인 정보 가져오기
    if top_login:  # 값이 존재하는 경우
        login_id = top_login.get("id")  # 가져온 로그인 정보의 ID
        user_document = collection_user.find_one({"id": login_id})  # 해당 ID로 사용자 정보 찾기
        if user_document:  # 사용자 정보가 존재하는 경우
            user_name = user_document.get("nickname")  # 사용자 닉네임 가져오기
            return templates.TemplateResponse("dobot.html", {"request": request, "user_name": user_name})
        else:
            return templates.TemplateResponse("dobot.html", {"request": request})
    else:
        message="로그인을 먼저 진행해 주세요"
        return templates.TemplateResponse("login.html", {"request": request})



@router.get("/map")
def map(request:Request):
    return templates.TemplateResponse("map.html", {"request": request})

@router.get("/menu")
def map(request:Request):
    return templates.TemplateResponse("menu.html", {"request": request})