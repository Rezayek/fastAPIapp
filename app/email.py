from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from . import schemas
from . import models
from . import oauth2
from . import config


conf = ConnectionConfig(
    MAIL_USERNAME = config.settings.mail,
    MAIL_PASSWORD = config.settings.mail_password,
    MAIL_FROM = config.settings.mail,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(email: schemas.EmailSchema, instance: models.User): 
    token_data = {
        "user_id": instance.id,
        "username": instance.user_name
    }
    
    token = oauth2.create_access_token (token_data)
    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
            
            </head>
            <body>

                <div style = "display: flex; align-items: center; justify-content: center; flex-direction: column">

                    <h3>
                        Account verification
                    </h3>
                    <br>
                    <p> please verifie your account by clicking on the button below </p>
                    <a style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; font_size: 1rem; text-decoration: none; background: #0275d8; color: white;" href="http://localhost:8000/verification/?token{token}">
                    Verify account
                    </a>
                </div>
                <p>
                please ignore this email if you did not regiter in our service 
                </p>
                <br>
                <p>
                this link will expire in 60 minutes 
                </p>
            </body>
        </html>
    """
    
    message = MessageSchema(
        subject= "Account Verification Email",
        recipients= email, 
        body= template,
        subtype= "html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message= message)