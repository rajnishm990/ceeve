import os 
import uuid
from typing import Tuple 
from pathlib import Path 
import bleach 
from app.core.config import settings


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + ["p", "div", "span", "br", "h1", "h2", "h3", "ul", "li", "ol", "strong", "em"]
ALLOWED_ATTRIBUTES = {"*": ["style", "class"]}

def save_uploaded_file(file_obj , filename:str) -> str :
    """
    Save a Starlette UploadFile-like object to local uploads dir.
    Returns the local path string.
    """
    unique = f"{uuid.uuid4().hex}_{filename}"
    dest = UPLOAD_DIR / unique
    with dest.open("wb") as f:
        f.write(file_obj.file.read())
    return str(dest.resolve())

def sanitize_html(html: str) -> str:
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)