from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def get_post(id: int):
    for post in My_post:
        if post['id'] == id:
            return post

def find_index_post(id):
    for i,p in enumerate(My_post):
        if p['id'] == id:
            return i


My_post = [
    {
        "id": 1,
        "title": "First title",
        "content": "First content"
    },
    {
        "id": 2,
        "title": "Second title",
        "content": "Second Content"
    }
]
@app.get("/")
def hello():
    return {"Message": My_post}

m 
@app.post("/createPost")
def create_post(post: Post):
    post_dict = post.dict()  
    post_dict['id'] = randrange(0, 100000)  
    My_post.append(post_dict) 
    return {"Message": post_dict} 


@app.get("/getpost/{id}")
def get_post_by_id(id: int):
    post = get_post(id) 
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} is not found"
        )
    return {"Message": post}

@app.delete("/postdelete/{id}")
def post_delete_by_id(id: int):
    index = find_index_post(id) 
    if index is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} is not found"
        )
    My_post.pop(index) 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/updatepost/{id}")
def update_post(id: int, updated_post: Post):
    post_index = find_index_post(id)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} is not found"
        )
    updated_post_dict = updated_post.dict()
    My_post[post_index].update(updated_post_dict)
    
    return {"Message": "Post {id} updated successfully", "Updated Post": My_post[post_index]}



