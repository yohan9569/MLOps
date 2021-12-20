import os

import sqlalchemy
from dotenv import load_dotenv


def connect(db="postgres"):

    load_dotenv(verbose=True)

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")

    url = f"postgresql://{user}:{password}@{server}:{port}/{db}"

    connection = sqlalchemy.create_engine(url)

    return connection
