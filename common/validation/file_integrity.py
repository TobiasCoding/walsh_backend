# AJUSTAR ESTAS FUNCIONES CUANDO TENGA ALGUN INGESTOR YA PREPARADO PARA QUE INTERMEDIEN CON FILE_SERVICE


import hashlib
import subprocess
from pathlib import Path
import magic
import mimetypes
from config.variables.security import ALLOWED_EXTENSIONS


def sha256_matches(content: bytes, expected_hash: str) -> bool:
    return hashlib.sha256(content).hexdigest() == expected_hash


def is_allowed_extension(file_path: Path) -> bool:
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS


def is_real_mime(file_path: Path) -> bool:
    try:
        mime = magic.from_file(str(file_path), mime=True)
        expected, _ = mimetypes.guess_type(file_path.name)
        return mime == expected
    except Exception:
        return False


def is_malicious(file_path: Path) -> bool:
    try:
        result = subprocess.run(
            ["clamscan", str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )
        return "Infected files: 1" in result.stdout
    except Exception:
        return False


# FORMA DE LLAMAR AL MODULO

# from common.validation.file_integrity import is_malicious, is_allowed_extension

# if not is_allowed_extension(file_path) or is_malicious(file_path):
#     raise Exception("Archivo no permitido")
