from fastapi import FastAPI

app = FastAPI(
    title="Edge Server",
)

@app.get("/")
async def root():
    return "Edge Server"

@app.get("/order")
async def order(table_id:int, menu:str, amount:int):
    content = f"{table_id} {menu} {amount}\n"
    read_content =""
    with open("order.txt", "r") as file:
        read_content = file.read()
    
    for read in read_content.split("\n"):
        if read == "":
            continue
        read = read.split(" ")
        
        read_table_id = read[0]
        read_menu = read[1]
        read_amount = read[2]
        
        if table_id == int(read_table_id) and menu == read_menu:
            amount += int(read_amount)
            content = f"{table_id} {menu} {amount}\n"
            read_content = read_content.replace(f"{read_table_id} {read_menu} {read_amount}", content)
            break
        
        elif table_id == int(read_table_id) and menu != read_menu:
            read_content = read_content.replace(read, content)
            break
        else:
            read_content += content
    
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
        
        json.append({"table_id":int(table_id), "menu":menu, "amount":quantity})
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
        
        
        json.append({"table_id":int(table_id), "call":call})
        
    return content

@app.get("/clear")
async def clear():
    
    with open("order.txt", "w") as file:
        file.write("")
        
    with open("call.txt", "w") as file:
        file.write("")
        
    return "success"