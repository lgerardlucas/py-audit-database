#!/usr/bin/python
# -*- coding: latin-1 -*-
# py_email_bory.py = Renderiza e contextualiza corpo do e-mail
# Autor: Marcos André Gerard Alves - V1.00- 01/10/2019

# Módulo responsável por renderizar e contextualizar um conjunto de 
# TAGs HTMLs no corpo do e-mail.
# Este módulo é consumido pelo arquivo py_email.py
import os
from settings import (
    get_config_company_name,
    get_config_company_copyright,
    get_config_company_home,
    get_date_auditit,
    get_weekday
    )
from datetime import datetime
from py_database import get_database_data_online

# Date time atual    
today = datetime.now()

def alert_cell_diff(**kwargs):
    """ Função que testará um determinado parâmetro, neste caso uma data
    e se esta data vinda do banco online estiver em desacordo com 
    a data atual, a célula muda de cor alertando.
    """
    # Testando a chave e somente nesta chave testar
    if kwargs.get('key_data') == 'Auditoria(TI)':

        # Recuperando a data do dia
        DATE_NOW = get_date_auditit()
    
        # TAG HTML de alerta 
        tag_html = '<td style="color:white; font-size: 16px; text-align: right; background-color: rgb(139, 0, 0);">'

        # Testando a data do dados x data do dia
        if kwargs.get('date_data')[:10] == str(DATE_NOW):
            return kwargs.get('tag_html_atual')    
        else:    
            return tag_html
    else:
        return kwargs.get('tag_html_atual')    

# -------- CORPO DO EMAIL COM AS EMPRESAS NA HORIZONTAL ----------
def get_template_bory_email_horizontal():
    bory_horizontal =  """
    <!DOCTYPE html>
    <html>

    <head>
        <style>
            body {
                margin: 0;
                padding: 50px;
            }

            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                padding: 10px 15px;
                width: 100%;

            }

            td,
            th {
                border: 1px solid #dddddd;
                padding: 6px 6px 6px 0px;
                background-color: rgb(169, 169, 169);
                font-weight: bold;
            }

            /*@media screen and (min-width: 600px) {
                table{
                        width: 50% !important; 
                        height:auto !important;
                        min-width: 200px !important;  
                }
            }*/
    
        </style>
    </head>

    <body>
        <a href="http://www.trabin.com.br/">
            <img src="https://res.cloudinary.com/quotation-now/image/upload/v1570189494/trabin/TrabinLogo_edovf4.gif" alt="HTML tutorial" style="width:auto;height:auto;border:0;">
        </a>

        <h2>"""+get_date_auditit().strftime("%d/%m/%Y")+""" - """+get_weekday()+"""<br>"""+get_config_company_name()+"""
        </h2>

    <!--Tabela com as informações de monitoramento-->
        <table width=100%;> 
            <tr>

    """ 

    break_company = ''
    # Add primeira célula superior esquerda em branco
    bory_horizontal = bory_horizontal + '<th style="font-size: 16px; text-align: center;"><b>Empresas(TI)</b></th>'

    # GET online dos dados de monitoramento
    db_monitor    = get_database_data_online('Select * From monitora order by company,key') 

    # Loop para montar o cabeçalho da tabela

    # Conta as colunas para expandir via tag=colspan a última célula destinada ao footer
    count_col = 1
    # Conta as empresas para impressão no footer
    count_col_company = 0
    for item in db_monitor:
        count_col = count_col + 1
        # split, transforma um string separada por vígula em uma lista
        # sptrip, retira os espaços em branco de ambos os lados
        s = item.split(',')
        company     = s[1].strip() 

        # Demais células referente aos títulos das colunas com os nomes das empresas
        if not break_company:
            bory_horizontal = bory_horizontal + '<td style="font-size: 16px; text-align: center;"><b>'+company+'</b></td>'
            count_col_company = count_col_company + 1
        elif break_company != company:
                bory_horizontal = bory_horizontal + '<td style="font-size: 16px; text-align: center;"><b>'+company+'</b></td>'
                count_col_company = count_col_company + 1
        break_company = company

    # GET online dos dados de monitoramento
    db_monitor      = get_database_data_online('Select * From monitora order by key,company') 
    
 
    bory_horizontal = bory_horizontal + '</tr>'
    bory_horizontal = bory_horizontal + '<tr>'

    # Loop para montar o corpo da tabela
    color_step_key      = 2
    color_step_value    = 2
    break_info = ''
    for item in db_monitor:
        s = item.split(',')
        key         = s[2].strip()
        value       = s[3].strip()
        date        = s[4].strip()
        if not break_info:
            bory_horizontal = bory_horizontal + '<td style="font-size: 16px; text-align: center; background-color: rgb(128, 128, 128);">'+key+'</td>'
        elif break_info != key: 
            bory_horizontal = bory_horizontal + '</tr>'
            bory_horizontal = bory_horizontal + '<tr>'
            if color_step_key == 1:
                bory_horizontal = bory_horizontal + '<td style="font-size: 16px; text-align: center; background-color: rgb(128, 128, 128);">'+key+'</td>'
                color_step_key = 2
                color_step_value = 2
            else:   
                bory_horizontal = bory_horizontal + '<td style="font-size: 16px; text-align: center; background-color: rgb(169, 169, 169);">'+key+'</td>'            
                color_step_key = 1
                color_step_value = 1
        break_info = key

        if color_step_value == 1:
            bory_horizontal = bory_horizontal + str(alert_cell_diff(origin='get_horizontal',tag_html_atual='<td style="font-size: 16px; text-align: right; background-color: rgb(169, 169, 169);">',date_data=value,key_data=key)) + value + '</td>'
        else:
            bory_horizontal = bory_horizontal + str(alert_cell_diff(origin='get_horizontal',tag_html_atual='<td style="font-size: 16px; text-align: right; background-color: rgb(128, 128, 128);">',date_data=value,key_data=key)) + value + '</td>'

    bory_horizontal = bory_horizontal + """

    </tr>
        <tr style="text-align: center;">
        <td colspan="""+str(count_col)+""" style="background-color: rgb(169, 169, 169);">
            <small>
                <div style="font-size: 18px;">Total de """+str(count_col_company)+""" Empresas 
                </div>
            </small>
        </td>
    </tr>      

    </tr>
        <tr style="text-align: center;">
        <td colspan="""+str(count_col)+""" style="background-color: rgb(128, 128, 128);">
            <small>
                <div>© 2019 Copyright:
                    <a href="""+get_config_company_home()+""" style="color: rgb(46, 45, 45)">
                        """+get_config_company_copyright()+"""
                    </a>
                </div>

                <div>Tecnologias:
                    <a href="https://www.python.org/" style="color: rgb(46, 45, 45)">
                        Language Python -
                    </a>
                
                    <a href="https://www.elephantsql.com" style="color: rgb(46, 45, 45)">
                        PostgreSQL-ElephantSQL(AWS) - 
                    </a>

                    <a href="https://cloudinary.com/" style="color: rgb(46, 45, 45)">
                        Cloudnay-Picture Platform(CLOUD) - 
                    </a>
                    
                </div>
            </small>
        </td>
    </tr>      


    </table>

    </body>

    </html>
    """
    return bory_horizontal

# -------- CORPO DO EMAIL COM AS EMPRESAS NA VERTICAL ----------
def get_template_bory_email_vertical():
    bory_vertical =  """
    <!DOCTYPE html>
    <html>

    <head>
        <style>
            body {
                margin: 0;
                padding: 50px;
            }

            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                padding: 8px 10px;
                width: 100%;

            }

            td,
            th {
                border: 1px solid #dddddd;
                padding: 6px 6px 6px 0px;
                background-color: rgb(169, 169, 169);
                width:auto !important;
                font-weight: bold;
            }

            @media screen and (min-width: 600px) {
                table{
                        width: 50% !important; 
                        height:auto !important;
                        min-width: 200px !important;  
                }
            }
    
        </style>
    </head>

    <body>
        <a href="http://www.trabin.com.br/">
            <img src="https://res.cloudinary.com/quotation-now/image/upload/v1570189494/trabin/TrabinLogo_edovf4.gif" alt="" style="width:auto;height:auto;border:0;">
        </a>

        <h2>"""+get_date_auditit().strftime("%d/%m/%Y")+""" - """+get_weekday()+"""<br>"""+get_config_company_name()+"""

        </h3>

    <!--Tabela com as informações de monitoramento-->
        <table> 
            <tr>

    """

    # Add primeira célula superior esquerda em branco
    bory_vertical = bory_vertical + '<th style="font-size: 16px; text-align: center;"><b>Empresas(TI)</b></th>'

    # GET online dos dados de monitoramento
    db_monitor    = get_database_data_online('Select * From monitora order by key,company') 

    # Loop para montar o cabeçalho da tabela
    break_key = ''
    # Conta as colunas para expandir via tag=colspan a última célula destinada ao footer
    count_col = 1
    for item in db_monitor:
        count_col = count_col + 1
        # split, transforma um string separada por vígula em uma lista
        # sptrip, retira os espaços em branco de ambos os lados
        s = item.split(',')
        key  = s[2].strip() 

        # Demais células referente aos títulos das colunas com os nomes das chaves(key)
        if not break_key:
            bory_vertical = bory_vertical + '<td style="font-size: 16px; text-align: center;"><b>'+key+'</b></td>'
        elif break_key != key:
                bory_vertical = bory_vertical + '<td style="font-size: 16px; text-align: center;"><b>'+key+'</b></td>'
        break_key = key

    # GET online dos dados de monitoramento
    db_monitor    = get_database_data_online('Select * From monitora order by company,key') 

    bory_vertical = bory_vertical + '</tr>'
    bory_vertical = bory_vertical + '<tr>'

    # Loop para montar o corpo da tabela
    count_col_company   = 0
    color_step_company  = 2
    color_step_value    = 2
    break_info = ''
    for item in db_monitor:
        s = item.split(',')
        company     = s[1].strip()
        key         = s[2].strip() 
        value       = s[3].strip()
        date        = s[4].strip()
        if not break_info:
            bory_vertical = bory_vertical + '<td style="font-size: 16px; background-color: rgb(128, 128, 128);">'+company+'</td>'
            count_col_company = count_col_company + 1
        elif break_info != company: 
            bory_vertical = bory_vertical + '</tr>'
            bory_vertical = bory_vertical + '<tr>'
            if color_step_company == 1:
                bory_vertical = bory_vertical + '<td style="font-size: 16px; background-color: rgb(128, 128, 128);">'+company+'</td>'
                count_col_company = count_col_company + 1
                color_step_company = 2
                color_step_value = 2
            else:   
                bory_vertical = bory_vertical + '<td style="font-size: 16px; background-color: rgb(169, 169, 169);">'+company+'</td>'
                count_col_company = count_col_company + 1
                color_step_company = 1
                color_step_value = 1
        break_info = company
        if color_step_value == 1:
            bory_vertical = bory_vertical + str(alert_cell_diff(origin='get_vertical',tag_html_atual='<td style="font-size: 16px; text-align: right; background-color: rgb(169, 169, 169);">',date_data=value,key_data=key))+value+'</td>'
        else:
            bory_vertical = bory_vertical + str(alert_cell_diff(origin='get_vertical',tag_html_atual='<td style="font-size: 16px; text-align: right; background-color: rgb(128, 128, 128);">',date_data=value,key_data=key))+value+'</td>'


    bory_vertical = bory_vertical + """

    </tr>
        <tr style="text-align: center;">
        <td colspan="""+str(count_col)+""" style="background-color: rgb(169, 169, 169);">
            <small>
                <div style="font-size: 18px;">Total de """+str(count_col_company)+""" Empresas 
                </div>
            </small>
        </td>
    </tr>      

    </tr>

        <tr style="text-align: center;">
            <td colspan="""+str(count_col)+""" style="background-color: rgb(128, 128, 128);">
            <small>
                <div>© 2019 Copyright:
                    <a href="""+get_config_company_home()+""" style="color: rgb(46, 45, 45)">
                        """+get_config_company_copyright()+"""
                    </a>
                </div>

                <div>Tecnologias:
                    <a href="https://www.python.org/" style="color: rgb(46, 45, 45)">
                        Language Python -
                    </a>
                
                    <a href="https://www.elephantsql.com" style="color: rgb(46, 45, 45)">
                        PostgreSQL-ElephantSQL(AWS) - 
                    </a>

                    <a href="https://cloudinary.com/" style="color: rgb(46, 45, 45)">
                        Cloudnay-Picture Platform(CLOUD) - 
                    </a>
                    
                </div>
            </small>
            </td>
        </tr>      

    </body>

    </html>
    """
    return bory_vertical

