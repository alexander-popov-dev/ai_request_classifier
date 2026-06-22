import time
from functools import wraps
from typing import Callable, Any

from src.core.exceptions import RetryError


def retry(
        attempts: int = 3,
        exceptions: tuple[type[Exception], ...] = (Exception,)
) -> Callable[[Callable], Callable]:
    """Retry a function on specified exceptions with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error: Exception | None = None

            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_error = e
                    if attempt < attempts - 1:
                        time.sleep(2 ** attempt)

            raise RetryError(last_error)
        return wrapper
    return decorator
