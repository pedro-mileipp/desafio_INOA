import smtplib
import email.message
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def enviar_email(assunto, corpo):  

    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = config['EMAIL']['Remetente']
    msg['To'] = config['EMAIL']['Destino']
    password = config['SMTP']['Senha'] 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    s = smtplib.SMTP(config['SMTP']['Porta'])
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    