from typing import TypedDict


class EmailData(TypedDict):
    subject: str
    message: str
    from_email: str
    recipient_list: list[str]
