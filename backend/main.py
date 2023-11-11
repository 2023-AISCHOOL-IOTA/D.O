from fastapi import FastAPI ,Request
from fastapi.templating import Jinja2Templates #html띄우기 위헤
from starlette.responses import HTMLResponse
from pydantic import BaseModel #보내고 받아오기 위해


app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

class DataInput(BaseModel):  # 받을데이터
    data: str


#  responsebody통해  받아옴 넘어오는 Request는  여기서 request라고 지정
#get방식
@app.get("/")
def read_root(request: Request):
    # HTML 템플릿을 사용하여 렌더링
    return templates.TemplateResponse("soi.html", {"request": request})

#post방식으로 받고
@app.post("/")
def process_data( data_input: DataInput):
    # 넘어오는 데이터인 DataInput를 data_input으로 지정
    processed_data = "나:" + data_input.data   #"나" + 넘어온 데이터
    return {"processed_data": processed_data} #processed_data라는 값으로 return







#request: Request

