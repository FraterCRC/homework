from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import UserRegister, UserLogin
import asyncpg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def read_root():
    return "success"


@app.post("/api/v1/create_user")
async def register(user: UserRegister):
    conn = await asyncpg.connect(
        host="localhost", port=5432, user="admin", password="admin"
    )
    await conn.execute(
        """
    INSERT INTO users (username, password, first_name, last_name, birth_date, gender, hobbies, city)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
        user.username,
        user.password,
        user.first_name,
        user.last_name,
        user.birth_date,
        user.gender,
        user.hobbies,
        user.city,
    )
    await conn.close()


@app.post("/login")
async def login(user: UserLogin):
    conn = await asyncpg.connect(
        host="localhost", port=5432, user="admin", password="admin"
    )
    result = await conn.fetch(
        "SELECT * FROM users WHERE users.username = $1 and users.password = $2",
        user.username,
        user.password,
    )


@app.post("/user/get/{id}")
async def get_user(id: str):
    conn = await asyncpg.connect(
        host="localhost", port=5432, user="admin", password="admin"
    )
    await conn.fetch("SELECT * FROM users WHERE users.id = $1", id)
    await conn.close()
