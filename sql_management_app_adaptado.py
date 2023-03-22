#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing libraries
import pandas as pd
import sqlite3
import streamlit as st
import datetime
import os
import numpy as np


# # Setting the page configurations

# In[7]:


st.set_page_config(page_title='Gestão de registros',page_icon=r"models\favicon.png")


# # 1. Home page

# In[194]:


def home_page():
    st.markdown("# Visualizar tabelas ")
    
    bt_download_bdo = st.button('Exportar para .csv')
    
    database_path = r"C:\Python\SQL_Database_Management_Adaptado\local_database\database_adaptado.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    res = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_names = []
    for name in res.fetchall():
        tables_names.append(name[0])
    cursor.close()
    connection.close()
    
    selected_table = st.selectbox(label='Selecione a tabela:',options=tables_names)
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    df = pd.read_sql('SELECT * FROM '+ selected_table ,connection, index_col='ID_'+str(selected_table))
    cursor.close()
    connection.close()
    
    st.dataframe(data=df, height=400, width=1000)
    
    if bt_download_bdo == True:
        df.to_csv('data_export.csv')


# # 2. Insert data page

# In[195]:


def insert_data_page():
    st.markdown("# Inserir dados")
    
    database_path = r"C:\Python\SQL_Database_Management_Adaptado\local_database\database_adaptado.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    res = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_names = []
    for name in res.fetchall():
        tables_names.append(name[0])
    cursor.close()
    connection.close()
    
    selected_table = st.selectbox(label='Selecione a tabela:',options=tables_names)
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    df = pd.read_sql('SELECT * FROM '+ selected_table ,connection, index_col='ID_'+str(selected_table))
    cursor.close()
    connection.close()
    
    values = []
    
    st.subheader('Preencha os valores:')
    
    with st.form(key='form_insert_values', clear_on_submit=True):
        
        for i in range(0,len(df.columns)):
            value_input = st.text_input(label=df.columns[i], key=f"input_{i}")
            values.append(value_input)
    
        button = st.form_submit_button(label="Inserir dados!")
    
    if button == True:
        connection = sqlite3.connect(database_path, timeout=10)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO ' + selected_table + ' ' +  str(tuple(df.columns)).replace("'",'') + ' VALUES ' + str(tuple(values)).replace("'",''))
        connection.commit()
        cursor.close()
        connection.close()
        st.write("Dados inseridos com êxito!")


# # 3. Modify data page!

# In[322]:


def modify_data_page():
    st.markdown("# Alterar dados")
    
    database_path = r"C:\Python\SQL_Database_Management_Adaptado\local_database\database_adaptado.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    res = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_names = []
    for name in res.fetchall():
        tables_names.append(name[0])
    
    #Get a table name by selectbox
    selected_table = st.selectbox(label='Selecione a tabela:',options=tables_names)
    
    #Getting dataframe
    df = pd.read_sql('SELECT * FROM '+ selected_table ,connection, index_col='ID_'+str(selected_table))
    
    label_id = ('Digite o número do ID_' + str(selected_table) + ' que deseja ALTERAR')
    
    id_value = st.text_input(label=label_id, value=1)
    
    values = []
    
    st.subheader('Modifique os valores:')
    
    with st.form(key='form_insert_values', clear_on_submit=False):
    
        for i in range(0,len(df.columns)):
            value_input = st.text_input(label=str(df.columns[i]), value=str(df.iloc[int(id_value)-1,i]), key=f"input_{i}")
            values.append(value_input)
        
        update_values = []
        for i in range(0, len(df.columns)):
            update_values.append(str(df.columns[i]) + " = " + '"' + str(values[i]) + '"')
            
        update_values = str(tuple(update_values)).replace("\'","")
        update_values = update_values.replace('(',"")
        update_values = update_values.replace(')',"")

        button = st.form_submit_button(label="Confirmar modificação")
    
    if button == True:
        cursor.execute('UPDATE ' + selected_table + " SET " + update_values + " WHERE ID_" + str(selected_table) + '=' + str(id_value))
        connection.commit()
        cursor.close()
        connection.close()
        st.write("Dados modificados com êxito!")


# # 4. Delete data page

# In[324]:


def delete_data_page():
    st.markdown("# Excluir dados")
    
    database_path = r"C:\Python\SQL_Database_Management_Adaptado\local_database\database_adaptado.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    res = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_names = []
    for name in res.fetchall():
        tables_names.append(name[0])
    
    #Get a table name by selectbox
    selected_table = st.selectbox(label='Selecione a tabela:',options=tables_names)
    
    #Getting dataframe
    df = pd.read_sql('SELECT * FROM '+ selected_table ,connection, index_col='ID_'+str(selected_table))
    
    label_id = ('Digite o número do ID_' + str(selected_table) + ' que deseja EXCLUIR:')
    
    id_value = st.text_input(label=label_id, value=0)
    
    button = st.button(label='Excluir dados')
    
    df_filtered = df.iloc[int(id_value)-1,:].copy()
    
    st.dataframe(data=df_filtered, height=400, width=1000)
    
    if button == True:
        cursor.execute('DELETE FROM ' + selected_table + ' WHERE ID_' + selected_table + '=' + str(id_value))
        connection.commit()
        cursor.close()
        connection.close()
        st.write("Dados excluídos com êxito!")


# # 5. Analytics page

# In[328]:


def analytics_page():
    st.markdown("# Análise das operações")
    
    database_path = r"C:\Python\SQL_Database_Management_Adaptado\local_database\database_adaptado.db"
    selected_table = 'OPERACOES'
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    res = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_names = []
    for name in res.fetchall():
        tables_names.append(name[0])

    #Getting dataframe
    df = pd.read_sql('SELECT * FROM '+ selected_table ,connection, index_col='ID_'+str(selected_table))
    cursor.close()
    connection.close()
    
    #Getting the most frequent SONDA
    def most_frequent(List):
        return max(set(List), key = List.count)
    ope_list = list(df['OPE_COL_2'].iloc[-100:].dropna())
    st.info('Operação mais realizada: ' + str(most_frequent(ope_list)))
    
    #Avarage duration in between operations
    st.info('Duração média das operações: ' + str(round(pd.to_numeric(df['OPE_COL_3']).mean(),2)))
    
    #Getting the most recent date item
    id_max_date = pd.to_numeric(pd.to_datetime(df['OPE_COL_1'])).idxmax()
    max_date = df['OPE_COL_1'].iloc[id_max_date]
    max_date_df = pd.DataFrame()
    n_items = df.shape[0]
    for i in range(0,n_items):
        if df['OPE_COL_1'].iloc[i] == max_date:
            max_date_df = pd.concat([max_date_df, df.iloc[i,:]])
    st.subheader("Últimas operações registradas")
    st.dataframe(data=max_date_df, height=400, width=1000)
    
    #Getting the dataframe
    #Setting dataframe date x number of rows (operations)

    operations_per_time_df = pd.DataFrame()
    operations_per_time_df['Date'] = pd.to_datetime(df['OPE_COL_1'], dayfirst=True)
    operations_per_time_df = operations_per_time_df.groupby(operations_per_time_df['Date'].dt.strftime('%B,%Y')).count()
    operations_per_time_df.rename(columns={'Date':'Count'},inplace=True)
    operations_per_time_df.reset_index(inplace=True)
    operations_per_time_df["Date"] = pd.to_datetime(operations_per_time_df["Date"])
    operations_per_time_df.sort_values(by='Date', inplace=True)
    operations_per_time_df['Date'] = operations_per_time_df['Date'].dt.strftime('%B,%Y')
    operations_per_time_df.reset_index(inplace=True)
    st.subheader("Número de operações x mês")
    st.bar_chart(data=operations_per_time_df, x='Date', y='Count', width=0.5)
    
    
    #Setting dataframe operations type x count
    operation_type_list = df['OPE_COL_4'].unique()
    operation_type_list_counts = []
    for i in operation_type_list:
        operation_type_list_counts.append(list(df['OPE_COL_4']).count(i))

    op_type_values = dict(zip(operation_type_list, operation_type_list_counts))
    
    op_type_df = pd.DataFrame.from_dict(data=op_type_values, orient='index')
    op_type_df.reset_index(inplace=True)
    op_type_df.rename(columns={'index':'Operações',0:'Número de operações'},inplace=True)
    op_type_df.sort_values(by='Número de operações',ascending=False, inplace=True)
    op_type_df.reset_index(inplace=True)
    op_type_df.drop('index', axis=1,inplace=True)
    
    st.subheader("Tipo de operação x quantidade")
    st.dataframe(data=op_type_df, height=400, width=800)
    
    #Setting dataframe time duration x month
    
    #Tempo de operação durante os meses
    operations_duration_per_month = pd.DataFrame()
    operations_duration_per_month['Date'] = pd.to_datetime(df['OPE_COL_1'], dayfirst=True)
    operations_duration_per_month['Duration'] = df['OPE_COL_3']
    operations_duration_per_month.dropna(inplace=True)
    
    #Format Date column to datetime
    operations_duration_per_month['Date'] = pd.to_datetime(operations_duration_per_month['Date'], format='%B,%Y')

    # Format Duration column to float .2
    operations_duration_per_month['Duration'] = pd.to_numeric(operations_duration_per_month['Duration'])
    operations_duration_per_month['Duration'] = operations_duration_per_month['Duration'].round(2)
    
    #Plotting the graph
    operations_duration_per_month = operations_duration_per_month.groupby(operations_duration_per_month['Date'].dt.strftime('%B,%Y')).sum()
    operations_duration_per_month.reset_index(inplace=True)
    st.subheader("Horas em operações por mês")
    st.bar_chart(data=operations_duration_per_month, x='Date', y='Duration', width=0.5)
    


# # 7. Drop & create database page

# In[ ]:


def drop_create_page():
    st.markdown("# Recriar banco de dados")
    
    

    
    
    
    


# # 6. Load BDO excel file

# In[3]:


def bdo_format_insert():
    #Loading bdo!
    
    bdo_df = pd.read_excel(uploaded_file)
    
    #Obtendo dados iniciais do bdo:

    sonda = str(bdo_df[bdo_df.columns[18]].iloc[5])
    data = str(bdo_df[bdo_df.columns[22]].iloc[3])
    data = data[:10]
    
    #Setting parameters
    t_name = 'OPERACOES'
    
    connection = sqlite3.connect(database_path, timeout=10)
    cursor = connection.execute('SELECT * FROM '+ t_name)
    table_columns = []
    for i in range(0,len(cursor.description)):
        c = cursor.description[i][0]
        table_columns.append(c)
    csr = connection.cursor()
    csr.close()
    connection.close()
    
    #bdo_columns - dá para melhorar se padronizar o nome das colunas e deixar igual às colunas de banco de dados
    #não iria precisar procurar pelo index das colunas se as colunas da planilha de bdo fossem deferentes e padronizadas
    #Por exemplo: a coluna INÍCIO se repete varias vezes dentro do bdo, fica dificil encontrar os dados do INÍCIO
    
    bdo_columns = ['INÍCIO','FIM','OPE','DTM','STB','TNF','OPE','DTM','STB','TNF','TEMPO','OPERAÇÃO','DESCRIÇÃO']
    
    bdo_rows = []
    
    #Find the limit of rows
    n = np.where(bdo_df == 'TOTAL')[0][0]
    
    for i in range(0,len(bdo_columns)):
            
        if i == 0:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0]) #numero da linha que inicia os itens da bdo_columns[0]
            y = list(l[1]) #numero da coluna que inicia os itens da bdo_columns[0]
            values = list(bdo_df.iloc[(x[1]+1):n-1,y[1]].dropna())
            bdo_rows.append(values)
            m = len(bdo_rows[0])
            
        if i == 1:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])        
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]].dropna())
            values = values[:m]
            bdo_rows.append(values)

        if i == 2:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 3:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 4:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 5:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 6:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[1]+1):n-1,y[1]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 7:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[1]+1):n-1,y[1]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 8:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[1]+1):n-1,y[1]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 9:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[1]+1):n-1,y[1]])
            values = values[:m]
            bdo_rows.append(values)

        if i == 10:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]].dropna())
            values = values[:m]
            bdo_rows.append(values)

        if i == 11:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]].dropna())
            values = values[:m]
            bdo_rows.append(values)

        if i == 12:
            l = np.where(bdo_df == bdo_columns[i])
            x = list(l[0])
            y = list(l[1])
            values = list(bdo_df.iloc[(x[0]+1):n-1,y[0]].dropna())
            values = values[:m]
            bdo_rows.append(values)

    #Renomeando para não repetir colunas e dar problema. Ajuste para o banco de dados!
    bdo_columns = ['INÍCIO','FIM','OPE_S','DTM_S','STB_S','TNF_S','OPE_L','DTM_L','STB_L','TNF_L','TEMPO','OPERAÇÃO','DESCRIÇÃO']
    
    #Construindo uma nova dataframe com os valores da
    bdo_zip = dict(zip(bdo_columns, bdo_rows))
    bdo_df_formated = pd.DataFrame(bdo_zip)
    
    #Creating a apropriate dataframe to insert in database
    connection = sqlite3.connect(database_path, timeout=10)
    cursor = connection.execute('SELECT * FROM '+ t_name)
    table_columns = []
    for i in range(0,len(cursor.description)):
        c = cursor.description[i][0]
        table_columns.append(c)
    csr = connection.cursor()
    csr.close()
    connection.close()

    bdo_df_to_db = pd.DataFrame(columns=table_columns)
    
    #Setting the columns that need functions values INICIO_COMPLETO, FIM_COMPLETO, DURACAO
    from datetime import datetime
    data_dt = datetime.strptime(data,'%Y-%m-%d')

    inicio_completo = []
    for i in list(bdo_df_formated['INÍCIO']):
        t = datetime.combine(data_dt, i)
        inicio_completo.append(t)

    fim_completo = []
    for i in list(bdo_df_formated['FIM']):
        t = datetime.combine(data_dt, i)
        fim_completo.append(t)

    duracao = []
    for i in range(0,len(bdo_df_formated)):
        t1 = datetime.strptime(str(bdo_df_formated['INÍCIO'][i]), "%H:%M:%S")
        t2 = datetime.strptime(str(bdo_df_formated['FIM'][i]), "%H:%M:%S")
        t3 = t2 - t1
        duracao.append(round(t3.total_seconds()/360))
        
    #Filling the bdo_df_to_db with values
    if t_name == 'OPERACOES':
        
        bdo_df_to_db['OPE_COL_1'] = list([data for i in range(0, len(bdo_df_formated.iloc[:,0]))])
        bdo_df_to_db['OPE_COL_2'] = list([sonda for i in range(0, len(bdo_df_formated.iloc[:,0]))])
        bdo_df_to_db['OPE_COL_3'] = duracao
        bdo_df_to_db['OPE_COL_4'] = inicio_completo
        bdo_df_to_db['OPE_COL_5'] = fim_completo
        bdo_df_to_db['OPE_COL_6'] = list(bdo_df_formated.iloc[:,11])
        bdo_df_to_db['OPE_COL_7'] = list(bdo_df_formated.iloc[:,12])
        bdo_df_to_db['OPE_COL_8'] = list(bdo_df_formated.iloc[:,4])
        bdo_df_to_db['OPE_COL_9'] = list(bdo_df_formated.iloc[:,5])
        bdo_df_to_db['OPE_COL_10'] = list(bdo_df_formated.iloc[:,6])
        bdo_df_to_db['OPE_COL_11'] = list(bdo_df_formated.iloc[:,7])
        bdo_df_to_db['OPE_COL_12'] = list(bdo_df_formated.iloc[:,8])
        bdo_df_to_db['OPE_COL_13'] = list(bdo_df_formated.iloc[:,9])
        bdo_df_to_db['OPE_COL_14'] = list(bdo_df_formated.iloc[:,2])
        bdo_df_to_db['OPE_COL_15'] = list(bdo_df_formated.iloc[:,3])
        bdo_df_to_db['OPE_COL_16'] = list(bdo_df_formated.iloc[:,10])
        bdo_df_to_db['OPE_COL_17'] = list(bdo_df_formated.iloc[:,0])
        bdo_df_to_db['OPE_COL_18'] = list(bdo_df_formated.iloc[:,1])
        bdo_df_to_db['OPE_COL_19'] = duracao
        bdo_df_to_db['OPE_COL_20'] = duracao
        
    #Inserting the bdo dataframe into database
    connection = sqlite3.connect(database_path, timeout=10)
    bdo_df_to_db.to_sql(t_name, connection, if_exists='append', index=False)
    csr = connection.cursor()
    csr.close()
    connection.close()
    
    st.dataframe(data=bdo_df_to_db)
    st.write("Dados carregados!")


# # Sidebar settings

# In[340]:


page_names_to_funcs = {
    "Visualizar tabelas": home_page,
    "Inserir dados": insert_data_page,
    "Modificar dados": modify_data_page,
    "Excluir dados": delete_data_page,
    "Analisar operações": analytics_page
}

#Image
st.sidebar.image(r"models\sidebar_image.png", use_column_width=True)

#Select page with selectbox
selected_page = st.sidebar.selectbox("Selecione a opção:", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

#Data info
database_path = r"C:\Python\SQL_Database_Management_Adaptado\local_database\database_adaptado.db"
connection = sqlite3.connect(database_path)
cursor = connection.cursor()
res = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables_names = []
for name in res.fetchall():
    tables_names.append(name[0])

st.sidebar.subheader('Número de registros:')

for i in tables_names:
    df = pd.read_sql('SELECT * FROM '+ str(i) ,connection, index_col='ID_'+str(i))
    st.sidebar.info(str(i) + ": " + str(df.shape[0]))

st.sidebar.subheader('Carregar dados:')

#Uploading BDO file
uploaded_file = st.sidebar.file_uploader(label=" ", accept_multiple_files=False, label_visibility="collapsed")

bdo_button = st.sidebar.button(label='Inserir dados!', key='bdo_button')

#Format and insert bdo
if bdo_button == True:
    bdo_df=pd.read_excel(uploaded_file)
    bdo_format_insert()
    st.sidebar.write("Dados carregados!")

