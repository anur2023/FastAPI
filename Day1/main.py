from random import randrange
import time
from typing import Optional
from fastapi import * # type: ignore
from pydantic import *
import psycopg2 as con
from psycopg2.extras import *
from sqlalchemy import *

# from database import SessionLocal

# from .import models
from database import get_db,engine
import models
import schemas
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(bind= engine)


# class Post(BaseModel):
#     title : str
#     content : str
#     published: bool = True
#     rating: Optional[int] = None


while True:
    try:
        conn = con.connect(host ="localhost",database = "fastapi",user="postgres",password="harsh")
        cursor = conn.cursor()
        print("Database connection was successfull...")
        break

    except Exception as error:
        print("Connection to database is failed..")
        print("Error",error)
        time.sleep(2)



@app.get('/')

def root():
    return {"message" : f"{my_data}"}

my_data = [{"title":"Title of post 1","content":"Content of post 1","id":1},
           {"title":"Title of post 2","content":"Content of post 2","id":2},
           {"title":"Title of post 3","content":"Content of post 3","id":3}
          ]

def find_id(id):
    for post in my_data:
        if(post["id"] == id):
            return post

def find_index_post(id):
    for i,p in enumerate(my_data):
        if p['id'] == id:
            return i

# @app.get('/sqlalchemy')
# def test_post(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"Data":posts}



@app.post('/postreq')

def postmet():
    cursor.execute("""
        SELECT * FROM posts
""")
    posts = cursor.fetchall()
    
    return posts 

@app.post("/createposts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)

def create_posts(post : schemas.PostCreate,db:Session = Depends(get_db)):
    # print(post)
    # post_dist = post.dict()
    # post_dist['id'] = randrange(0,100000)
    # my_data.append(post_dist)
#     cursor.execute("""
#     INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *
# """,
#     (post.title,post.content,post.published)               
#     )

#     my_post = cursor.fetchone()
#     conn.commit()
    # my_post = models.Post(title = post.title,content = post.content,published = post.published)
    my_post = models.Post(**post.dict(exclude={'rating'}))
    db.add(my_post)
    db.commit()
    db.refresh(my_post)
    return my_post

@app.get("/posts/{id}",response_model=schemas.Post)
# # First Way
# def get_post(id:int, response:Response):
#     post = find_id(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {'Message:'f'Post with id {id} is not exist'}
#     return {"Post Details":post}

# Second Way

def get_post(id:int,db:Session = Depends(get_db)):
    # post = find_id(id)
#     cursor.execute(""" 
#     SELECT * FROM posts WHERE id = %s
# """,str(id))
#     post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'Post with id {id} not found.'
        )
    return post


# Deleting Post
# Find the index in the array that has required id

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id:int,db:Session = Depends(get_db)):
    # index = find_index_post(id)
#     cursor.execute("""
#     DELETE FROM posts WHERE id = %s RETURNING *
# """,(str(id)))
#     deleted_post = cursor.fetchone()
#     conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail= f'Post with id {id} does not exists.'  
                            )
    # my_data.pop(index)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Updating the post 

@app.put("/post/{id}")

def update_post(id:int,post:schemas.PostCreate,db:Session= Depends(get_db)):
    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post_in_db = post_query.first()
    # index = find_index_post(id)
#     cursor.execute(""" 
#         UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
# """,(post.title, post.content,post.published,str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()


    if post_in_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail = f"Post with id {id} does not exist..."
                            )
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_data[index] = post_dict
    post_query.update(post.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    return post_query.first()


@app.get("/post")
def get_post(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts