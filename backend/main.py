from fastapi import FastAPI ,Request, HTTPException
from fastapi.templating import Jinja2Templates #html띄우기 위헤
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel #보내고 받아오기 위해
import time
from pymongo import MongoClient
from app.routers import db
from app.routers import other
from fastapi.security import APIKeyCookie, APIKeyHeader
import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from datetime import datetime
import atexit

app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(db.router)
app.include_router(other.router)


#몽고디비에서 AI(자동증가 기능 구현)
def get_next_sequence_value(sequence_name):
    sequence_doc = db.sequences.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return sequence_doc["sequence_value"]


class DataInput(BaseModel):  # 받을데이터
    data: list

# 요청 데이터 모델 정의
class UserRequest(BaseModel):
    question: str

client = MongoClient("mongodb://localhost:27017/")
db = client["chat"]
collection_user = db["User"]
collection_dialog = db["Dialog"]
collection_login = db["login"]

#post방식으로 받고
@app.post("/dobot") #POST방식으로 요청이 들어오면
def chat(data_input: DataInput):
    # 넘어오는 데이터인 DataInput를 data_input으로 지정
    # 모델 및 토크나이저 로딩
    model = GPT2LMHeadModel.from_pretrained('C:\\Users\\gjaischool\\Documents\\GitHub\\D.O\\backend\\saved_model')
    tokenizer = PreTrainedTokenizerFast.from_pretrained('C:\\Users\\gjaischool\\Documents\\GitHub\\D.O\\backend\\saved_model')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    model.eval()
    user_input = data_input.data[0]
    realtime = data_input.data[1]

   # input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, add_special_tokens=True, return_tensors="pt").to(device)
    
    # 모델이 응답 생성
    with torch.no_grad():
        output = model.generate(input_ids, max_length=100)
    
    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    if user_input in reply:
        reply = reply.replace(user_input, "").strip()


    processed_data = "알겠습니다"  #"오니까 반환하는 데이터 나중에 여기에 모델 연결
    chat_id = get_next_sequence_value("chat_id")
    today_date = datetime.now().strftime("%Y-%m-%d")

    first_document = collection_login.find_one()  # 첫 번째 도큐먼트를 가져옵니다.

    # 필요한 데이터 추출
    id_value = first_document.get("id")

    conversation = {"chat_ID": chat_id, "message": user_input, "answer": reply, "date":today_date,"id":id_value }
    inserted_data = collection_dialog.insert_one(conversation)
    
    return  {"processed_data": reply} #processed_data라는 값으로 return

#챗봇 페이지에서 뒤로 가기 누르면 홈으로 넘어가게
@app.get("/home")
def backward(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

#채팅로그 보여주는 페이지
@app.get('/review')
def review(request: Request):
    documents = list(collection_user.find({}, {"_id": 0, "message": 1, "answer":1,  "date":1} ))  # MongoDB에서 모든 문서를 리스트로 변환
    return templates.TemplateResponse("review.html", {"request": request, "documents": documents})

@app.post('/review')
def review(request: Request):
    documents = list(collection_user.find())  # 모든 문서를 리스트로 변환
    return templates.TemplateResponse("review.html", {"request": request, "documents": documents})

def cleanup_on_exit():
    collection_login.delete_many({})  # 컬렉션 내용을 모두 삭제하는 부분입니다.

atexit.register(cleanup_on_exit)