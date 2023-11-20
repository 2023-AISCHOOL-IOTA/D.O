from fastapi import FastAPI ,Request, HTTPException
from fastapi.templating import Jinja2Templates #html띄우기 위헤
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel #보내고 받아오기 위해
import time
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.routers import db
from app.routers import other
from pymongo import MongoClient
from fastapi.security import APIKeyCookie, APIKeyHeader


app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(db.router)
app.include_router(other.router)


class DataInput(BaseModel):  # 받을데이터
    data: list


#client = MongoClient("mongodb://localhost:27017/")
#collection2 = db["Dialog"]


#post방식으로 받고
@app.post("/dobot") #POST방식으로 요청이 들어오면
def process_data( data_input: DataInput):
    # 넘어오는 데이터인 DataInput를 data_input으로 지정

    user_input = data_input.data[0]
    realtime = data_input.data[1]

    processed_data = "알겠습니다!"   #"오니까 반환하는 데이터 나중에 여기에 모델 연결
    conversation = {"message": user_input, "timestamp": realtime, "answer":processed_data}
    #inserted_data = collection2.insert_one(conversation)
    time.sleep(0.6) #대화 느낌  주기 위해 time.sleep
    return  {"processed_data": processed_data} #processed_data라는 값으로 return

#챗봇 페이지에서 뒤로 가기 누르면 홈으로 넘어가게
@app.get("/home")
def backward(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

