import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Any, Dict, List
import plotly.graph_objects as go

st.title("비교")
st.write('')
df_k = pd.read_csv('data/KIPRIS 전체.csv')
df_u = pd.read_csv('data/WIPO 전체.csv')

top1 = df_k['기술분류'].value_counts().head(10)
top2 = df_u['기술분류'].value_counts().head(10)

cols = [top1, top2]
titles = ['국내 기업 방산 특허 기술', '해외 기업 방산 특허 기술']

# 색상 매핑 고정
colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']

######## 파이차트 : 국내외 기술분류 비교 ####### 
st.subheader('상위 10개 기술 분포 국내외 비교')

# 차트 생성 함수
def create_donut_chart(data, title, colors):
    fig = go.Figure(data=[go.Pie(
        labels=data.index,
        values=data.values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='percent+label',
        textposition='inside',
        sort=False
    )])
    fig.update_layout(title=title, showlegend=False)
    return fig
# 레이아웃: 가로 2분할
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(create_donut_chart(top1, "국내 기업 방산 기술", colors), use_container_width=True)
with col2:
    st.plotly_chart(create_donut_chart(top2, "해외 기업 방산 기술", colors), use_container_width=True)

st.divider()

######## 막대 그래프 : 기술 분류별 국내외 방산 특허 비율 비교 ####### 
st.subheader('상위 20개 기술별 특허 비율 국내외 비교')
df1 = df_k.copy()
df2 = df_u.copy()

# 데이터전처리
df1['기업분류'] = '국내'
df2['기업분류'] = '해외'
df_a = pd.concat([df1, df2], ignore_index=True)
top = df_a['기술분류'].value_counts().head(20).index
df_top = df_a[df_a['기술분류'].isin(top)]

# 기술분류와 기업분류별 건수
count_df = df_top.groupby(['기술분류', '기업분류'], observed=True).size().reset_index(name='count')
# 비율 계산
count_df['비율'] = count_df.apply(
    lambda row: row['count'] / len(df_k) if row['기업분류'] == '국내' else row['count'] / len(df_u),
    axis=1)
# 정렬된 순서 유지
count_df['기술분류'] = pd.Categorical(count_df['기술분류'], categories=top[::-1], ordered=True)

# Plotly 수평 막대 그래프
fig = px.bar(
    count_df,
    y='기술분류',
    x='비율',
    color='기업분류',
    orientation='h',
    barmode='group',
    labels={'비율': '비율', '기술분류': '기술 분류'},
    title='상위 20개 기술별 특허 비율 국내외 비교'
)

fig.update_layout(
    legend_title_text='출원인',
    yaxis_title='기술분류',
    xaxis_title='비율',
    height=800
)

# Streamlit에 출력
st.plotly_chart(fig, use_container_width=True)

st.divider()

######## 선 그래프 : 기술별 누적 출원 수 ####### 
st.subheader('국내 기업 기술의 연도별 누적 출원 수')

# 여러 개의 항목 리스트
options = df_k['기술분류'].unique()
op_default = [' 항공시스템', ' 생산기반기술', ' 정보통신모듈/부품', ' 정보이론', ' 로봇/자동화기계']

# 다섯 개 항목만 선택할 수 있게 하기
selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)
flag = False
if st.button('그래프 확인'):
    # 선택한 항목이 5개를 초과하면 경고 메시지 출력
    if len(selected_options) > 5:
        st.warning('최대 5개까지만 선택할 수 있습니다.')
    else:
        # 선택한 항목 출력
        st.write(f'선택한 항목: {selected_options}')
        flag = True
if flag:
    # 날짜 처리
    df_k['출원일자'] = pd.to_datetime(df_k['출원일자'])

    # 월별, 분류별 집계 후 누적합
    cumulative = (
        df_k.groupby(['출원일자', '기술분류'])
        .size()
        .unstack(fill_value=0)
        .sort_index()
        .cumsum()
    )

    # 사용자 지정 분류
    selected_categories = selected_options
    # selected_categories = df_u['기술분류'].value_counts().head(5).index
    selected_cumulative = cumulative[selected_categories]

    # 출원일자 컬럼을 Period 형식으로 변환 후 필터링
    filtered_cumulative = selected_cumulative[selected_cumulative.index.to_period('M') >= pd.Period('2004-01-01', freq='M')]

    # Plotly로 그래프 그리기
    st.title('기술별 누적 특허 출원 수')

    # 그래프 만들기
    fig = px.line(filtered_cumulative, 
                title="기술별 누적 특허 출원 수",
                labels={"value": "누적 출원 수", "출원일자": "출원일자"},
                width=800, height=600)

    # 레전드 추가
    fig.update_layout(
        legend_title="기술분류",
        xaxis_title="출원일자",
        yaxis_title="누적 출원 수",
        template="plotly_dark"
    )

    # Streamlit에서 Plotly 그래프 표시
    st.plotly_chart(fig)

st.divider()

######## 연도별 상위 10개 기술 특허 출원 수 (막대 그래프) ####### 
st.subheader('특허기술누적(연도별)')

# 범위 슬라이더 생성 (2004에서 2025까지 선택 가능)
start_year, end_year = st.slider(
    '연도 선택 (최대 범위 5년)',
    2004, 2025, (2004, 2025)
)
flag = False
# 종료 연도가 시작 연도에서 5년 이상 차이나면 조정
year_range = list(range(start_year, end_year + 1))

if st.button('확인'):
    if end_year - start_year > 4:
        st.warning('최대 5년까지만 선택할 수 있습니다.')
    else:
        # 선택한 항목 출력
        st.write(f'선택한 항목: {year_range}')
        flag = True

if flag:
    # 국내
    df_k['출원일자'] = pd.to_datetime(df_k['출원일자'])
    df_k = df_k[(df_k['출원일자'].dt.year >= start_year) & (df_k['출원일자'].dt.year <= end_year)]
    df_k['연도'] = df_k['출원일자'].dt.year
    df_grouped = df_k.groupby(['기술분류', '연도']).size().unstack(fill_value=0)

    # 상위 10개 기술분류 추출
    top = df_grouped.sum(axis=1).sort_values(ascending=False).head(10)

    # top 10 기술분류만 필터링
    df_top = df_grouped.loc[top.index]

    # plotly에서 사용 가능한 long-form 데이터로 변환
    df_melted = df_top.reset_index().melt(id_vars='기술분류', var_name='연도', value_name='개수')

    # 누적 막대그래프 그리기
    fig = px.bar(
        df_melted,
        x='기술분류',
        y='개수',
        color='연도',
        title='연도별 상위 10개 기술 특허 출원 수 (국내)',
        labels={'기술분류': '기술분류', '개수': '개수', '연도': '연도'},
    )

    fig.update_layout(barmode='stack', xaxis_tickangle=-45)

    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 해외
    df_u['출원일자'] = pd.to_datetime(df_u['출원일자'])
    df_u = df_u[(df_u['출원일자'].dt.year >= start_year) & (df_u['출원일자'].dt.year <= end_year)]
    df_u['연도'] = df_u['출원일자'].dt.year
    df_grouped2 = df_u.groupby(['기술분류', '연도']).size().unstack(fill_value=0)

    # 상위 10개 기술분류 추출
    top2 = df_grouped2.sum(axis=1).sort_values(ascending=False).head(10)

    # top 10 기술분류만 필터링
    df_top2 = df_grouped2.loc[top2.index]

    # plotly에서 사용 가능한 long-form 데이터로 변환
    df_melted2 = df_top2.reset_index().melt(id_vars='기술분류', var_name='연도', value_name='개수')

    # 누적 막대그래프 그리기
    fig = px.bar(
        df_melted2,
        x='기술분류',
        y='개수',
        color='연도',
        title='연도별 상위 10개 기술 특허 출원 수 (해외)',
        labels={'기술분류': '기술분류', '개수': '개수', '연도': '연도'},
    )

    fig.update_layout(barmode='stack', xaxis_tickangle=-45)

    # Streamlit에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)


st.divider()

######## 월별 특허 출원 수 국내외 비교 (선선 그래프) ####### 
st.subheader('월별 특허 출원 수')

# 날짜를 월 단위로 변환 후 그룹화
def get_monthly_counts(df):
    df['출원일자'] = pd.to_datetime(df['출원일자'])
    df = df[df['출원일자'] >= '2004-01-01']
    return df.groupby(df['출원일자'].dt.to_period('M')).size().sort_index()

df_k = pd.read_csv('data/KIPRIS 전체.csv')
df_u = pd.read_csv('data/WIPO 전체.csv')
# 월별 데이터 추출
domestic_counts = get_monthly_counts(df_k)
foreign_counts = get_monthly_counts(df_u)

# 인덱스를 datetime으로 변환
domestic_counts.index = domestic_counts.index.to_timestamp()
foreign_counts.index = foreign_counts.index.to_timestamp()

# Plotly 그래프 객체 생성
fig = go.Figure()

fig.add_trace(go.Scatter(x=domestic_counts.index, y=domestic_counts.values,
                         mode='lines', name='국내 기업'))
fig.add_trace(go.Scatter(x=foreign_counts.index, y=foreign_counts.values,
                         mode='lines', name='해외 기업'))

fig.update_layout(title='월별 특허 출원 수 국내외 비교',
                  xaxis_title='월',
                  yaxis_title='특허 수',
                  legend_title='기업 유형',
                  template='plotly_white')

st.plotly_chart(fig)

st.divider()

######## 산점도 : 기술/기업/연도 한눈에 보기 ####### 
st.subheader('기업별 특허 출원일자와 특허기술 (국내)')

# 여러 개의 항목 리스트
options = df_k['출원인'].unique()
op_default = ['KAI', '한화에어로스페이스', 'LIG넥스원']

# 다섯 개 항목만 선택할 수 있게 하기
selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)
flag = False
if st.button('확인', key='scatter'):
    flag = True
    df = df_k.copy()

    # 데이터 전처리
    df = df[df['출원인'].isin(selected_options)]
    df = df.dropna(subset=['IPC분류'])
    df['출원일자'] = pd.to_datetime(df['출원일자'], format='%Y-%m-%d')
    df = df[df['출원일자'] >= '2004-01-01']

    # 상위 20개 기술분류 필터링
    counts = df.groupby('기술분류').size().sort_values(ascending=False)
    top = counts.head(20).index
    df = df[df['기술분류'].isin(top)]

    # IPC분류 정렬 순서 설정
    ipc_order = df[['IPC분류', '기술분류']].drop_duplicates().sort_values('기술분류')['IPC분류']
    df['IPC분류'] = pd.Categorical(df['IPC분류'], categories=ipc_order, ordered=True)

    # IPC -> 기술분류 매핑
    ipc_to_tech = df.drop_duplicates(subset=['IPC분류'])[['IPC분류', '기술분류']].set_index('IPC분류')['기술분류'].to_dict()

    # y축 라벨 압축 표시용 함수
    def keep_center_only(labels):
        new_labels = [''] * len(labels)
        i = 0
        while i < len(labels):
            j = i
            while j < len(labels) and labels[j] == labels[i]:
                j += 1
            mid = (i + j - 1) // 2
            new_labels[mid] = labels[mid]
            i = j
        return new_labels

    # 압축된 y축 라벨 생성
    original_labels = [ipc_to_tech.get(ipc, ipc) for ipc in df['IPC분류'].cat.categories]
    compressed_labels = keep_center_only(original_labels)

    # Plotly용 y값 변환 (카테고리 순서 기준 인덱스)
    df['IPC_idx'] = df['IPC분류'].cat.codes

    # Plotly 산점도 그리기
    fig = px.scatter(
        df,
        x='출원일자',
        y='IPC_idx',
        color='출원인',
        opacity=0.5,
        labels={'IPC_idx': '기술분류'},
        title='기업별 특허 출원일자와 특허기술',
        hover_data=['출원인', '출원일자', '기술분류'],
        height=800,
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    # y축 눈금 이름 수정
    fig.update_yaxes(
        tickmode='array',
        tickvals=list(range(len(compressed_labels))),
        ticktext=compressed_labels,
        tickfont=dict(size=10)
    )

    # Streamlit에서 출력
    st.plotly_chart(fig, use_container_width=True)


st.subheader('기업별 특허 출원일자와 특허기술 (해외)')

# 여러 개의 항목 리스트
options = df_u['출원인'].unique()
op_default = ['NORINCO', 'L3Harris Technologies']

# 다섯 개 항목만 선택할 수 있게 하기
selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)
flag = False
if st.button('확인', key='scatter2'):
    flag = True
    df = df_u.copy()

    # 데이터 전처리
    df = df[df['출원인'].isin(selected_options)]
    df = df.dropna(subset=['IPC분류'])
    df['출원일자'] = pd.to_datetime(df['출원일자'], format='%Y-%m-%d')
    df = df[df['출원일자'] >= '2004-01-01']

    # 상위 20개 기술분류 필터링
    counts = df.groupby('기술분류').size().sort_values(ascending=False)
    top = counts.head(20).index
    df = df[df['기술분류'].isin(top)]

    # IPC분류 정렬 순서 설정
    ipc_order = df[['IPC분류', '기술분류']].drop_duplicates().sort_values('기술분류')['IPC분류']
    df['IPC분류'] = pd.Categorical(df['IPC분류'], categories=ipc_order, ordered=True)

    # IPC -> 기술분류 매핑
    ipc_to_tech = df.drop_duplicates(subset=['IPC분류'])[['IPC분류', '기술분류']].set_index('IPC분류')['기술분류'].to_dict()

    # y축 라벨 압축 표시용 함수
    def keep_center_only(labels):
        new_labels = [''] * len(labels)
        i = 0
        while i < len(labels):
            j = i
            while j < len(labels) and labels[j] == labels[i]:
                j += 1
            mid = (i + j - 1) // 2
            new_labels[mid] = labels[mid]
            i = j
        return new_labels

    # 압축된 y축 라벨 생성
    original_labels = [ipc_to_tech.get(ipc, ipc) for ipc in df['IPC분류'].cat.categories]
    compressed_labels = keep_center_only(original_labels)

    # Plotly용 y값 변환 (카테고리 순서 기준 인덱스)
    df['IPC_idx'] = df['IPC분류'].cat.codes

    # Plotly 산점도 그리기
    fig = px.scatter(
        df,
        x='출원일자',
        y='IPC_idx',
        color='출원인',
        opacity=0.5,
        labels={'IPC_idx': '기술분류'},
        title='기업별 특허 출원일자와 특허기술',
        hover_data=['출원인', '출원일자', '기술분류'],
        height=800,
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    # y축 눈금 이름 수정
    fig.update_yaxes(
        tickmode='array',
        tickvals=list(range(len(compressed_labels))),
        ticktext=compressed_labels,
        tickfont=dict(size=10)
    )

    # Streamlit에서 출력
    st.plotly_chart(fig, use_container_width=True)