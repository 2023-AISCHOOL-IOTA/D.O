from fastapi import FastAPI ,Request, HTTPException #HTTPException 는 문제 발생시 상태 코드와 함께 해당 예외 발생 시켜 알려줌
from fastapi.templating import Jinja2Templates #HTML 템플릿을 렌더링하기 위해 fast api는 api서버 구축이여서 html랜더링 못함 -> 진자사용하면 동적 가능 안쓰면 css나, js처럼  static에 넣기, 근데 이럼 정적이 됨
from fastapi.staticfiles import StaticFiles#정적파일들을 쓰기 위해 가져옴
from pydantic import BaseModel #데이터 모델 정의하기 위해 사용 형식정의, request response 에서 유효성 검사
from jose import JWTError, jwt # JWT(Jason Web Tokens) 웹 토큰 기반의 인증방식 -> 아래 자세히 쓰겠음
from pymongo import MongoClient# 몽고디비
from app.routers import db # 라우터  쓰기 위해,  import db라는 이름의 라우터를 쓰겠다
from app.routers import other # 라우터  쓰기 위해, import other 라는 이름의 라우터를 쓰겠다
from fastapi.security import APIKeyCookie, APIKeyHeader
import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast #트랜스포머
from datetime import datetime #날짜 가져오기
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.middleware import create_jwt_token #미들웨어에 있는 토큰 발급 함 수 쓰기 위해
"""미들웨어란? ->  middleware란 모든 리퀘스트에 대해 path operation이 수행되기전 실행되는 함수를 말한다.
프론트 엔드와 백엔드 사이?
만들고 @app.middleware("http")이렇게 해야 하는데 코드 짜면서 계속 순환 오류 나서
그냥 미들웨어란 이름의 파이썬 파일로 만들었다(미들웨이 기능 안하고 필요할때 호출 만 함)
,
JWT(Jason Web Tokens) 인증을 위한 웹토큰 인증 방식 로그인 같이 사용자 인증이 필요 시 사용
로그인 시 아이디와 SECRET_KEY 이용 및 HS256라는 알고리즘(해싱시 사용) 사용해 복잡한 토큰이라는 문자열을 만듬
이 토큰을 헤더나 쿠키에 저장해 서버에 함께 전송
서버에서 토큰을 받아 이 토큰의 상태를 확인하고 인증된 사람인지 확인함
jwt 서명은 헤더(타입, 사용된 알고리즘), 패이로드(안에 들어간 정보), 서명(이 두가지를 합쳐서 만든 서명)
서명 생성시 사용한 키는 알려지면 안됨
서명 검증시 토큰을 받고 다시 헤더와 페이로드에서 값을 꺼내 만들때와 동일한 방식으로 조합 해 확인
만약 다르다면 유효하지 않음"""


app = FastAPI() #app이라는 이름으로 fast api 인스턴스를 생성하곘다

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates/html") # fast api에서 html파일을 랜더링 하기위해 jinja2 사용 디렉토리는 위치 
app.mount("/static", StaticFiles(directory="static"), name="static") #정적 파일들 static파일들을 제공 "/static" url  이 경로 로 가면 된다 
# app.mount: fast api에 특정 경로를 지정하여 정적 파일을 제공
# StaticFiles(directory="static"): fast api의 staticRiles를 사용해 정적파일을 제공할 수 있는 설정을 구성
#directory="static" 실제 파일 의 디렉토리 
#name: 다음에 정적 파일 경로 참조 시 사용 이름
# "{{ url_for('static', path= 'css/dobot.css')}}" static이라는 이름을 가진 경로에서 실제 path안에 있는 상대 경로에 있는 파일을 가져오겠다
app.include_router(db.router) # 이 db라는 파일에서 정의된 라우터를 현재 fast api인스턴스에 추가하겠다
app.include_router(other.router) #이 other이라는 파일에서 정의된 라우터를 현재 fast api인스턴스에 추가하겠다

SECRET_KEY = "236979CB6F1AD6B6A6184A31E6BE37DB3818CC36871E26235DD67DCFE4041492" #암호화시 사용하는 시크릿키 보통 32바이트의 길이 나 그 이상 

#몽고디비에서 AI(자동증가 기능 구현)
def get_next_sequence_value(sequence_name):
    sequence_doc = db.sequences.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return sequence_doc["sequence_value"]


class DataInput(BaseModel):  # DataInput이라는 이름으로 받을 데이터 정의함
    data: list

client = MongoClient("mongodb://localhost:27017/") #pymongo사용해 DB에 연결 서버주소
db = client["chat"] #chat이라는 이름의 데에터베이스 선택
collection_user = db["User"] #user이라는 이름의 컬렉션 생성or선택 (이렇게 쓴다고 만 해도 없으면 몽고디비가 알아서 생성해줌)
collection_dialog = db["Dialog"] #Dialog이라는 이름의 컬렉션 생성 or 선택


#post방식으로 요청이 들어오면 이 아래 정의 된 함수들을 실행 하겠다 
@app.post("/dobot")
def chat(data_input: DataInput,request: Request):  #DataInput은 위에 형식을 정의
    token = request.cookies.get("access_token") #request는 http요청 정보 가지고 있음  -> 이걸 받은 이유 : 이안에 토큰이 있는 쿠키가 있다
    if not token:  #토큰이 없다  -> 아예 로그인시 발급받는 토큰이 없다-> 로그인 이 안됐다
        return templates.TemplateResponse("login.html", {"request": request}) #로그인 페이지로 보냄
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("ID")
#이제 이 아이디를 가지고 collection_user에서 nickname가져와서 return해주는 코드 연결 예정

    # 넘어오는 데이터인 DataInput를 data_input으로 지정
    # 모델 및 토크나이저 로딩
    user_input = data_input.data[0] # 사용자의 메세지 넘어온 데이터(list)중 0번째에 있음
    



    processed_data = "알겠습니다"  #"오니까 반환하는 데이터 나중에 여기에 모델 연결
    #chat_id = get_next_sequence_value("chat_id") #위에 만든 몽고디비에서 AI구현 코드 호출 만든 값을 chat _id라는 변수에 넣기 
    today_date = datetime.now().strftime("%Y-%m-%d") #날짜위해 년-월-일 형식으로 시간 




    conversation = { "message": user_input, "answer": processed_data, "date":today_date, id:user_id}
    inserted_data = collection_dialog.insert_one(conversation)
    #user_input, 모델에서 나온 값, 날짜, 유저 아이디를 제이슨 타입으로 묶기 
	  # collection_dialog에 제이슨 형식으로 넣기(원래 몽고디비 넣을때 제이슨 형식  처럼 key value형식으로 넣어야 함