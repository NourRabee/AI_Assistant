from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.config import settings
from repositories.user_repo import UserRepository

# SMTP Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

templates_env = Environment(loader=FileSystemLoader("templates"))


class EmailService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    async def send_reset_email(self, email: EmailStr, token: str):
        template = templates_env.get_template("reset_password_token.html")
        user = self.user_repo.get_by_email(email)
        html_content = template.render(user_name=user.full_name ,token=token)

        message = MessageSchema(
            subject="Password Reset Request",
            recipients=[email],
            body=html_content,
            subtype="html"
        )

        fm = FastMail(conf)
        print("Preparing to send email...")
        await fm.send_message(message)
        print("Email send call completed.")

