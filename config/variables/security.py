# config/security.py

# Lista blanca de extensiones permitidas
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
    ".docx",
    ".xlsx",
    ".csv",
    ".json",
    ".html",
    ".xml",
    ".zip",
}

MAX_UPLOAD_MB = 50

ENABLE_CLAMAV = True  # puede desactivarse en entornos de desarrollo
