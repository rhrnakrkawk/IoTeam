# 가게측에서 사용하는 API를 정의한 파일입니다.

from typing import Optional
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import FileResponse
from influxdb import client as influxdb
import pymysql
from pydantic import BaseModel
import os
import datetime

from .internal import food_router as food
from .internal import ingredient_router as ingredient
from .internal import table_router as table

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

router.include_router(food)
router.include_router(ingredient)
router.include_router(table)


@router.get("/")
async def restaurant_mainpage():
    return "Restaurant Router"
