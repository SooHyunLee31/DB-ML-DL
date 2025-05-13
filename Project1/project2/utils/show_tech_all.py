# 전체 - 데이터프레임 조회
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
# pip install streamlit-aggrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

data = pd.read_csv('data/KIPRIS 전체.csv')
ipc = pd.read_excel('data/IPC 분류표.xlsx')
ipc_info_df = pd.read_excel('data/IPC코드설명표.xlsx')

# 연도별 그래프 만들 때 쓰는 데이터 프레임
df = data.copy()
df = df.drop(columns='Unnamed: 0')
df['출원일자'] = pd.to_datetime(df['출원일자'])
df['연도'] = df['출원일자'].dt.year.astype(int)

# 기술 분류 selectbox 옵션
tech_options = sorted(df['기술분류'].unique())
options1 = ['전체'] + tech_options

# 연도 분류 selectbox 옵션
year_options = sorted(df['연도'].unique())
options2 = ['전체'] + year_options


def show_tech(df, tech, year):
    st.subheader(f"{year}년도 기술분류: {tech}")
    if (tech == '전체') & (year == '전체'):
        st.dataframe(df.set_index('기술분류'))
    
    elif tech == '전체':
        df1 = df[df['연도'] == year]
        st.dataframe(df1.set_index('연도'))
    
    elif year == '전체':
        df1 = df[df['기술분류'] == tech]
        st.dataframe(df1.set_index('기술분류'))
    
    else:
        df1 = df[(df['기술분류'] == tech) & (df['연도'] == year)]
        st.dataframe(df1.set_index('연도'))