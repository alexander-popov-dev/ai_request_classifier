from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment and .env file."""

    model_config = SettingsConfigDict(env_file=".env")

    gemini_api_key: str
    gemini_model: str = "gemini-3.1-flash-lite"
    input_file: str = "input/input_requests.csv"
    output_file: str = "output/output.json"
    report_file: str = "output/report.md"
    request_delay: float = 4.0