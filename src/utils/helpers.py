import re
def validate_email(email: str) -> bool:
    return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email))
def validate_phone(phone: str) -> bool:
    digits = re.sub(r'\D','',phone)
    return 7 <= len(digits) <= 15
