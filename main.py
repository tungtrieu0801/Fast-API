from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


my_post = [{"id": 1, "title": "title 1", "content": "content1"},{"id": 2, "title": "title 2", "content": "content2"} ]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/posts")
async def root():
    return {"data": my_post}


# @app.get("/posts/lastest")
# def get_lastest_post():
#     post = my_post[len(my_post)-1]
#     return {"data": post}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict ['id']= randrange(0,10000000000)
    my_post.append(post_dict)
    return {"data": post_dict}



@app.get("/posts/{id}")
def get_one_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return{"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exsit")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exsit")
    print(post)
    post_dict = post.dict()
    post_dict ['id'] = id
    my_post[index] = post_dict
    return {"data": post_dict}
