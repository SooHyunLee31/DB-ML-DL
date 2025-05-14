# 한국 전체 기술별 누적 출원수

def kor_cumulative_line(df_k):
    import streamlit as st
    import plotly.express as px
    import pandas as pd

    st.subheader('국내 기업 기술의 연도별 누적 출원 수')

    options = df_k['기술분류'].unique()
    op_default = [' 항공시스템', ' 생산기반기술', ' 정보통신모듈/부품', ' 정보이론', ' 로봇/자동화기계']
    selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)
    flag = False

    if st.button('확인', key='line'):
        if len(selected_options) > 5:
            st.warning('최대 5개까지만 선택할 수 있습니다.')
        else:
            st.write(f'선택한 항목: {selected_options}')
            flag = True

    if flag:
        df_k['출원일자'] = pd.to_datetime(df_k['출원일자'])
        cumulative = (
            df_k.groupby(['출원일자', '기술분류'])
            .size()
            .unstack(fill_value=0)
            .sort_index()
            .cumsum()
        )

        selected_cumulative = cumulative[selected_options]
        filtered_cumulative = selected_cumulative[selected_cumulative.index.to_period('M') >= pd.Period('2004-01-01', freq='M')]

        st.title('기술별 누적 특허 출원 수')
        fig = px.line(
            filtered_cumulative,
            title="기술별 누적 특허 출원 수",
            labels={"value": "누적 출원 수", "출원일자": "출원일자"},
            width=800,
            height=600
        )
        fig.update_layout(
            legend_title="기술분류",
            xaxis_title="출원일자",
            yaxis_title="누적 출원 수",
            template="plotly_dark"
        )
        st.plotly_chart(fig)
        st.divider()
        st.subheader('그래프 분석 예시')
        st.write('''이 그래프는 기술별 누적 특허 출원을 비교한 것입니다.
누적 곡선의 기울기를 통해 연구개발이 활발했던 시기를 파악할 수 있습니다.
국내는 기술별 격차가 크지 않고 완만한 상승세를 보이며, 제조·센서 기반의 방산 내재화에 집중된 반면,
해외는 항공시스템 등 첨단 분야에서 독주 양상을 보이고 있습니다.
''')
        st.image(f'image1/선그래프_기술별 누적 특허 출원 수 (국내).png', width=700)
        st.subheader('전략적 인사이트')
        st.write('''기술 성장 곡선 분석은 정부 핵심기술 선정의 객관적 기준이 될 뿐 아니라, 
R&D 투자의 최적 시점을 파악하는 데에도 유용한 전략 도구입니다.''')
        

# 해외 전체 기술별 누적 출원수

def for_cumulative_line(df_u):
    import streamlit as st
    import plotly.express as px
    import pandas as pd

    st.subheader('해외 기업 기술의 연도별 누적 출원 수')

    options = df_u['기술분류'].unique()
    op_default = [' 항공시스템', ' 생산기반기술', ' 정보통신모듈/부품', ' 정보이론', ' 로봇/자동화기계']
    selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)
    flag = False

    if st.button('그래프 확인', key='for_cumulative_btn'):
        if len(selected_options) > 5:
            st.warning('최대 5개까지만 선택할 수 있습니다.')
        else:
            st.write(f'선택한 항목: {selected_options}')
            flag = True

    if flag:
        df_u['출원일자'] = pd.to_datetime(df_u['출원일자'])

        cumulative = (
            df_u.groupby(['출원일자', '기술분류'])
            .size()
            .unstack(fill_value=0)
            .sort_index()
            .cumsum()
        )

        selected_cumulative = cumulative[selected_options]
        filtered_cumulative = selected_cumulative[selected_cumulative.index.to_period('M') >= pd.Period('2004-01-01', freq='M')]

        st.title('기술별 누적 특허 출원 수')
        fig = px.line(
            filtered_cumulative,
            title="기술별 누적 특허 출원 수",
            labels={"value": "누적 출원 수", "출원일자": "출원일자"},
            width=800,
            height=600
        )

        fig.update_layout(
            legend_title="기술분류",
            xaxis_title="출원일자",
            yaxis_title="누적 출원 수",
            template="plotly_dark"
        )

        st.plotly_chart(fig)
        st.divider()
        st.subheader('그래프 분석 예시')
        st.write('''이 그래프는 기술별 누적 특허 출원을 비교한 것입니다.
누적 곡선의 기울기를 통해 연구개발이 활발했던 시기를 파악할 수 있습니다.
국내는 기술별 격차가 크지 않고 완만한 상승세를 보이며, 제조·센서 기반의 방산 내재화에 집중된 반면,
해외는 항공시스템 등 첨단 분야에서 독주 양상을 보이고 있습니다.
''')
        st.image(f'image2/선그래프_기술별 누적 특허 출원 수 (해외).png', width=700)
        st.subheader('전략적 인사이트')
        st.write('''기술 성장 곡선 분석은 정부 핵심기술 선정의 객관적 기준이 될 뿐 아니라, 
R&D 투자의 최적 시점을 파악하는 데에도 유용한 전략 도구입니다.''')
