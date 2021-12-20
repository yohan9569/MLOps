from app import tables
from app.database import engine

# 테이블 만들기 실행 여기서 테크 멘토님 추천
tables.Base.metadata.create_all(bind=engine)
