from pathlib import Path

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.core.config import security_settings

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET_KEY)

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def generate_url_safe_token(data: dict) -> str | None:
    return _serializer.dumps(data)

def decode_url_safe_token(token: str, max_age: int = 3600) -> dict:
    try:
        data = _serializer.loads(token, max_age=max_age)
        return data
    except BadSignature, SignatureExpired:
        raise ValueError("Invalid or expired token")
