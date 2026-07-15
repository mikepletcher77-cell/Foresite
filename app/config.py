from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Generate your own with: python -c "import secrets; print(secrets.token_hex(32))"
    jwt_secret: str = "CHANGE_ME_BEFORE_DEPLOYING"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 30  # 30 days, so people stay logged in

    # Get a free key at https://ridb.recreation.gov/ (Get API Key, top right)
    recreation_gov_api_key: str = ""

    database_url: str = ""

    email_username: str = ""
    email_password: str = ""
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 465
    email_from_address: str = ""
    cron_secret: str = ""
    class Config:
        env_file = ".env"


settings = Settings()