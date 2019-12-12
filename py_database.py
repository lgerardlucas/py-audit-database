#!/usr/bin/python
# -*- coding: latin-1 -*-
# py_database.py = Arquivo de conexão e geração dos dados
# Autor: Marcos André Gerard Alves - V1.00 - 01/10/2019

# Módulo destinado a estabelecer comunicação com os bancos de dados,
# tanto ONLINE quanto HOST.
# Sua outra função, é executar instruções SQLs enviadas por outros módulos,
# inserindo, deletando e atualizando quando necessário 
import os
import psycopg2

from settings import (
    get_config_online_server_ip,
    get_config_online_server_db,
    get_config_online_server_port, 
    get_config_online_server_passwd,
    get_config_online_server_user,

    get_config_product_server_ip,
    get_config_product_server_db,
    get_config_product_server_port, 
    get_config_product_server_passwd,
    get_config_product_server_user,


    get_config_contingency_server_ip,
    get_config_contingency_server_db,
    get_config_contingency_server_port,
    get_config_contingency_server_passwd,
    )

# HOST = Conecta a um banco interno
con = psycopg2.connect(
    host=       get_config_product_server_ip(), 
    port=       get_config_product_server_port(), 
    database=   get_config_product_server_db(), 
    user=       get_config_product_server_user(), 
    password=   get_config_product_server_passwd()
)
cur = con.cursor()

# HOST = Executa o SQL retornando uma única tupla 
def get_database_data(sql=''):
    cur.execute(sql)
    recset = cur.fetchall()
    return "%s" %(recset[0])
    con.close()

# CLOUD = Conecta a um banco externo(cloud)
cloud = psycopg2.connect(
    host=       get_config_online_server_ip(), 
    port=       get_config_online_server_port(), 
    database=   get_config_online_server_db(), 
    user=       get_config_online_server_user(), 
    password=   get_config_online_server_passwd()
)

# CLOUD = Executa o SQL retornando mais de uma tupla
def get_database_data_online(sql=''):
    cloud_cur = cloud.cursor()
    cloud_cur.execute(sql)
    recset = cloud_cur.fetchall()
    list_data = []
    for row in recset:
        list_data.append("%s, %s, %s, %s, %s " %(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))
    return list_data
    cloud.close()

# CLOUD = Executa o SQL para deletar dados da empresa que esta sendo monitoradas
def delete_database_data_online(sql=''):
    rows_deleted = 0
    try:    
        cloud_cur = cloud.cursor()
        cloud_cur.execute(sql)
        rows_deleted = cloud_cur.rowcount    
        cloud.commit()
        cloud_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            print("Erro ao deletar os dados desta empresa! "+error)
    finally:
        if cloud_cur is not None:
            cloud_cur.close()
    return rows_deleted    

# CLOUD = Executa o SQL para inserir dados da empresa que esta sendo monitoradas
def insert_database_data_online(namedict):
    rows_insert = 0
    try:            
        cloud_cur = cloud.cursor()
        cloud_cur.executemany("""INSERT INTO monitora(company,key,value,date) VALUES (%(company)s, %(key)s, %(value)s, %(date)s)""", namedict)                    

        rows_insert = cloud_cur.rowcount    
        cloud.commit()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Erro ao inserir dados nesta empresa! ")
    finally:
        if cloud_cur is not None:
            cloud_cur.close()
    return rows_insert

