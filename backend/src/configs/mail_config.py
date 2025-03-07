# # configs/mail_config.py
# from pydantic import BaseModel
# from fastapi_mail import ConnectionConfig

# # Define the configuration for FastAPI Mail
# class EmailConfig(BaseModel):
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_FROM: str
#     MAIL_PORT: int = 587
#     MAIL_SERVER: str = "smtp.gmail.com"
#     MAIL_TLS: bool = True
#     MAIL_SSL: bool = False

# # The email configuration that can be loaded dynamically
# mail_config = EmailConfig(
#     MAIL_USERNAME="ritu.kansal456@gmail.com",
#     MAIL_PASSWORD="your_email_password",
#     MAIL_FROM="ritu.kansal456@gmail.com"
# )


# mail_connection_config = ConnectionConfig(
#     MAIL_USERNAME=mail_config.MAIL_USERNAME,
#     MAIL_PASSWORD=mail_config.MAIL_PASSWORD,
#     MAIL_FROM=mail_config.MAIL_FROM,
#     MAIL_PORT=mail_config.MAIL_PORT,
#     MAIL_SERVER=mail_config.MAIL_SERVER,
#     MAIL_TLS=mail_config.MAIL_TLS,
#     MAIL_SSL=mail_config.MAIL_SSL,
# )