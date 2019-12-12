#!/usr/bin/python
# -*- coding: latin-1 -*-
# py_config.py = Arquivo de configuração do sistema
# Autor: Marcos André Gerard Alves - V1.00 - 01/10/2019

# Módulo responsável por retornar as configurações usado por
# todos os outros módulos vindas do arquivo "conf.ini"
# Estrutura do arquivo: CHAVE + VALOR
# O arquivo conf.ini não é tratado pelo git, sendo somente 
# versionado o arquivo base d enome conf.ini.original
import os
import codecs
import ConfigParser
from datetime import datetime,date

# Determina o ponto inicial do sistema
def get_local_host_project():
    NAME_SIS = 'py-send-email'          
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(BASE_DIR, NAME_SIS)

# Verifica a existência de qualquer arquivo dentro do projeto
# e retorna o caminho+nome se encontrado
def get_exists_file(file):
    if not os.path.isfile(get_local_host_project()+'/'+file):
        return ''
    else:
        return get_local_host_project()+'/'+file

# Estabece o caminho + nome do arquivo de configuração para leitura
#PATH_PG = os.path.abspath(os.path.join(BASE_DIR, NAME_SIS+'/conf.ini'))

# Verifica a existencia do arquivo de configuração
if get_exists_file('conf.ini') != '':
    # Lendo o arquivo de configuração do sistema
    cfg = ConfigParser.ConfigParser()
    cfg.read(get_exists_file('conf.ini'))
    # GET referente a versão da estrutura da grade de informações py_auditit.py
    def get_version():
        return 'v.1.06'

    # GET dia da semana a que pertence uma data
    def get_weekday():
        dias   = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
        return dias[get_date_auditit().weekday()]

    # GET da data -1 dia para auditoria
    def get_date_auditit():
        data_dia    = date.today()
        data_ontem  = date.fromordinal(data_dia.toordinal()-1)
        return data_ontem

    # GET referente as informações da empresea faz o monitoramento
    def get_config_company_name():
        return cfg.get('COMPANY','NAME')
    def get_config_company_copyright():
        return cfg.get('COMPANY','COPYRIGHT')
    def get_config_company_home():
        return cfg.get('COMPANY','HOME')

    # GET referente as informações da empresea que esta sendo monitorada
    def get_config_company_name_auditit():
        return cfg.get('COMPANY_AUDITIT','NAME')

    # GET referente as configurações do banco de ONLINE - ELEPHANTSQL  
    # https://customer.elephantsql.com/instance
    def get_config_online_server_ip():
        return cfg.get('ONLINE_SERVER','IP')

    def get_config_online_server_db():
        return cfg.get('ONLINE_SERVER','DB')

    def get_config_online_server_port():
        return cfg.get('ONLINE_SERVER','PORT')

    def get_config_online_server_passwd():
        return cfg.get('ONLINE_SERVER','PASSWD')

    def get_config_online_server_user():
        return cfg.get('ONLINE_SERVER','USER')

    # GET referente as configurações do banco de PRODUÇÃO
    def get_config_product_server_ip():
        return cfg.get('PRODUCT_SERVER','IP')

    def get_config_product_server_db():
        return cfg.get('PRODUCT_SERVER','DB')

    def get_config_product_server_port():
        return cfg.get('PRODUCT_SERVER','PORT')

    def get_config_product_server_passwd():
        return cfg.get('PRODUCT_SERVER','PASSWD')

    def get_config_product_server_user():
        return cfg.get('PRODUCT_SERVER','USER')

    def get_config_product_server_id():
        return cfg.get('PRODUCT_SERVER','ID')

    # GET referente as configurações do banco de CONTINGENCIA
    def get_config_contingency_server_ip():
        return cfg.get('PRODUCT_CONTINGENCY','IP')

    def get_config_contingency_server_db():
        return cfg.get('PRODUCT_CONTINGENCY','DB')

    def get_config_contingency_server_port():
        return cfg.get('PRODUCT_CONTINGENCY','PORT')

    def get_config_contingency_server_passwd():
        return cfg.get('PRODUCT_CONTINGENCY','PASSWD')

    def get_config_contingency_server_user():
        return cfg.get('PRODUCT_CONTINGENCY','USER')

    def get_config_contingency_server_id():
        return cfg.get('PRODUCT_CONTINGENCY','ID')

    # GET referente as configurações para envio de e-mail
    def get_config_email_from():
        return cfg.get('EMAIL','FROM')

    def get_config_email_to():
        return cfg.get('EMAIL','TO')

    def get_config_email_cc():
        return cfg.get('EMAIL','CC')

    def get_config_email_passwd():
        return cfg.get('EMAIL','PASSWD')

    def get_config_email_smtp():
        return cfg.get('EMAIL','SMTP')

    def get_config_email_port():
        return cfg.get('EMAIL','PORT')
        