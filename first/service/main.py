from typing import Annotated
from fastapi import Depends, FastAPI, Header, Path, Query, Request
from fastapi.responses import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from .schemas import UserRegister, UserLogin
import uuid
import asyncpg
from hashlib import md5

app = FastAPI()
auth = HTTPBasic()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

in_memory_token_store = {}


@app.get("/ping")
def ping():
    return "success"


@app.post("/user/register")
async def register(user: UserRegister):
    conn = await asyncpg.connect(
        host="host.docker.internal", port=5432, user="admin", password="admin", database="postgres"
    )
    await conn.execute(
        """
    INSERT INTO users (username, password, first_name, last_name, birth_date, gender, hobbies, city)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
        user.username,
        md5(user.password.encode()).hexdigest(),
        user.first_name,
        user.last_name,
        user.birth_date,
        user.gender,
        user.hobbies,
        user.city,
    )
    await conn.close()


@app.post("/login")
async def login(username: str, password: str) -> str:
    conn = await asyncpg.connect(
        host="host.docker.internal", port=5432, user="admin", password="admin", database="postgres"
    )
    result = await conn.fetch(
        "SELECT * FROM users WHERE users.username = $1 and users.password = $2",
        username,
        md5(password.encode()).hexdigest(),
    )
    if not result:
        return Response(status_code=403)
    token = str(uuid.uuid4())
    in_memory_token_store[token] = result[0]["username"]
    return  token



@app.get("/user/get/{id_}")
async def get_user(
    authorization: Annotated[str, Header()], 
    id_: Annotated[int, Path()]
):
    token = authorization
    if not token:
        return Response(status_code=403)
    token = token.split(" ")[1]
    if token not in in_memory_token_store:
        return Response(status_code=403)

    conn = await asyncpg.connect(
        host="host.docker.internal", port=5432, user="admin", password="admin", database="postgres"
    )
    results = await conn.fetch("SELECT * FROM users WHERE users.id = $1", id_)
    await conn.close()

    return results

