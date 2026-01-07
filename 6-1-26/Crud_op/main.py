from fastapi import FastAPI
from Crud_op.routes import router

app = FastAPI()

app.include_router(router)