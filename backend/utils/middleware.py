from fastapi import Request #HTTP 요청에 대한 정보를 담고 있으며, 클라이언트로부터 받은 요청의 다양한 측면을 접근하고 조작할 수 있는 기능
from jose import JWTError, jwt
from datetime import datetime, timedelta



# 토큰을 발급하는 함수
def create_jwt_token(ID: str ):
    # 비밀 키 (secret key) - 토큰 서명에 사용됨
    SECRET_KEY = "236979CB6F1AD6B6A6184A31E6BE37DB3818CC36871E26235DD67DCFE4041492"

    # 토큰에 추가할 페이로드 (Payload) - 토큰에 포함할 정보
    payload = {
        "ID": ID,
        
    }

    # 토큰 생성
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

#메인 파일의 jwt부분 참고