# pip install ~~
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from influxdb import client as influxdb
import pymysql
import os
from datetime import datetime

# My Module
import tool
from tool import login_admin_mysql
from models import Food
from routers import restaurant_router

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 요청 정보 추출
    method = request.method
    url = request.url
    client_ip = request.client.host
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 로그 메시지 생성
    log_message = f"[{timestamp}] IP: {client_ip} - Method: {method} - URL: {url}\n"

    # 로그 파일에 기록
    with open("server_log.txt", "a") as log_file:
        log_file.write(log_message)

    response = await call_next(request)
    return response

# user router
app.include_router(restaurant_router)


@app.get("/")
async def mainpage():
    return FileResponse("front/home.html")