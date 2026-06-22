from enum import StrEnum


class CategoryType(StrEnum):
    """Supported classification categories for a request."""

    AUTOMATION = "автоматизація"
    INTEGRATION = "інтеграція"
    REPORT_ANALYTICS = "звіт-аналітика"
    BUG_SUPPORT = "баг-підтримка"
    QUESTION_CONSULTATION = "питання-консультація"
    OUT_OF_SCOPE = "поза скоупом"

class PriorityType(StrEnum):
    """Priority levels for a classified request."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
