from fastapi import FastAPI
from fastapi.routing import APIRouter
from utils import filter_characters

import uvicorn

VERSION= "1.1.0"

app= FastAPI(title= "ZenkApi", version= VERSION)
api_router= APIRouter()

@api_router.get("/")
async def root():

    return {"message": "Welcome to ZenkApi!"}

@api_router.get("/characters")
async def get_characters(name: str= None, contains: str= None, has_zenkai: bool= None, is_lf: bool= None, is_tag: bool= None, limit: int= None, id: str= None, color: str= None, rarity= None, tags= None):
    
    filters= {"name": name, "contains": contains, "has_zenkai": has_zenkai, "is_lf": is_lf, "is_tag": is_tag, "id": id, "color": color, "rarity": rarity, "tags": tags}

    if limit == None:

        limit= 2

    filtered_results= filter_characters(filters)

    return filtered_results[:limit]

app.include_router(api_router, prefix= "/zenkapi/v1")

if __name__ == "__main__":

    uvicorn.run(app)