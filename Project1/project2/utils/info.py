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