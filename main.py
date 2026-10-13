from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="第一个FastAPI接口")

@app.get("/")
def hello():
    return {"msg":"hello fastapi","status":200}

@app.get("/user/{name}")
def get_user(name:str):
    return {"username":name,"info":"测试动态路径参数"}

# POST请求接收JSON
class UserBody(BaseModel):
    username: str
    age: int

@app.post("/add_user")
def add_user(user: UserBody):
    return {"receive_data":user.model_dump(),"tip":"成功收到post的json参数"}
