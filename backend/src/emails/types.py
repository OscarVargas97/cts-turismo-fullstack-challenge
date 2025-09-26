from typing import TypedDict, Any, Dict, Optional


class EmailData(TypedDict):
    subject: str
    message: str
    from_email: str
    recipient_list: list[str]
    html_message: Optional[str]
