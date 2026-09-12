from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key:str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    aws_s3_bucket_name: str
  


    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings() # type: ignore

