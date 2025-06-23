from sqlalchemy.orm import Session
import secrets # Used for generating a simple token
import models, schemas

# This is a very simple, insecure way to manage tokens for this exercise.
# In a real app, you would use JWTs and a proper user lookup.
# We'll store tokens here with their corresponding user_id.
# Format: { "token_string": user_id }
active_tokens = {}

# --- User CRUD ---

def get_user_by_email(db: Session, email: str):
    """ Fetches a user from the database by their email. """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """ Creates a new user in the database. """
    # !!! SECURITY WARNING: Storing plain text passwords !!!
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_token(user_id: int) -> str:
    """ Generates a simple, random token for a user. """
    token = secrets.token_hex(16)
    active_tokens[token] = user_id
    return token

def get_user_id_from_token(token: str) -> int | None:
    """ Finds the user ID associated with a token. """
    return active_tokens.get(token)


# --- Post CRUD ---

def create_post_for_user(db: Session, text: str, user_id: int):
    """ Creates a post in the database linked to a user. """
    db_post = models.Post(text=text, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_for_user(db: Session, user_id: int):
    """ Gets all posts from the database for a specific user. """
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()

def delete_post_by_id(db: Session, post_id: int, user_id: int):
    """ Deletes a post from the database. """
    # We also check user_id to make sure a user can only delete their own posts.
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == user_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False