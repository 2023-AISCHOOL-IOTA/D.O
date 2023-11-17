from fastapi import FastAPI ,Request, HTTPException
from fastapi.templating import Jinja2Templates #html띄우기 위헤
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel #보내고 받아오기 위해
import time
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")
app.mount("/static", StaticFiles(directory="static"), name="static")


class DataInput(BaseModel):  # 받을데이터
    data: list

class login(BaseModel):
    login: list
   
class User(BaseModel):
    id: str
    password: str
    name: str

client = MongoClient("mongodb://localhost:27017/")


db = client["new"]
collection = db["User"]





#  responsebody통해  받아옴 넘어오는 Request는  여기서 request라고 지정
#get방식
@app.get("/")
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    return templates.TemplateResponse("home.html", {"request": request})  #이 주소로 요청이 오면 HOME이 열리게

@app.get("/dobot") # 로고 누르면 여기로 요청이 옴 그럼이 HTML이 열림
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    return templates.TemplateResponse("dobot.html", {"request": request})

#post방식으로 받고
@app.post("/dobot") #POST방식으로 요청이 들어오면
def process_data( data_input: DataInput):
    # 넘어오는 데이터인 DataInput를 data_input으로 지정

    user_input = data_input.data[0]
    realtime = data_input.data[1]

    processed_data = "알겠습니다!"   #"오니까 반환하는 데이터 나중에 여기에 모델 연결
    conversation = {"user_input": user_input, "timestamp": realtime, "processed_data":processed_data}
    inserted_data = collection.insert_one(conversation)
    time.sleep(0.6) #대화 느낌  주기 위해 time.sleep
    return  {"processed_data": processed_data} #processed_data라는 값으로 return

#챗봇 페이지에서 뒤로 가기 누르면 홈으로 넘어가게
@app.get("/home")
def backward(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

"""
@app.post("/model_response") #POST방식으로 요청이 들어오면
def process_data( data_input: DataInput):
    # 넘어오는 데이터인 DataInput를 data_input으로 지정


    processed_data = "알겠습니다"   #"오니까 반환하는 데이터 나중에 여기에 모델 연결
    time.sleep(0.6) #대화 느낌  주기 위해 time.sleep
    return  {"processed_data": processed_data} #processed_data라는 값으로 return """

@app.get('/review')
def review(request: Request):
    documents = list(collection.find({}, {"_id": 0, "user_input": 1, "timestamp": 1, "processed_data":1} ))  # MongoDB에서 모든 문서를 리스트로 변환
    return templates.TemplateResponse("review.html", {"request": request, "documents": documents})
    
@app.post('/review')
def review(request: Request):
    documents = list(collection.find())  # 모든 문서를 리스트로 변환
    return templates.TemplateResponse("review.html", {"request": request, "documents": documents})

@app.get('/login')
def Gologin(request: Request):
    # 삭제할 문서들의 쿼리
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/login')
def login(user: login):
     login = user.login[0]
     password = user.login[1]
     user_in_db = collection.find_one({"User_id": login})
     if user_in_db is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
     
     elif user_in_db["password"] != password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
     return {"message": "로그인 성공"}

@app.get('/join')
def Gologin(request: Request):
    # 삭제할 문서들의 쿼리
    return templates.TemplateResponse("join.html", {"request": request})

@app.post('/join')
def Gologin(user: User):
    # 삭제할 문서들의 쿼리
     new_user = {
        "User_id": user.id,
        "password": user.password,
        "name": user.name
    }
     collection.insert_one(new_user)
     return {"message": "Data added successfully"}
