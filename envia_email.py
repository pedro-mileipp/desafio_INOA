import smtplib
import email.message
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

corpoTeste = "E-mail enviado com sucesso"
assuntoTeste = "Teste do envio de e-mail com Python"

def enviar_email(assunto, corpo):  

    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'pedromileipp2@gmailcom'
    msg['To'] = 'pedromileipp@gmail.com'
    password = 'senha' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Credenciais de login
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

