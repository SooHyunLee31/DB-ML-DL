# 전체 - 기술, 연도 별 막대 그래프

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
# pip install streamlit-aggrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

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

def pie_chart(data, ipc_info_df):
        kipris = data.copy()
        
        st.write(' - IPC별 요약')
        col1, col2 = st.columns([3.5, 2.5], gap='medium', vertical_alignment= 'center')        
        ipc_counts = kipris['IPC분류'].value_counts().reset_index()
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
        
def total_sum_concat_year(data1):
    total_row = pd.DataFrame({
        '연도': ['총계'],
        '출원수': [data1['출원수'].sum()]
    })
    df = pd.concat([total_row, data1], ignore_index=True)
    return df

def total_sum_concat_tech(data1):
    total_row = pd.DataFrame({
        '기술분류': ['총계'],
        '출원수': [data1['출원수'].sum()]
    })
    df = pd.concat([total_row, data1], ignore_index=True)
    return df

def info_show(df, tech, year, ipc_info_df):
        # copy한 원본 데이터에 연도 컬럼을 추가하고 3개 컬럼만 추출
        df_f = df[['출원인','기술분류','연도']]
        st.subheader(f'기술 분야 - {tech}, 연도 - {year}')
        st.write(f' - 출원수 비교 그래프')
        
        # 기술, 연도 전체 필터링
        if (tech == '전체') & (year == '전체'):
            # 기업 별 개수 측정
            counts = df_f['출원인'].value_counts().reset_index()
            counts2 = df_f['연도'].value_counts().reset_index()
            counts3 = df_f['기술분류'].value_counts().reset_index()
            counts.columns = ['출원인', '출원수']
            counts2.columns = ['연도', '출원수']
            counts3.columns = ['기술분류', '출원수']
            a = total_sum_concat_year(counts2)
            b = total_sum_concat_tech(counts3)
            # 그래프 설계
            fig = px.bar(counts, x = '출원수', 
                        y = '출원인',
                        orientation= 'h',
                        text='출원수')
            # 구간 설정
            col1, col2 = st.columns([3.5,2.5])

            with col1:
                # 그래프 구현
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                with st.container():
                    # 빈도수 표로 구현
                    gb = GridOptionsBuilder.from_dataframe(a)
                    grid_options = gb.build()
                    AgGrid(a,
                        gridOptions=grid_options,
                        fit_columns_on_grid_load=True, # 열 너비 자동 맞춤
                        height=250,
                        theme='streamlit')
                with st.container():
                    # 빈도수 표로 구현
                    gb = GridOptionsBuilder.from_dataframe(b)
                    grid_options = gb.build()
                    AgGrid(b,
                        gridOptions=grid_options,
                        fit_columns_on_grid_load=True, # 열 너비 자동 맞춤
                        height=250,
                        theme='streamlit')
            st.divider()
            pie_chart(df, ipc_info_df)
        # 기술 전체 필터링
        elif tech == '전체':
            # 연도 필터링
            df_y = df_f[df_f['연도'] == year]
            df_y2 = df[df['연도'] == year]
            # 연도별 기업의 출원 수 측정
            counts = df_y['출원인'].value_counts().reset_index()
            counts2 = df_y['기술분류'].value_counts().reset_index()
            counts.columns = ['출원인', '출원수']
            counts2.columns = ['기술분류', '출원수']
            a = total_sum_concat_tech(counts2)
            
            # 그래프 설계
            fig = px.bar(counts, x = '출원수', 
                        y = '출원인',
                        orientation= 'h',
                        text='출원수')
            # 구간 설정
            col1, col2 = st.columns([3.5,2.5])
            with col1:
                # 그래프 구현
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # 빈도수 표로 구현
                gb = GridOptionsBuilder.from_dataframe(a)
                grid_options = gb.build()
                AgGrid(a,
                       gridOptions=grid_options,
                       fit_columns_on_grid_load=True, # 열 너비 자동 맞춤
                       theme='streamlit')
            st.divider()    
            pie_chart(df_y2, ipc_info_df)
            
        # 연도 전체 필터링
        elif year == '전체':
            # 기술 필터링
            df_t = df_f[df_f['기술분류'] == tech]
            df_t2 = df[df['기술분류'] == tech]
            # 기술별 기업의 출원 수 측정
            counts = df_t['출원인'].value_counts().reset_index()
            counts2 = df_t['연도'].value_counts().reset_index()
            counts.columns = ['출원인', '출원수']
            counts2.columns = ['연도', '출원수']
            a = total_sum_concat_year(counts2)
            
            # 그래프 설계
            fig = px.bar(counts, x = '출원수', 
                        y = '출원인',
                        orientation= 'h',
                        text='출원수')
            # 구간 설정
            col1, col2 = st.columns([3.5,2.5])
            with col1:
                # 그래프 구현
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # 빈도수 표로 구현
                gb = GridOptionsBuilder.from_dataframe(a)
                grid_options = gb.build()
                AgGrid(a,
                       gridOptions=grid_options,
                       fit_columns_on_grid_load=True, # 열 너비 자동 맞춤
                       theme='streamlit')
            st.divider()
            pie_chart(df_t2, ipc_info_df)
        # 기술, 연도 필터링
        else:
            # 기술, 연도별 필터링
            df_f2 = df_f[(df_f['기술분류'] == tech) & (df_f['연도'] == year)]
            df_f22 = df[(df['기술분류'] == tech) & (df['연도'] == year)]
            # 기술, 연도별 기업의 출원 수 측정
            counts = df_f2['출원인'].value_counts().reset_index()
            counts2 = df_f2['기술분류'].value_counts().reset_index()
            counts.columns = ['출원인', '출원수']
            counts2.columns = ['기술분류', '출원수']
            
            # 그래프 설계
            fig = px.bar(counts, x = '출원수', 
                        y = '출원인',
                        orientation= 'h',
                        text='출원수')
            
            # 구간 설정
            col1, col2 = st.columns([3.5,2.5])
            with col1:
                # 그래프 구현
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # 빈도수 표로 구현
                gb = GridOptionsBuilder.from_dataframe(counts2)
                grid_options = gb.build()
                AgGrid(counts2,
                       gridOptions=grid_options,
                       fit_columns_on_grid_load=True, # 열 너비 자동 맞춤
                       theme='streamlit')
            st.divider()
            pie_chart(df_f22, ipc_info_df)

def wordcloud_info(choice, key_list, value_list, df):
    w_dic = dict(zip(key_list, value_list))
    st.divider()
    st.subheader('INSIGHT')
    st.write(f'**{choice}**에 대한 워드 클라우드 분석을 수행한 결과, **{w_dic[choice]}**(이)가 가장 높은 출현 빈도를 보여 주요 키워드로 확인되었습니다.')
    st.divider()
    # 빈도수 계산 (데이터프레임으로 변환)
    value_counts = df['기술분류'].value_counts().reset_index().head(10)
    value_counts.columns = ['기술분류', '출원 개수']
    # Plotly 막대그래프 그리기
    fig = px.bar(value_counts, x='기술분류', y='출원 개수',
                title='기술별 출원 개수(상위 10개)',
                labels={'기술분류': '기술분류', '출원 개수': '출원 개수'})
    st.plotly_chart(fig)