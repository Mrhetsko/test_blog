from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """
    SQLAlchemy model for the User.
    This represents the 'users' table in the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) # In a real app, this should be a hashed password

    # This creates a relationship between User and Post
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    """
    SQLAlchemy model for a Post.
    This represents the 'posts' table in the database.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1024), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # This creates a relationship back to the User
    owner = relationship("User", back_populates="posts")