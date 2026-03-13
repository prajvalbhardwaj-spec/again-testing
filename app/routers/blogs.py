from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/", response_model=schemas.BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_blog = models.Blog(**blog.model_dump(), author_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/", response_model=List[schemas.BlogOut])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).filter(models.Blog.published == True).all()


@router.get("/{blog_id}", response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=schemas.BlogOut)
def update_blog(
    blog_id: int,
    updated: schemas.BlogUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this blog"
        )

    if updated.title is not None:
        blog.title = updated.title
    if updated.content is not None:
        blog.content = updated.content
    if updated.published is not None:
        blog.published = updated.published

    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this blog"
        )

    db.delete(blog)
    db.commit()
