import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

data = pd.read_csv('data/KIPRIS 전체.csv')
data = data.drop(columns=['법적상태'])
ipc = pd.read_excel('data/IPC 분류표.xlsx')
ipc_info_df = pd.read_excel('data/IPC코드설명표.xlsx')

st.title("국내")

choice = st.selectbox('기업', ('한화에어로스페이스','한화시스템','현대트랜시스','현대로템','현대위아', 
                                    '현대인프라코어','KAI', 'LIG넥스원', '풍산', 'STX엔진','SK오션플랜트'))

tab1, tab2, tab3  = st.tabs(["기업분석","특허기술 분석","연도별 조회"])

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

def make_pie_chart():
        kipris = data[data['출원인'] == choice]
        kipris2 = kipris.drop(columns='Unnamed: 0')
        options = np.insert(kipris2['기술분류'].unique(), 0, '전체')
        tech = st.selectbox('기술 분야 선택', options, key=f'{choice}_tech_selectbox')
        st.divider()

        if tech != '전체':
            st.header(f'{choice} 특허 기술 - {tech}')
            st.divider()
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
            st.divider()
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

with tab2:   
        if choice == '한화에어로스페이스':
            make_pie_chart()    

        if choice == '한화시스템':
            make_pie_chart()

        if choice == '현대트랜시스':
            make_pie_chart()

        if choice == '현대로템':
            make_pie_chart()

        if choice == '현대위아':
            make_pie_chart()

        if choice == '현대인프라코어':
            make_pie_chart()

        if choice == 'KAI':
            make_pie_chart()

        if choice == 'LIG넥스원':
            make_pie_chart()

        if choice == '풍산':
            make_pie_chart()

        if choice == 'SK오션플랜트':
            make_pie_chart()

        if choice == 'STX엔진':
            make_pie_chart()