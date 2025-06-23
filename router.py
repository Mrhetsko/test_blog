from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal
from pydantic import BaseModel


router = APIRouter()


# Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoint Definitions ---

@router.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Endpoint for new user registration. """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = crud.create_user(db=db, user=user)
    token = crud.create_user_token(user_id=new_user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """ Endpoint for user login. """
    user = crud.get_user_by_email(db, email=form_data.email)
    # !!! SECURITY WARNING: Comparing plain text passwords !!!
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = crud.create_user_token(user_id=user.id)
    return {"access_token": token, "token_type": "bearer"}


# To simplify for now, I will pass the token in the body of the request.
# A more common way is to use an Authorization header.
class PostCreateWithToken(schemas.PostCreate):
    token: str


@router.post("/addpost")
def add_post(payload: PostCreateWithToken, db: Session = Depends(get_db)):
    """ Endpoint to add a new post. """
    user_id = crud.get_user_id_from_token(payload.token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    post = crud.create_post_for_user(db=db, text=payload.text, user_id=user_id)
    return {"postID": post.id}


class TokenPayload(BaseModel):
    token: str


@router.post("/getposts", response_model=List[schemas.Post])
def get_posts(payload: TokenPayload, db: Session = Depends(get_db)):
    """ Endpoint to get all posts for the authenticated user. """
    user_id = crud.get_user_id_from_token(payload.token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    posts = crud.get_posts_for_user(db, user_id=user_id)
    return posts


class DeletePostPayload(BaseModel):
    token: str
    postID: int


@router.post("/deletepost")
def delete_post(payload: DeletePostPayload, db: Session = Depends(get_db)):
    """ Endpoint to delete a post. """
    user_id = crud.get_user_id_from_token(payload.token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    success = crud.delete_post_by_id(db=db, post_id=payload.postID, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or you don't have permission to delete it")

    return {"status": "success", "message": "Post deleted"}