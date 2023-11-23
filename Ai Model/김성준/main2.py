from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

# FastAPI 앱 생성
app = FastAPI()

# 요청 데이터 모델 정의
class UserRequest(BaseModel):
    question: str

# 모델 및 토크나이저 로딩
model = GPT2LMHeadModel.from_pretrained('C:\\Users\\gjaischool\\Documents\\GitHub\\D.O2\\Ai Model\\김성준\\saved_model')
tokenizer = PreTrainedTokenizerFast.from_pretrained('C:\\Users\\gjaischool\\Documents\\GitHub\\D.O2\\Ai Model\\김성준\\saved_model')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 엔드포인트 정의
@app.post("/chat")
def chat(request: UserRequest):
    model.eval()
    input_ids = tokenizer.encode(request.question + tokenizer.eos_token, return_tensors="pt").to(device)
    
    # 모델이 응답 생성
    with torch.no_grad():
        output = model.generate(input_ids, max_length=100)
    
    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"reply": reply}


