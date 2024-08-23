import smtplib
import email.message

def enviar_email(assunto, corpo):  

    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'pedromileipp2@gmail.com'
    msg['To'] = 'pedromileipp@gmail.com'
    password = 'senha' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')