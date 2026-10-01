from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SIGEC - UFC Campus Russas"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/ufc_iot"
    
    # config pro mqtt futuro
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_TOPIC_TELEMETRY: str = "ufc/campus_russas/+/telemetry"
    MQTT_CLIENT_ID: str = "sigec_backend"
    
    BASELINE_POWER_KW: float = 2.5
    DEFAULT_TARIFF_KWH: float = 0.85

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()