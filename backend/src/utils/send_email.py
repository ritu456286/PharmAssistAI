# from fastapi_mail import FastMail, MessageSchema
# from src.configs.mail_config import mail_config, mail_connection_config  # Import the email config
# import logging

# fm = FastMail(mail_connection_config)

# # Utility function to send emails
# async def send_email(recipient: str, subject: str, body: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[recipient],
#         body=body,
#         subtype="plain"
#     )

#     try:
#         await fm.send_message(message)
#         logging.info(f"Email sent to {recipient}")
#     except Exception as e:
#         logging.error(f"Error sending email: {e}")