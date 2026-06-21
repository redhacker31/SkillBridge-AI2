import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.config import settings

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Saves an UploadFile to a local path."""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def upload_resume(db: Session, user_id: int, file: UploadFile) -> Resume:
    """
    Validates, saves the file to disk, and stores metadata in the database.
    """
    # 1. Validation
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # Note: FastAPI UploadFile size validation is better done before reading the whole file,
    # but we can check it after reading or relying on Nginx/reverse proxy in prod.
    # We will assume client-side limits are respected, and add basic server-side later if needed.

    # 2. Setup storage path
    uploads_dir = Path(settings.upload_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    file_ext = Path(file.filename).suffix if file.filename else ".pdf"
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = uploads_dir / unique_filename

    # 3. Save file
    save_upload_file(file, file_path)
    file_size = file_path.stat().st_size

    # Check file size limit (5MB = 5 * 1024 * 1024 bytes)
    max_size = 5 * 1024 * 1024
    if file_size > max_size:
        # cleanup
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5MB limit."
        )

    # 4. Save metadata to DB
    new_resume = Resume(
        user_id=user_id,
        filename=file.filename or "unknown.pdf",
        file_path=str(file_path),
        file_size=file_size,
        content_type=file.content_type
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume
