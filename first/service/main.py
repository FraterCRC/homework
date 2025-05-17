from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from .schemas import UserRegister, UserLogin
import asyncpg

app = FastAPI()
auth = HTTPBasic()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return "success"


@app.post("/user/register")
async def register(user: UserRegister):
    conn = await asyncpg.connect(
        host="localhost", port=5432, user="admin", password="admin", database="postgres"
    )
    await conn.execute(
        """
    INSERT INTO users (username, password, first_name, last_name, birth_date, gender, hobbies, city)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
        user.username,
        user.password,  # TODO: hash
        user.first_name,
        user.last_name,
        user.birth_date,
        user.gender,
        user.hobbies,
        user.city,
    )
    await conn.close()


@app.post("/login")
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(auth)]):
    conn = await asyncpg.connect(
        host="localhost", port=5432, user="admin", password="admin", database="postgres"
    )
    result = await conn.fetch(
        "SELECT * FROM users WHERE users.username = $1 and users.password = $2",
        credentials.username,
        credentials.password,
    )

    return {"access_token": result["id"], "token_type": "bearer"}


@app.post("/user/get/{id}")
async def get_user(id_: int, credentials: Annotated[HTTPBasicCredentials, Depends(auth)]):
    conn = await asyncpg.connect(
        host="localhost", port=5432, user="admin", password="admin", database="postgres"
    )
    results = await conn.fetch("SELECT * FROM users WHERE users.id = $1", id_)
    await conn.close()

    return results

