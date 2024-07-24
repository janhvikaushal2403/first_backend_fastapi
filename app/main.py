from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# here we'll define list of url which can access our apis
# for public acess = ["*"]
origins = ["*"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        
app.include_router(post.router)  
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(vote.router) 

@app.get("/")
async def root():
    return {"message": "Hello World"}





# my_posts =[{"title":"title of post 1", "content": "content of post 1", "id": 1},
#            {"title":"favorite Food", "content": "Pizza", "id": 2}]

# for getting post from id
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p 
        
# # for getting index 
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}




