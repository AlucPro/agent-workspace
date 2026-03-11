from datetime import datetime, timezone


def generate_message_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"msg_{timestamp}"
