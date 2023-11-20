from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import BertTokenizer, BertForSequenceClassification

app = FastAPI()

# 토크나이저와 모델 초기화
tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
model = BertForSequenceClassification.from_pretrained('monologg/kobert', num_labels=4436, state_dict=torch.load('model_file_path.pth'))
model.eval()

class Item(BaseModel):
    sentence: str

@app.post("/predict")
def predict(item: Item):
    # 문장을 모델에 입력하기 위해 토크나이징
    inputs = tokenizer(item.sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # 모델로부터 예측 수행
    with torch.no_grad():
        outputs = model(**inputs)

    # 예측 결과 추출
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    prediction = probabilities.argmax().item()

    return {"prediction": prediction}
