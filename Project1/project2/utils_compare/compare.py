import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def compare_pie(top1, top2):
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

    def create_donut_chart(data, title):
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

    st.subheader('상위 10개 기술 분포 국내외 비교')
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_donut_chart(top1, "국내 기업 방산 기술"), use_container_width=True)
    with col2:
        st.plotly_chart(create_donut_chart(top2, "해외 기업 방산 기술"), use_container_width=True)
    st.write('')
    st.write('**그래프 분석 예시**')
    st.write('''이 파이차트는 국내외 기술 편중 정도를 비교한 것입니다. 
국내의 경우, 자동차·철도차량 분야가 31.6%를 차지하며 기술 쏠림 현상이 뚜렷하게 나타납니다.
해외의 경우 상위 10개 기술분류 간 편차가 크지 않아, 다양한 분야에서 균형된 기술 발전이 이뤄지고 있다고 
할 수 있습니다.
''')
    st.write('')
    st.write('**전략적 인사이트**')
    st.write('국내 기술 포트폴리오는 다변화가 필요하며, 특정 분야 집중을 완화하는 전략적 분산이 요구됩니다.')
    st.divider()

def compare_bar_ratio(df_k, df_u):
    st.subheader('상위 20개 기술별 특허 비율 국내외 비교')
    df1 = df_k.copy()
    df2 = df_u.copy()
    df1['기업분류'] = '국내'
    df2['기업분류'] = '해외'
    df_a = pd.concat([df1, df2], ignore_index=True)
    top = df_a['기술분류'].value_counts().head(20).index
    df_top = df_a[df_a['기술분류'].isin(top)]

    count_df = df_top.groupby(['기술분류', '기업분류'], observed=True).size().reset_index(name='count')
    count_df['비율'] = count_df.apply(
        lambda row: row['count'] / len(df1) if row['기업분류'] == '국내' else row['count'] / len(df2),
        axis=1)
    count_df['기술분류'] = pd.Categorical(count_df['기술분류'], categories=top[::-1], ordered=True)

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

    fig.update_layout(legend_title_text='출원인', yaxis_title='기술분류', xaxis_title='비율', height=800)
    st.plotly_chart(fig)
    st.write('')
    st.write('**그래프 분석 예시**')
    st.write('''다음의 막대그래프는 국내외 상위 20개 기술분류의 특허 비율을 비교한 것입니다. 
국내는 자동차·철도차량 분야의 특허 비중이 높고, 정보통신·정보이론 등 신기술 분야의 중요도가 확대되고 있습니다. 
반면 해외는 항공시스템, 나노기술, 고분자화학 등에서 기술 주도권이 두드러집니다.
''')
    st.write('')
    st.write('**전략적 인사이트**')
    st.write('''국내 강세 분야인 정보통신/센서 분야의 기술은 민군 활용도가 높기 때문에, 중소기업과의 협업을 통한
기술사업화를 기대할 수 있습니다.
또한 상대적 열위인 분야들은 단기적인 글로벌 협력과 함께, 장기적인 기술 국산화 시도가 필요합니다. 
''')
    st.divider()

def compare_stack_year(df_k, df_u, start_year, end_year):

    def make_stacked(df, label):
        df['출원일자'] = pd.to_datetime(df['출원일자'])
        df = df[(df['출원일자'].dt.year >= start_year) & (df['출원일자'].dt.year <= end_year)]
        df['연도'] = df['출원일자'].dt.year
        grouped = df.groupby(['기술분류', '연도']).size().unstack(fill_value=0)
        top = grouped.sum(axis=1).sort_values(ascending=False).head(10)
        df_top = grouped.loc[top.index]
        melted = df_top.reset_index().melt(id_vars='기술분류', var_name='연도', value_name='개수')

        fig = px.bar(
            melted,
            x='기술분류',
            y='개수',
            color='연도',
            title=f'{label} 상위 10개 기술 연도별 특허 출원 수',
            barmode='stack',
            labels={'기술분류': '기술분류', '개수': '개수', '연도': '연도'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    make_stacked(df_k, '국내')
    make_stacked(df_u, '해외')
    st.write('')
    st.write('**그래프 분석 예시**')
    st.write('''국내 상위 11개 기업의 특허 출원은 꾸준히 증가하는 추세를 보이지만,
'자동차/철도차량', '무기센서' 등 일부 사업에만 치중되어 있습니다.
한편 해외 상위 11개 기업은 ‘항공시스템’, ‘정보기술’ 중심의 첨단 기술을 선도하며
다양한 산업 분야에 고르게 분산하여 투자하고 있습니다.
''')
    st.write('')
    st.write('**전략적 인사이트**')
    st.write('''해당 그래프는 정부의 기술 다변화 유도 필요성과
국내 대기업의 주도가 약한 '정보이론','로봇'등에서의 중소기업 및 스타트업의 진입 가능성을 시사 합니다.
''')
    st.divider()

def compare_monthly(df_k, df_u):
    st.subheader('월별 특허 출원 수 국내외 비교')
    def get_monthly_counts(df):
        df['출원일자'] = pd.to_datetime(df['출원일자'])
        df = df[df['출원일자'] >= '2004-01-01']
        return df.groupby(df['출원일자'].dt.to_period('M')).size().sort_index()

    domestic_counts = get_monthly_counts(df_k)
    foreign_counts = get_monthly_counts(df_u)

    domestic_counts.index = domestic_counts.index.to_timestamp()
    foreign_counts.index = foreign_counts.index.to_timestamp()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=domestic_counts.index, y=domestic_counts.values, mode='lines', name='국내 기업'))
    fig.add_trace(go.Scatter(x=foreign_counts.index, y=foreign_counts.values, mode='lines', name='해외 기업'))

    fig.update_layout(title='월별 특허 출원 수 국내외 비교',
                      xaxis_title='월',
                      yaxis_title='특허 수',
                      legend_title='기업 유형',
                      template='plotly_white')

    st.plotly_chart(fig)
    st.write('')
    st.write('**그래프 분석 예시**')
    st.write('''앞선 특허 누적 선 그래프를 월별 특허 출원 추이로 더 상세히 분석한 시계열 그래프 입니다.
국내 방산 기업의 연구 개발은 짧은 기간 산발적으로 급증했다가 바로 급감하는 형태를 보입니다.
반면 해외 방산 기업의 연구 개발은 월별 변동은 있으나 전반적으로 균형 잡힌 계단식 상승 구조를 보입니다.
''')
    st.write('')
    st.write('**전략적 인사이트**')
    st.write('''이러한 차이는 기술 개발 방식의 구조적 차이, 
즉 국내의 단기 중심 연구와 해외의 장기적 특허 운영 전략에서 비롯된 것으로 보입니다. 
국내 기업은 장기 과제를 추진하는 해외 기업의 전략을 벤치마킹하고, 
기술 개발과 출원 시점을 보다 분산화할 필요가 있습니다.
''')
    st.divider()


#  비교 탭 코드 삽입

def render_comparison_tab(df_k, df_u):
    top1 = df_k['기술분류'].value_counts().head(10)
    top2 = df_u['기술분류'].value_counts().head(10)
    compare_pie(top1, top2)
    compare_bar_ratio(df_k, df_u)
    st.subheader('연도별 상위 10개 기술 특허 출원 수 (국내/해외)')
    # 연도 범위 선택
    start_year, end_year = st.slider(
        '연도 선택 (최대 범위 5년)',
        2004, 2025, (2021, 2025)
    )
    compare_stack_year(df_k, df_u, start_year, end_year)

    compare_monthly(df_k, df_u)