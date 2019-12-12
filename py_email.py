#!/usr/bin/python
# -*- coding: latin-1 -*-
# py_email.py = Arquivo para envio do email
# Autor: Marcos André Gerard Alves - V1.00 - 01/10/2019

# Módulo responsável por literalmente enviar o e-mail a seus
# destinatários com informações em seu corpo, coletadas no 
# banco de dados online de monitoramento.
import smtplib
import email.message
from settings import (
    get_config_company_name,

    get_config_email_from,
    get_config_email_to,
    get_config_email_cc,
    get_config_email_passwd,
    get_config_email_smtp,
    get_config_email_port
    )
from py_email_bory import get_template_bory_email_horizontal,get_template_bory_email_vertical

# Envio do e-mail
msg = email.message.Message()
msg['Subject']  = get_config_company_name()
msg['From']     = get_config_email_from()
msg['To']       = get_config_email_to()
cc = get_config_email_cc()
if cc:
    msg['Cc']       = cc
password        = get_config_email_passwd()
msg.add_header('Content-Type', 'text/html')

# Renderiza corpo do email em formato HORIZONTAL por empresa, ou seja, a empresa na linha
#msg.set_payload(get_template_bory_email_horizontal())

# Renderiza corpo do email em formato VERTICAL por empresa, ou seja, as empresas na coluna
# msg.set_payload(get_template_bory_email_vertical())

# Renderiza corpo do email em dois formatos, vertical e horinzontal por empresa
msg.set_payload(get_template_bory_email_vertical()+"\n<br>"+get_template_bory_email_horizontal())

# Este print, mostra o html com dados reais, onde podemos colocá-lo em um arquivo .html e olhar no navegador 
# seu comportamento. 
#print(get_template_bory_email_vertical())
#print(get_template_bory_email_horizontal())

s = smtplib.SMTP(get_config_email_smtp() +':'+ get_config_email_port())
s.starttls()
s.login(msg['From'], password)
if cc:
    s.sendmail(msg['From'], [msg['To'],msg['Cc']], msg.as_string())
else:    
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
