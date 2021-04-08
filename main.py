from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI

#from .models import *
from schemas import City


# SQLAlchemy specific code, as with any other app
DATABASE_URL = "mysql://root:diatta96@localhost/sakila"

database = databases.Database(DATABASE_URL)



db = [
  {
    "name": "Dakar",
    "timezone": "Senegal/Dakar"
  },
  {
    "name": "Ziguinchor",
    "timezone": "Senegal/Ziguinchor"
  },
  {
    "name": "Thies",
    "timezone": "Senegal/Thies"
  }
]


app = FastAPI(title="Google Meet Analyzer API")

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def index():
    return await {'key': 'value'}

@app.get('/cities')
async def get_cities():
    return await db

@app.get('/cities/{city_id}')
async def get_city(city_id : int):
    return await db[city_id-1]

@app.post('/cities')
async def create_city(city: City):
    db.append(city.dict())
    return await db[-1]

@app.delete('/cities/{city_id}')
async def delete_city(city_id: int):
    db.pop(city_id-1)
    return await {}


