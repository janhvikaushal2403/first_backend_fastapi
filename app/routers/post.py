from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2


router = APIRouter(
     prefix = "/posts",
     tags= ['Posts']
)

@router.get("/", response_model= List[schemas.PostOut])
def get_allposts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
                 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # getting data from db
    # cursor.execute("""SELECT * FROM posts""")
    # my_posts = cursor.fetchall()

    # for getting particular id posts 
    # my_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # from sqlalchemy 
    
    # my_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
    post_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,isouter= True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    my_posts = [
        {
            **post.__dict__,
            "votes": votes,
            "owner": post.owner  # Assuming `owner` is a relationship attribute of `Post`
            #      "owner" : {
            #     "id": user.id,
            #     "name": user.name,
            #     "email": user.email,
            # },  
        }
        for post, votes in post_votes
    ]
    return my_posts


# this will give status 201 not 200
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
               
    # for extracting separate field
    # print(new_post)
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    # print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
   
#    to retrieve single post 
@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id:int , response : Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # for getting id only
    # print(id)
    #   return {"post detail" : f"here is post {id}"}
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = find_post(id)

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post_vote_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(
              models.Post.id == id).group_by(models.Post.id).first()
                        

    if not post_vote_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    post, votes = post_vote_query

    # Assuming models.Post has a relationship to models.User and you want to include owner details in the response
    owner = db.query(models.User).filter(models.User.id == post.owner_id).first()

    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Owner with id: {post.owner_id} was not found")

    posts = post.__dict__
    posts.update({
        "votes": votes,
        "owner": {
            "id": owner.id,
            "email": owner.email,
            "created_at": owner.created_at
        }
    })

    return posts
#     post = [
#             {
#                 **post.__dict__,
#                 "owner" : {
#                     "id": user.id,
#                     "name": user.name,
#                     "email": user.email,
#                 },
#                 "votes" : votes
#             }
            
            
#             for post, votes, user in posts_vote_query
#         ]
#     if not post:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # # to avoid getting null
#         # return {"message" : f"post with id: {id} was not found"}
# # to avoid the hardcoding in the abobe lines use http exception
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")

#     return post

# delete post 
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} doesn't exist")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorized to perform action")
    # my_posts.pop(index)
    # return {"message" : "Post was successfully deleted"}    this will give error if u delete the sm post more than once 
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

# updating post 
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user) ):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s,
    #                published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                            detail= f"post with id: {id} doesn't exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail= "Not authorized to perform action")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # print(post_dict)
    post_query.update(post.dict(), synchronize_session= False)
    db.commit()
    return post_query.first()




