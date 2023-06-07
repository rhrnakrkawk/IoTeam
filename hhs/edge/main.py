from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Edge Server"

@app.get("/order")
async def order(table_id:int, menu:str, amount:int):
    content = f"{table_id} {menu} {amount}\n"
    
    with open("order.txt", "a") as file:
        file.write(content)
        
    return "success"

@app.get("/call")
async def call(table_id:int,call:str):
    content = f"{table_id} {call}\n"
    
    with open("call.txt", "a") as file:
        file.write(content)
        
    return "success"

@app.get("/get/order")
async def get_order():
    
    with open("order.txt", "r") as file:
        content = file.read()
    
    json = []
    if content is None:
        return "No Data"
    for line in content.split("\n"):
        if line == "":
            continue
        line = line.split(" ")
        
        table_id = line[0]
        menu = line[1]
        quantity = line[2]
        
        json.append({"table_id":table_id, "menu":menu, "amount":quantity})
    return json

@app.get("/get/call")
async def get_call():
    with open("call.txt", "r") as file:
        content = file.read()
    
    json = []
    if content is None:
        return "No Data"
    for line in content.split("\n"):
        if line == "":
            continue
        line = line.split(" ")
        
        table_id = line[0]
        call = line[1]
        
        
        json.append({"table_id":table_id, "call":call})
        
    return content

@app.get("/clear")
async def clear():
    with open("order.txt", "w") as file:
        file.write("")
        
    with open("call.txt", "w") as file:
        file.write("")
        
    return "success"