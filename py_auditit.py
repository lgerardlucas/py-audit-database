#!/usr/bin/python
# -*- coding: latin-1 -*-
# py_auditit.py = Arquivo de auditoria
# Autor: Marcos André Gerard Alves - V1.00 - 04/10/2019

# Módulo responsável por coletar informações do banco host,
# a fim de preparar e enviar os dados para o banco online, 
# que serão contextualizado no corpo do e-mail pelo 
# módulo py_email_bory.py
from py_database import (get_database_data,
    delete_database_data_online,
    insert_database_data_online
)
from settings import get_config_company_name_auditit,get_config_product_server_id,get_version,get_weekday,get_date_auditit

# GET referente as configurações - Retorna nome da empresa monitorada
COMPANY = get_config_company_name_auditit()

# Analisa se existe uma empresa
if COMPANY:
    # Deleta dados da empresa monitorada
    SQL_CLOUD_DELETE = 'Delete From monitora Where company = '+"'%s'" %(COMPANY)
    delete_database_data_online(SQL_CLOUD_DELETE)

    # ID da empresa quando se deseja ter um referencial nos dados do banco host
    ID = get_config_product_server_id()

    # Dicionário com os dados coletados com a empresa host
    QTDE_NOTAS   = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 and "ModuloOrigemNota"   in (' +"'%s'" %('TS-Compras')+','+"'%s'" %('TS-Fature')+','+"'%s'" %('TS-Pedido')+','+"'%s'" %('Inventario')+','+"'%s'" %('TS-Fiscal')+','+"'%s'" %('TS-Servico')+','+"'%s'" %('TS-Estoque')+ ')' )
    QTDE_NOTASC  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('TS-Compras'))
    QTDE_NOTASF  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('TS-Fature'))
    QTDE_NOTASP  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('TS-Pedido'))
    QTDE_NOTASI  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('Inventario'))

    QTDE_NOTAST  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('TS-Fiscal'))
    QTDE_NOTASS  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('TS-Servico'))
    QTDE_NOTASE  = get_database_data('Select Count(*) From "NotaFiscal"  Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaNota" = '+str(ID)+' end and "DataEmissaoNota"     = Current_Date-1 And "ModuloOrigemNota"    = '+"'%s'" %('TS-Estoque'))


    QTDE_PARCELAQ= get_database_data('Select Count(*) From "Parcela"     Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaParcela" = '+str(ID)+' end and "DataOperacaoParcela" = Current_Date-1 And "TipoOperacaoParcela" = '+"'%s'" %('Q'))
    QTDE_PARCELAC= get_database_data('Select Count(*) From "Parcela"     Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaParcela" = '+str(ID)+' end and "DataOperacaoParcela" = Current_Date-1 And "TipoOperacaoParcela" = '+"'%s'" %('C'))
    QTDE_PARCELAE= get_database_data('Select Count(*) From "Parcela"     Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaParcela" = '+str(ID)+' end and "DataEmissaoParcela"  = Current_Date-1 And "TipoOperacaoParcela" = '+"'%s'" %('E'))

    QTDE_PESSOAS = get_database_data('Select Count(*) From "PessoaGeral" Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaIdentificador" = '+str(ID)+' end and "DataCadastramentoPessoa"  = Current_Date-1')
    QTDE_PRODUTOS= get_database_data('Select Count(*) From "Produto"     Where Case When '+str(ID)+' = 0 then true else "CodigoEmpresaIdentificador" = '+str(ID)+' end and "DataCadastramentoProduto" = Current_Date-1')

    # Retorna o dia -1 para aditoria
    DATA_AUDITIT = get_date_auditit()
   
    # Retorna o dia da semana da auditoria
    DIA_AUDITIT = get_weekday()
    
    SQL_CLOUD_INSERT_DICT = (
        {"company":""+COMPANY+"", "key":"Auditoria(TI)",            "value": ""+str(DATA_AUDITIT)+"",   "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Compras)",    "value": ""+str(QTDE_NOTASC)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Estoque)",    "value": ""+str(QTDE_NOTASE)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Fature)",     "value": ""+str(QTDE_NOTASF)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Fiscal)",     "value": ""+str(QTDE_NOTAST)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Inventário)", "value": ""+str(QTDE_NOTASI)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Pedido)",     "value": ""+str(QTDE_NOTASP)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Serviço)",    "value": ""+str(QTDE_NOTASS)+"",    "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Qtde Notas\n(Total)",      "value": ""+str(QTDE_NOTAS)+"",     "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Parcelas\n(Abertas)",      "value": ""+str(QTDE_PARCELAE)+"",  "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Parcelas\n(Canceladas)",   "value": ""+str(QTDE_PARCELAC)+"",  "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Parcelas\n(Quitadas)",     "value": ""+str(QTDE_PARCELAQ)+"",  "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Pessoas\n(Geral)",         "value": ""+str(QTDE_PESSOAS)+"",   "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Produtos\n(Geral)",        "value": ""+str(QTDE_PRODUTOS)+"",  "date":""+str(DATA_AUDITIT)+"" },
        {"company":""+COMPANY+"", "key":"Versão",                   "value": ""+get_version()+"",       "date":""+str(DATA_AUDITIT)+"" }
    )
    insert_database_data_online(SQL_CLOUD_INSERT_DICT)