from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="第一个FastAPI接口")

# sqlite 文件数据库，不用安装服务，直接生成db文件
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据库表模型
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)

# 请求入参模型
class UserBody(BaseModel):
    username: str
    age: int

@app.get("/")
def hello():
    return {"msg":"hello fastapi","status":200}

@app.get("/user/{name}")
def get_user(name:str):
    return {"username":name,"info":"测试动态路径参数"}

# 新增用户存入数据库
@app.post("/add_user")
def add_user(user: UserBody):
    db = SessionLocal()
    db_user = DBUser(username=user.username, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return {"id":db_user.id,"receive_data":user.model_dump(),"tip":"数据存入sqlite数据库"}

# 查询全部用户
@app.get("/list_user")
def list_user():
    db = SessionLocal()
    users = db.query(DBUser).all()
    db.close()
    return {"user_list":[{"id":u.id,"username":u.username,"age":u.age} for u in users]}
