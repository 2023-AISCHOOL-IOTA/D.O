from fastapi import FastAPI, Request, APIRouter, HTTPException, Response # API라우터 앤드포인트를 구조화 하기 위해 사용 HTTPException 예외 처리 하기 위한 클래스 일부러 에러 일으킬 수 있음
from fastapi.templating import Jinja2Templates #메인 파일 주석 참조
from fastapi.staticfiles import StaticFiles#메인 파일 주석 참조
from fastapi.security import APIKeyCookie, APIKeyHeader
from pymongo import MongoClient#메인 파일 주석 참조
from utils.middleware import create_jwt_token #메인 파일 주석 참조
from jose import JWTError, jwt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi#메인 파일 주석 참조

SECRET_KEY = "236979CB6F1AD6B6A6184A31E6BE37DB3818CC36871E26235DD67DCFE4041492"
#그외 모아둔 라우터
router = APIRouter()  # apirouter이라는 인스턴스 생성
#메인 파일 주석 참조



url = "mongodb+srv://010127js:ninosoi2001!@soi.hhnr8fk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url, server_api=ServerApi('1'))
db = client["chat"]
collection_user = db["User"]



# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")


#  responsebody통해  받아옴 넘어오는 Request는  여기서 request라고 지정
#get방식
@router.get("/" )
def read_home(request: Request, response: Response):
    token = request.cookies.get("access_token")
    message = ""
    if not token:
        message = "로그인을 해주세요"
        log = "login"
        return templates.TemplateResponse("home.html", {"request": request, "message": message, "log": log})
    else:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("ID")
        
        users = collection_user.find_one({"id": user_id})
        
        log  = "logout"
        
        if users:
            user_name = users.get("nickname")
            message = user_name + "님 환영합니다!"
            log  = "logout"
              
    
    return templates.TemplateResponse("home.html", {"request": request, "message": message, "log":log})


@router.get("/chat")
def read_dobot(request: Request, response: Response):
    token = request.cookies.get("access_token")
    if not token:
        message = "로그인을 해주세요"
        log = "login"
        return templates.TemplateResponse("login.html", {"request": request, "message": message, "log": log})
    else:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("ID")
        users = collection_user.find_one({"id": user_id})
        log  = "logout"
        if users:
            user_name = users.get("nickname")
            message = user_name + "님 안녕하세요!"
            log  = "logout"
              
    return templates.TemplateResponse("chat.html", {"request": request, "message": message, "log": log, "chat_end": True})



@router.get("/map")
def map(request:Request, response: Response):
    token = request.cookies.get("access_token")
    if not token:
        message = "로그인을 해주세요"
        log = "login"
        
    else:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("ID")
        users = collection_user.find_one({"id": user_id})
        if users:
            user_name = users.get("nickname")
            if user_name:
                message = user_name + "님 안녕하세요!"
            else:
                message = "사용자 이름이 없습니다."
            log  = "logout"
        

    return templates.TemplateResponse("map.html", {"request": request, "message": message, "log":log})



    
@router.get("/menu")
def map(request:Request, response: Response):
    token = request.cookies.get("access_token")
    if not token:
        message = "로그인을 해주세요"
        log = "login"
        
    else:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("ID")
        users = collection_user.find_one({"id": user_id})
        if users:
            user_name = users.get("nickname")
            if user_name:
                message = user_name + "님 안녕하세요!"
            else:
                message = "사용자 이름이 없습니다."
            log  = "logout"

    return templates.TemplateResponse("menu.html", {"request": request, "message": message, "log":log})


@router.get("/game")
def map(request:Request):
    token = request.cookies.get("access_token")
    if not token:
        message = "로그인을 해주세요"
        log = "login"
        
    else:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("ID")
        users = collection_user.find_one({"id": user_id})
        if users:
            user_name = users.get("nickname")
            if user_name:
                message = user_name + "님 안녕하세요!"
            else:
                message = "사용자 이름이 없습니다."
            log  = "logout"
    return templates.TemplateResponse("game.html",  {"request": request, "message": message, "log":log})