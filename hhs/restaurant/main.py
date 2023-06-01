import fastapi
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from routes.foods import foods_router
from routes.receipts import receipts_router
from routes.orders import orders_router
from routes.stocks import stocks_router
from routes.tables import tables_router


app = fastapi.FastAPI(
    title="Restaurant API",
    description="Restaurant API for IoT Project",
)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(foods_router.router)
app.include_router(receipts_router.router)
app.include_router(orders_router.router)
app.include_router(stocks_router.router)
app.include_router(tables_router.router)

app.mount("/assets", StaticFiles(directory='frontend_restaurant/dist/assets'))

@app.get("/")
def home():
    return FileResponse('frontend_restaurant/dist/index.html')