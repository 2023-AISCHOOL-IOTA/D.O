from fastapi import FastAPI, Request, Form, APIRouter, HTTPException,status, Depends, Response #Depends이건 의존성 처리 위해 앤드포인트의 매개변수로 사용 먼저 실행됨
#response응답 생성
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import random
from fastapi import Request
from fastapi import Body
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pydantic import BaseModel 
import hashlib #해싱 함수 -> 주어진 입력값이 고정된 출력값으로 변환, 일방향성
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from utils.middleware import create_jwt_token 
from fastapi.responses import RedirectResponse 
from fastapi import Cookie, HTTPException
from datetime import datetime,timedelta
import requests
import secrets
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json


#주석 참조
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

class simple(BaseModel):
    title:str
    content:str
    title:str
    time:str
    number:int


SECRET_KEY = "236979CB6F1AD6B6A6184A31E6BE37DB3818CC36871E26235DD67DCFE4041492"

url = "mongodb+srv://010127js:ninosoi2001!@soi.hhnr8fk.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(url, server_api=ServerApi('1'))
db = client["chat"]
collection_user = db["User"]
collection_dialog = db["Dialog"]
collection_review = db["Review"]


#여기서 로그인 버튼을 누르면 가는건데 로그인이 되어 있으면 log를 로그아웃으로 보낼꺼고 토큰이 있으면 토큰 삭제하고 홈으로
@router.get('/login')
def gologin(request: Request, response:Response):  
    # 로그인
     token = request.cookies.get("access_token")
     if not token:
        message = "로그인을 해주세요"
        log = "login"
        return templates.TemplateResponse("login.html", {"request": request, "message": message, "log":log})
     if token:
        message = "로그인을 해주세요"
        log = "login"
        
    
        response = RedirectResponse(url="/") 
        response.delete_cookie(key="access_token")
        message = "로그인을 해주세요"
        log = "login"
        #return RedirectResponse(url="/")
        return response
     
        
            

     
@router.post('/login')
def login(user: login, response: Response):
    expires = datetime.utcnow() + timedelta(hours=1)  
    user_in_db = collection_user.find_one({"id": user.id}) #로그인시 들어온 user라는 값에 있는 id를 가지고 일치하는게 있는지 검색
    password = user.password #비밀번호는 어차피 해싱 해야 되서 그냥 그대로 

# 비밀번호를 sha256으로 해싱 -> 해싱 시 16진수의 해시값이 됨
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user_in_db is None: #-> db #일치하는 값이 없다면(맞는 아이디조차 없다면)
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    #일부러 400에러 일으킴, 이거 숫자 바꾸면 진짜 웹이나 터미널에서 그 에러 났다고 나옴 신기
    elif user_in_db["password"] != hashed_password:  #아이디는 맞지만 저장된 비밀번호가 해시비밀번호와 다르다면
        raise HTTPException(status_code=400, detail="Incorrect username or password")# 오류
    
    token = create_jwt_token(user.id) #미들웨어py에 정의한 토큰 만드는 함수 사용해 id를 가지고 토큰을 만듬
    response.set_cookie(key="access_token", value=token, httponly=False, secure=False, expires =expires.timestamp() ) 
#   #쿠키에 저장 이름: access_token, 형식: tolen,httponly: 자바스크립트에서 쿠키 접근X 보안 강화를 위해  
#   #secure: 쿠키가 https에서만 전송 될 수 있게 이게 false면 그냥 http도 됨 
   
    return {"message": "로그인 성공"}

    

@router.get('/join')
def gojoin(request: Request):
    # 회원가입
    message = "로그인을해주세요"
    return templates.TemplateResponse("sign.html", {"request": request, "message":message})

@router.post('/join')
def join(user: User):
    existing_user = collection_user.find_one({"id": user.id}) #회원가입시 중복 검사 하지만 만약 중복된 값이 넘어왔을 경우
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
    token = request.cookies.get("access_token")
    if not token:
        message = "로그인을 해주세요"
        log = "login"
        response = RedirectResponse(url="/login") 
        return response
        
    else:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("ID")
        users = collection_user.find_one({"id": user_id})
        if users:
            user_name = users.get("nickname")
            if user_name:
                message = user_name + "님 환영합니다!"
                log = "logout"
                all_documents = collection_review.find({}, {'_id': 0})
                all_document = list(all_documents)
                all_document_j = json.dumps(all_document)
                return templates.TemplateResponse("review.html", {"request": request, "message": message, "log":log ,"name":user_name+"님", "login" : True, "all_list":all_document_j})
            else :
                message = "로그인을 해주세요"
                log = "login"
                response.delete_cookie(key="access_token")
                response = RedirectResponse(url="/") 


@router.post('/review')
def review_db(request:Request, review:simple):
    token = request.cookies.get("access_token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("ID")
    users = collection_user.find_one({"id": user_id})
    user_name  = users.get("nickname")   #이걸로 들어갈 닉너임 찾기 완료

    title = review.title #가져올 제목
    content  = review.content   #가져올 내용
    date =  datetime.now().strftime("%Y-%m-%d") #가져올 날짜
    time = review.time
    number = review.number
    review_data = {"num":number,
                    "user_name":user_name,
                    "title":title,
                   "content":content,
                   "date":date,
                   "time":time}
    collection_review.insert_one(review_data)

    
    return {"user_name":user_name, "review":True}

@router.post('/check')  #아이디 중복 체크
def check_id(only: only, request: Request):
    # request를 이용한 작업 수행
    user_in_db = collection_user.find_one({"id": only.id}) #만약있다면
    if user_in_db:
        # 이미 존재하는 아이디인 경우
        raise HTTPException(status_code=400, detail="exists") #강제 에러
    
    return {"message":"sucess"}

@router.get('/user_info')
def get_user_info(request: Request):
    token = request.cookies.get("access_token")
    if not token:
       response = RedirectResponse(url="/login")
       return response  # 토큰이 없는 경우 로그인 페이지로 리디렉션
    
    user_info_list = []
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("ID")

        # collection_user에서 해당 ID와 일치하는 정보 찾기
    user_document = collection_user.find_one({"id": user_id})

    if user_document:  # 정보가 존재하는 경우
            # 사용자 정보 가져오기
            user_info = {
                "id": user_document.get("id"),
                "password": user_document.get("password"),
                "nickname": user_document.get("nickname"),
                # 필요한 정보들을 user_document로부터 가져와 user_info에 저장
            }
            user_info_list.append(user_info)
    return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info})

