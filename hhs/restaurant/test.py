from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware

import json 
import pandas as pd
origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stock_list = {}
food_list = {}
need_ingredient_list = {}
order_list = {}
################
table_list = {}
table_order_list = {}
total_sales = 0
# 메인 페이지
@app.get("/")
def read_root():
    return {"Hello": "World"}



# 주문하기
@app.post("/order")
def order(id: int, people: int, menu: list):
    global total_sales
    order_id = id
    num_people = people
    menu_list = menu

    names = [menu_list[i] for i in range(0, len(menu_list), 3)]
    
    for name in names:
        if name not in food_list:
            return f"{name}은 메뉴에 없습니다."
        else:
            if name in need_ingredient_list.keys():
                need_list = need_ingredient_list[name]
                for ingredient,need_stock in need_list.items():
                    if stock_list[ingredient] < need_stock:
                        return f"{ingredient}의 재고가 부족합니다."
                    else:
                        stock_list[ingredient] -= need_stock
                
    prices = [menu_list[i] for i in range(1, len(menu_list), 3)]
    amounts = [menu_list[i] for i in range(2, len(menu_list), 3)]
    
    total_price = sum([int(prices[i]) * int(amounts[i]) for i in range(len(prices))])
    total_sales += total_price
    
    order_list[id]  ={
        "num_people": num_people,
        "menu": menu_list,
        "total_price": total_price,
    }
    menu_html = ""
    for i in range(len(names)):
        menu_html += f"""
        <tr>
            <td>{names[i]}</td>
            <td>{prices[i]}</td>
            <td>{amounts[i]}</td>
        </tr>
        """
    
    
    return f""""""

# 주문 내역 확인하기
@app.get("/order")
def order():
    if len(order_list) == 0:
        return "No Order."
    else:
        return order_list



# 재고 추가하기
@app.post("/stock")
def stock(name:str,amount:int):
    if name in stock_list:
        stock_list[name] += amount
    else:
        stock_list[name] = amount
        
    return {
            "name": name,
            "amount": stock_list[name],
            "msg": "Success"
        }

# 재고 확인하기
@app.get("/stock")
def stock():
    if len(stock_list) == 0:
        return "No Stock"
    else:
        return stock_list



# 음식 확인하기
@app.get("/food")
def food():
    if len(food_list) == 0:
        return "No Food"
    else:
        return food_list

# 음식 추가하기
@app.post("/food")
def food(name:str,price:int,need_ingredient:list):
    food_list[name] = {
        "price": price,
    }
    need_ingredient_list[name] = need_ingredient
    return ["음식이 정상적으로 추가되엇습니다.",
        {
        "name": name,
        "price": price,
        
        }
    ]


# 오늘의 매상
@app.get("/sales")
def sales():
    return total_sales

# 직원 호출
@app.get("/call")
def call(content:str, table:int,amount:int=0):
    if amount ==0:
        return f"{table}번 테이블에 직원을 호출했습니다."
    else:
        return f"{table}번 테이블에서 {content} {amount}개를 호출했습니다."
