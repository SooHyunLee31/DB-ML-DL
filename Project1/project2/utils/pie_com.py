# 기업별 - 파이 차트 그리기
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

data = pd.read_csv('data/KIPRIS 전체.csv')
ipc = pd.read_excel('data/IPC 분류표.xlsx')
ipc_info_df = pd.read_excel('data/IPC코드설명표.xlsx')

def make_info_fig(top_ipc, ipc_info_df):
    # 설명 붙이기: 외부 설명 데이터프레임과 merge
    top_ipc = pd.merge(top_ipc, ipc_info_df, on='IPC', how='left')
    # 파이차트 생성
    fig = px.pie(
        top_ipc,
        names='IPC',
        values='빈도수',
        title='상위 10개 기술분류 비율',
        custom_data=['설명']
    )
    # 마우스 오버 시 외부 설명 텍스트 출력
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>%{customdata[0]}<br><extra></extra>'
    )
    return fig

def make_pie_chart(data, choice):
        kipris = data[data['출원인'] == choice]
        kipris2 = kipris.drop(columns='Unnamed: 0')
        options = np.insert(kipris2['기술분류'].unique(), 0, '전체')
        tech = st.selectbox('기술 분야 선택', options, key=f'{choice}_tech_selectbox')
        st.divider()

        if tech != '전체':
            st.header(f'{choice} 특허 기술 - {tech}')
            st.header('기술 분야 별 요약')

            col1, col2 = st.columns([3.5, 2.5], gap='medium', vertical_alignment= 'center')
            # 선택한 기술분야만 출력
            kipris_tech = kipris2[kipris2['기술분류'] == tech]
            # 기술분야 빈도수 측정
            ipc_counts = kipris_tech[kipris_tech['출원인'] == choice]['IPC분류'].value_counts().reset_index()
            ipc_counts.columns = ['IPC', '빈도수']
            top_ipc = ipc_counts.head(10)

            with col1:
                # IPC 분류 상위 10개 시각화
                fig = make_info_fig(top_ipc, ipc_info_df)
                st.plotly_chart(fig)

            with col2:
                filter_df = ipc_info_df[ipc_info_df['IPC'].isin(top_ipc['IPC'])]
                filter_df = filter_df.drop(columns='Unnamed: 0').set_index('IPC')
                st.dataframe(filter_df)

            st.divider()
            st.dataframe(kipris2[kipris2['기술분류'] == tech].set_index('기술분류'))
        
        else:
            st.header(f'{choice} 특허 기술 - {tech}')
            kipris_tech = kipris2.set_index('기술분류')
            ipc_counts = kipris_tech[kipris_tech['출원인'] == choice]['IPC분류'].value_counts().reset_index()
            ipc_counts.columns = ['IPC', '빈도수']
            top_ipc = ipc_counts.head(10)        
            
            col1, col2 = st.columns([2.5, 3.5], gap='medium', vertical_alignment= 'center')

            with col1:
                st.header('기술 분야 별 요약')
                fig = make_info_fig(top_ipc, ipc_info_df)
                st.plotly_chart(fig)

            with col2:
                filter_df = ipc_info_df[ipc_info_df['IPC'].isin(top_ipc['IPC'])]
                filter_df = filter_df.drop(columns='Unnamed: 0').set_index('IPC')
                st.dataframe(filter_df)

            st.divider()
            st.dataframe(kipris_tech)