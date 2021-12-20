import os  # os를 제어할 수 있는 모듈

from dotenv import load_dotenv
from sqlalchemy import create_engine  # db랑 object 연결. Object-Relational Mapping
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(verbose=True)  # .env 읽어서 불러오기


def connect(db):
    """
    database와의 연결을 위한 함수입니다.

    Args:
        db(str): 사용할 데이터베이스의 이름을 전달받습니다.

    Returns:
        created database engine: 데이터베이스에 연결된 객체를 반환합니다.

    Examples:
        >>> engine = connect("my_db")
        >>> query = "SHOW timezone;"
        >>> engine.excute(query).fetchall()
        [('Asia/Seoul',)]
        >>> print(engine)
        Engine(postgresql://postgres:***@127.0.0.1:5432/my_db)
    """
    print(db)

    POSTGRES_USER = os.getenv("POSTGRES_USER")  # 로드된 환경 변수를 담는다.
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        + f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{db}"
    )

    connection = create_engine(SQLALCHEMY_DATABASE_URL)

    return connection


POSTGRES_DB = os.getenv("POSTGRES_DB")
engine = connect(POSTGRES_DB)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
# session 테이블에 내용물 넣을 때 사용하자
Base = declarative_base()
# 테이블 만들 때 사용. # 상속클래스들을 자동으로 인지하고 알아서 매핑해줌.
