from fastapi import FastAPI ,Request
from fastapi.templating import Jinja2Templates #html띄우기 위헤
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel #보내고 받아오기 위해
import time

app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
class DataInput(BaseModel):  # 받을데이터
    data: str


#  responsebody통해  받아옴 넘어오는 Request는  여기서 request라고 지정
#get방식
@app.get("/")
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    return templates.TemplateResponse("nes.html", {"request": request})

@app.get("/soi.html")
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    return templates.TemplateResponse("soi.html", {"request": request})

#post방식으로 받고
@app.post("/soi.html")
def process_data( data_input: DataInput):
    # 넘어오는 데이터인 DataInput를 data_input으로 지정


    processed_data = "알겠습니다"+"<br>"   #"오니까 반환하는 데이터 나중에 여기에 모델 연결
    time.sleep(0.5) #대화 느낌  주기 위해 time.sleep
    return  {"processed_data": processed_data} #processed_data라는 값으로 return