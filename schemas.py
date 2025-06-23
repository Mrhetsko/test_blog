from pydantic import BaseModel, EmailStr, constr

# --- User Schemas ---

class UserCreate(BaseModel):
    """ Schema for creating a new user (Signup). """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """ Schema for user login. """
    email: EmailStr
    password: str


# --- Post Schemas ---

class PostBase(BaseModel):
    """ Base schema for a Post, contains the text. """
    text: constr(max_length=1024) # A simple validation

class PostCreate(PostBase):
    """ Schema for creating a new post. """
    pass

class Post(PostBase):
    """ Schema for returning a post from the API. """
    id: int
    owner_id: int

    # This tells Pydantic to read the data even if it's not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    class Config:
        orm_mode = True

# --- Token Schema ---

class Token(BaseModel):
    """ Schema for the authentication token. """
    access_token: str
    token_type: str