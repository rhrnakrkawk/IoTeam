from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Edge Server"

@app.get("/order")
async def order(table_id:int, menu:str, quantity:int):
    content = f"{table_id} {menu} {quantity}\n"
    
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
    
    # json = []
    # if content is None:
    #     return "No "
    # for line in content.split("\n"):
    #     if line == "":
    #         continue
    #     line = line.split(" ")
        
    #     table_id = line[0]
    #     menu = line[1]
    #     quantity = line[2]
        
    #     json.append({"table_id":table_id, "menu":menu, "quantity":quantity})
    return content

@app.get("/get/call")
async def get_call():
    with open("call.txt", "r") as file:
        content = file.read()
    
    
        
    return content

@app.get("/clear/order")
async def clear():
    with open("order.txt", "w") as file:
        file.write("")
    return "success"

@app.get("/clear/call")
async def clear():
    with open("call.txt", "w") as file:
        file.write("")
    return "success"