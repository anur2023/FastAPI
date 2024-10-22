from random import randrange
from typing import Optional
from fastapi import *
from pydantic import BaseModel

app = FastAPI()
class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating: Optional[int] = None

def get_post(id):
    for post in my_post:
        if post['id'] == id:
            return post


def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get('/',status_code=status.HTTP_200_OK)

def root():
    return {'message':f'{my_post}'}




my_post = [{"title":"Title of post 1","content":"Content of post 1","id":1},
           {"title":"Title of post 2","content":"Content of post 2","id":2},
           {"title":"Title of post 3","content":"Content of post 3","id":3}
          ]

# Posting data in the server

@app.post('/Post')

def post_method():
    return {'message':f'{my_post}'}


@app.post('/createPost')
def create_post(post:Post):
    post_dist = post.dict()
    post_dist['id'] = randrange(0,100000)
    my_post.append(post_dist)
    return {"data":my_post}

@app.get('/getPost/{id}')

def GetPost(id:int):
    post = get_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} is not found "
        )

    return {'message':f'{post}'}


# Deleting the post

@app.delete('/deletePost/{id}')

def delete(id:int):
    index = find_index_post(id)
    

    if index == None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id {id} is not found "
        )
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


