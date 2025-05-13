# 기업별 - 연도 막대 그래프

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

def make_info_bar(top_ipc, ipc_info_df):
        # 설명 붙이기
        top_ipc = pd.merge(top_ipc, ipc_info_df, on='IPC', how='left')
        # 바 차트 생성
        fig = px.bar(
            top_ipc,
            x='빈도수',
            y='IPC',
            title='상위 10개 기술분류',
            orientation= 'h',
            text='빈도수',
            custom_data=['설명']
        )
        # 마우스 오버 시 설명 출력
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>빈도수: %{y}<br>%{customdata[0]}<extra></extra>'
        )
        return fig

# year_show랑 같음음
def make_bar_year(data, choice, ipc_info_df):
    df1 = data[data['출원인'] == choice]
    df1 = df1.drop(columns='Unnamed: 0')
    df1['출원일자'] = pd.to_datetime(df1['출원일자'])
    df1 = df1.sort_values(by='출원일자').reset_index(drop=True)
    df1['연도'] = df1['출원일자'].dt.year
    
    year_options = df1['연도'].unique()
    options = ['전체'] + sorted(year_options)
    year = st.selectbox('연도 선택', options)
    st.divider()

    st.header(f'{choice} 특허 기술 - {year}년도')
    # df1 = df1[df1['연도'] == year].set_index('연도')
    df1['출원일자'] = df1['출원일자'].dt.date
    df1 = df1[['발명의명칭', 'IPC분류', '기술분류', '출원일자', '출원인', '요약', '연도']]

    if year != '전체':
        df2 = df1[df1['연도'] == year]
        # IPC 분류 상위 10개 시각화
        ipc_counts = df1[df1['출원인'] == choice]['IPC분류'].value_counts().reset_index()
        ipc_counts.columns = ['IPC', '빈도수']
        top_ipc = ipc_counts.head(10)
        fig = make_info_bar(top_ipc, ipc_info_df)

        col1, col2 = st.columns([2.5, 3.5], gap='medium', vertical_alignment= 'center')
        with col1:
            st.plotly_chart(fig)  
        
        with col2:
            filter_df = ipc_info_df[ipc_info_df['IPC'].isin(top_ipc['IPC'])]
            filter_df = filter_df.drop(columns='Unnamed: 0').set_index('IPC')
            st.dataframe(filter_df)
        
        st.divider()
        st.dataframe(df2.set_index('연도'))              
    else:
        ipc_counts = df1['IPC분류'].value_counts().reset_index()
        ipc_counts.columns = ['IPC', '빈도수']
        top_ipc = ipc_counts.head(10)
        fig = make_info_bar(top_ipc, ipc_info_df)

        col1, col2 = st.columns([2.5, 3.5], gap='medium', vertical_alignment= 'center')
        
        with col1:
            st.plotly_chart(fig)  
        
        with col2:
            filter_df = ipc_info_df[ipc_info_df['IPC'].isin(top_ipc['IPC'])]
            filter_df = filter_df.drop(columns='Unnamed: 0').set_index('IPC')
            st.dataframe(filter_df)
        st.divider()
        st.dataframe(df1.set_index('연도'))