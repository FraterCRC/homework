FROM python:3.11-slim-bookworm

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD fastapi run service/main.py --reload
