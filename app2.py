import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder,GridUpdateMode,DataReturnMode

st.set_page_config(layout="wide")
st.title('Football goals for each player')
st.write('')

def add_goals():
    st.session_state.df['goals'] = st.session_state.df['goals'] + 1
    #st.session_state.counter += 1

if 'aggrid_key' not in st.session_state:
    st.session_state.aggrid_key = 0
    st.session_state.counter = 0
    st.session_state.df = pd.DataFrame({'players':['A', 'B', 'C', 'D'], 'goals':[20, 23, 19, 41]})

col1,col2,col3,col4 = st.columns(4)
reload_data = False

with col1:
    st.markdown('When you load the app the button works normally:')
    bootoon = st.button('Add one goal to each player')
    if bootoon:
        add_goals()
        reload_data = True
    st.markdown('Count of times button was clicked:')
    st.write(st.session_state.counter)

with col2:
    st.markdown('Input dataframe before ag-grid:')
    st.dataframe(st.session_state.df)

with col3:
    st.markdown('But if later you edit the ag-grid, the button stops working')
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    gb.configure_column(field='players',editable=False)
    gb.configure_column(field='goals',editable=True)
    gb.configure_grid_options(stopEditingWhenCellsLoseFocus=True,headerHeight=30,rowHeight=30)
    go = gb.build()
    ag = AgGrid(
        dataframe=st.session_state.df,
        key=st.session_state.aggrid_key,
        reload_data=reload_data,
        height=180,
        gridOptions=go,
        enable_enterprise_modules=True)

with col4:
    st.markdown('Input dataframe after ag-grid:')
    st.dataframe(st.session_state.df)

#if (st.session_state.df['goals'] != ag['data'].iloc[:,1]).any():
 #   st.session_state.df['goals'] = ag['data'].iloc[:,1].values
  #  st.experimental_rerun()