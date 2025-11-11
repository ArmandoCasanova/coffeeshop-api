def new_user_verification_code_email_tempalte(
    user_name: str,
    code: int,
) -> str:
    head = """
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifica tu correo electrónico</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2e9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }

        .container {
            background-color: #242424;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90vw;
            max-width: 400px;
            text-align: center;
            color: white;
            overflow: hidden;
            position: relative;
        }

        .header {
            background-color: #A3775A;
            padding: 20px;
            border-radius: 15px 15px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            top: -20px;
            left: -20px;
            width: calc(100% + 40px);
            text-align: left;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            color: white;
            line-height: 1.2;
            flex-grow: 1;
        }

        .logo {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-right: 5%;
        }

        .logo img {
            width: 80px;
            height: 80px;
        }

        .content {
            padding: 20px;
        }

        .content p {
            font-size: 16px;
            color: #ccc;
            margin-top: 0;
        }

        .code-box {
            background-color: #FFFDD0;
            border-radius: 30px;
            padding: 15px 30px;
            display: inline-block;
            margin: 20px 0;
        }

        .code-box span {
            font-size: 48px;
            font-weight: 700;
            color: #654321;
        }

        .footer p {
            font-size: 12px;
            color: #999;
            margin-bottom: 20px;
        }

        .social-icons {
            margin-top: 15px;
        }

        .social-icons img {
            width: 24px;
            height: 24px;
            margin: 0 10px;
        }

        @media (max-width: 480px) {
            .container {
                padding: 10px;
            }

            .header {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                top: -10px;
                left: -10px;
                width: calc(100% + 20px);
            }

            .header h1 {
                font-size: 20px;
                text-align: left;
            }

            .logo img {
                width: 60px;
                height: 60px;
            }

            .content p {
                font-size: 14px;
            }

            .code-box span {
                font-size: 36px;
            }
        }

        @media (max-width: 768px) {
            .logo img {
                width: 70px;
                height: 70px;
            }
        }
    </style>
</head>
    """

    body = f"""
        <body>
    <div class="container">
        <div class="header">
            <h1>Verifica tu<br>correo electrónico</h1>
            <div class="logo">
                <img src="cid:logo_principal" alt="CoffeeShop Logo">
            </div>
        </div>

        <div class="content">
            <p>Bienvenido a CoffeeShop! Ingresa el siguiente código en la app para verificar tu correo.</p>
            <div class="code-box">
                <span>{code}</span>
            </div>
        </div>

        <div class="footer">
            <p>Por favor, introduce tu código de activación para activar tu cuenta y comenzar a usar todas las funciones de la aplicación.</p>
            <div class="social-icons">
                <img src="cid:icono_gmail" alt="Gmail">
                <img src="cid:icono_facebook" alt="Facebook">
                <img src="cid:icono_instagram" alt="Instagram">
            </div>
        </div>
    </div>
</body>
</html>
    """

    return f"{head}{body}"


def new_password_reset_code_email_template(
    user_name: str,
    code: int,
) -> str:
    head = """
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reestablece tu contraseña</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2e9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }

        .container {
            background-color: #242424;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90vw;
            max-width: 400px;
            text-align: center;
            color: white;
            overflow: hidden;
            position: relative;
        }

        .header {
            background-color: #A3775A;
            padding: 20px;
            border-radius: 15px 15px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            top: -20px;
            left: -20px;
            width: calc(100% + 40px);
            text-align: left;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            color: white;
            line-height: 1.2;
            flex-grow: 1;
        }

        .logo {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-right: 5%;
        }

        .logo img {
            width: 80px;
            height: 80px;
        }

        .content {
            padding: 20px;
        }

        .content p {
            font-size: 16px;
            color: #ccc;
            margin-top: 0;
        }

        .code-box {
            background-color: #FFFDD0;
            border-radius: 30px;
            padding: 15px 30px;
            display: inline-block;
            margin: 20px 0;
        }

        .code-box span {
            font-size: 48px;
            font-weight: 700;
            color: #654321;
        }

        .footer p {
            font-size: 12px;
            color: #999;
            margin-bottom: 20px;
        }

        .social-icons {
            margin-top: 15px;
        }

        .social-icons img {
            width: 24px;
            height: 24px;
            margin: 0 10px;
        }

        @media (max-width: 480px) {
            .container {
                padding: 10px;
            }

            .header {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                top: -10px;
                left: -10px;
                width: calc(100% + 20px);
            }

            .header h1 {
                font-size: 20px;
                text-align: left;
            }

            .logo img {
                width: 60px;
                height: 60px;
            }

            .content p {
                font-size: 14px;
            }

            .code-box span {
                font-size: 36px;
            }
        }

        @media (max-width: 768px) {
            .logo img {
                width: 70px;
                height: 70px;
            }
        }
    </style>
</head>
    """

    body = f"""
        <body>
    <div class="container">
        <div class="header">
            <h1>Reestablece<br>tu contraseña</h1>
            <div class="logo">
                <img src="cid:logo_principal" alt="CoffeeShop Logo">
            </div>
        </div>

        <div class="content">
            <p>Bienvenido a CoffeeShop! Ingresa el siguiente código en la app para reestablecer tu contraseña.</p>
            <div class="code-box">
                <span>{code}</span>
            </div>
        </div>

        <div class="footer">
            <p>Por favor, introduce tu código de reestablecimiento para comenzar a usar todas las funciones de la aplicación.</p>
            <div class="social-icons">
                <img src="cid:icono_gmail" alt="Gmail">
                <img src="cid:icono_facebook" alt="Facebook">
                <img src="cid:icono_instagram" alt="Instagram">
            </div>
        </div>
    </div>
</body>
</html>
    """

    return f"{head}{body}"
