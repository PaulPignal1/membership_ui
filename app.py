import pandas as pd
import streamlit as st
import shutil
import numpy as np
import random
from st_aggrid import AgGrid, GridOptionsBuilder,GridUpdateMode,DataReturnMode

st.set_page_config(layout='wide')
st.title('Identify duplicates')
st.write('This short app aims at facilitate the work of identify duplicates in Housing Tables')

# Upload the CSV file
uploaded_file = st.file_uploader("Upload the CSV", type="csv")

#Column to display
col1=['hashed_uuid','uuid', 'name', 'network_id', 'partner_id_network','legal_id_agency', 'agency_phone_number']
col2=['hashed_uuid','compared_id','compared_uuid','compared_name', 'compared_network_id', 'compared_partner_id_network','compared_legal_id_agency', 'compared_agency_phone_number']

def func_all_duplicates():
    st.session_state.df['duplicata'] = 1

def func_no_duplicate():
    st.session_state.df['duplicata'] = 0

def create_dataframe(df_init,df_final):
    df_test=df_init[~df_init['hashed_uuid'].isin(set(df_final['hashed_uuid']))]
    uuid_select=random.choice(list(set(df_test['hashed_uuid'])))
    df_sample=df_test[df_test['hashed_uuid']==uuid_select]
    df1=df_sample[col1].drop_duplicates()
    df2=df_sample[col2]
    df2.columns=df2.columns.str.replace('compared_','')
    df_total=pd.concat([df1,df2]).reset_index(drop=True)
    df_total['duplicata']=np.nan
    return df_total

def convert_df(df):
   return df.to_csv().encode('utf-8')


if uploaded_file is not None:
	# Read the file

    with open("test_UI_membership.csv", "wb") as buffer:
        shutil.copyfileobj(uploaded_file, buffer)

    df_init = pd.read_csv("test_UI_membership.csv", sep=',', header=0)
    if 'df_final' not in st.session_state:
        st.session_state['df_final'] = pd.DataFrame(columns=['hashed_uuid', 'id','duplicata'])


    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    reload_data = False

    if 'message' not in st.session_state:
        st.session_state['message'] = 'Start'

    bootoon0 = st.button(st.session_state['message'])
    if bootoon0:
        if 'aggrid_key' not in st.session_state:
            st.session_state.aggrid_key = 0
            st.session_state.df=create_dataframe(df_init, st.session_state['df_final'])
        else:
            st.session_state.df=create_dataframe(df_init, st.session_state['df_final'])
            reload_data = True
        bootoon0 = False
        st.session_state['message'] = 'Reload'


    bootoon1 = st.button('All duplicates')
    if bootoon1:
        func_all_duplicates()
        reload_data = True

    bootoon2 = st.button('No duplicate')
    if bootoon2:
        func_no_duplicate()
        reload_data = True


    if 'df' and 'aggrid_key' in st.session_state:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
        gb.configure_column(field='duplicata',editable=True)
        gb.configure_grid_options(stopEditingWhenCellsLoseFocus=True,headerHeight=30,rowHeight=30)
        go = gb.build()
        ag = AgGrid(
        dataframe=st.session_state.df,
        key=st.session_state.aggrid_key,
        reload_data=reload_data,
        height=180,
        gridOptions=go,
        enable_enterprise_modules=True)

    
    bootoon3 = st.button('Validate')
    if bootoon3:
        if (st.session_state.df['duplicata']!=ag['data'].iloc[:,8]).any():
            st.session_state.df['duplicata']=ag['data'].iloc[:,8]
        st.dataframe(st.session_state.df)
    
    bootoon4 = st.button('Add to final')
    if bootoon4:
        st.session_state['df_final'] = st.session_state['df_final'].append(st.session_state.df[['hashed_uuid','id','duplicata']])
        # bootoon0=False

    bootoon5 = st.download_button(
   "Press to Download",
   convert_df(st.session_state['df_final']),
   "file.csv",
   "text/csv",
   key='download-csv')


