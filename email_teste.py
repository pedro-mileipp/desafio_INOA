import smtplib
import email.message

corpoTeste = "E-mail enviado com sucesso"
assuntoTeste = "Teste do envio de e-mail com Python"

def enviar_email(assunto, corpo):  

    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = 'pedromileipp2@gmail.com'
    msg['To'] = 'pedromileipp2@gmail.com'
    password = 'ifrmptqkvwwhddtl' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo)

    s = smtplib.SMTP('smtp-mail.outlook.com: 587')
    s.starttls()
    # Credenciais de login
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')




enviar_email(assuntoTeste, corpoTeste)
