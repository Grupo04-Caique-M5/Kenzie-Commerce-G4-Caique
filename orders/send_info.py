import smtplib
import email.message


def send_email(status, obj):
    products = obj.cart_products
    name = " "
    for prod in products:
        name += prod["name"] + ", "

    corpo_email = f"""
    <p>Olá, seu pedido de {name} teve uma atualização!</p>
    <p>O Status do seu pedido atualmente é: {status}</p>
    """

    msg = email.message.Message()
    msg["Subject"] = "Atualização sobre seu pedido"
    msg["From"] = "enum.commerce@gmail.com"
    msg["To"] = obj.user.email
    password = "btlyeicgfxvlffin"
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(corpo_email)

    s = smtplib.SMTP("smtp.gmail.com: 587")
    s.starttls()
    s.login(msg["From"], password)
    s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
    print("Email enviado")
