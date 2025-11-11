import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.settings import settings

from app.core.http_response import CoffeeAppHttpResponse

from app.constants.email_template import new_user_verification_code_email_tempalte, new_password_reset_code_email_template


class EmailService:
    @staticmethod
    def send_verification_email(
        to_name: str, to_email: str, verification_code: str
    ):
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD

        msg = MIMEMultipart("alternative")
        msg["From"] = smtp_username
        msg["To"] = to_email
        msg["Subject"] = "¡Verifica tu cuenta!"

        text = """¡Activa tu cuenta ahora!"""

        html = new_user_verification_code_email_tempalte(
            user_name=to_name, code=verification_code
        )

        mail = None
        try:
            first_part = MIMEText(text, "plain")
            second_part = MIMEText(html, "html")

            msg.attach(first_part)
            msg.attach(second_part)

            mail = smtplib.SMTP(smtp_server, smtp_port)
            mail.ehlo()
            mail.starttls()
            mail.login(smtp_username, smtp_password)
            mail.sendmail(smtp_username, to_email, msg.as_string())

        except Exception as e:
            print(f"Error enviando email: {e}")

        finally:
            if mail:
                try:
                    mail.quit()
                except:
                    pass

    @staticmethod
    def send_conection_code_email(
        to_name: str, to_email: str, verification_code: str
    ):
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD

        msg = MIMEMultipart("alternative")
        msg["From"] = smtp_username
        msg["To"] = to_email
        msg["Subject"] = "¡Este es tu numero de conexión!"

        text = """¡Tu numero de Conexión!"""

        html = new_user_verification_code_email_tempalte(
            user_name=to_name, code=verification_code
        )

        mail = None
        try:
            first_part = MIMEText(text, "plain")
            second_part = MIMEText(html, "html")

            msg.attach(first_part)
            msg.attach(second_part)

            mail = smtplib.SMTP(smtp_server, smtp_port)
            mail.ehlo()
            mail.starttls()
            mail.login(smtp_username, smtp_password)
            mail.sendmail(smtp_username, to_email, msg.as_string())

        except Exception as e:
            print(f"Error enviando email: {e}")

        finally:
            if mail:
                try:
                    mail.quit()
                except:
                    pass

    @staticmethod
    def send_password_reset_code_email(
        to_name: str, to_email: str, verification_code: str
    ):
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD

        msg = MIMEMultipart("alternative")
        msg["From"] = smtp_username
        msg["To"] = to_email
        msg["Subject"] = "Codigo de reestablecimiento de contraseña."

        text = """¡Activa tu cuenta ahora!"""

        html = new_password_reset_code_email_template(
            user_name=to_name, code=verification_code
        )

        mail = None
        try:
            first_part = MIMEText(text, "plain")
            second_part = MIMEText(html, "html")

            msg.attach(first_part)
            msg.attach(second_part)

            mail = smtplib.SMTP(smtp_server, smtp_port)
            mail.ehlo()
            mail.starttls()
            mail.login(smtp_username, smtp_password)
            mail.sendmail(smtp_username, to_email, msg.as_string())

        except Exception as e:
            print(f"Error enviando email: {e}")

        finally:
            if mail:
                try:
                    mail.quit()
                except:
                    pass


