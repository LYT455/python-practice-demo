from fastapi import FastAPI

app = FastAPI(title="第一个FastAPI接口")

@app.get("/")
def hello():
    return {"msg":"hello fastapi","status":200}

# 新增用户接口
@app.get("/user/{name}")
def get_user(name:str):
    return {"username":name,"info":"测试动态路径参数"}
