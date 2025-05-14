# 기업별 특허 출원일자와 특허기술(국내)

def kor_ipc_scatter(df_k): 
    import streamlit as st
    import plotly.express as px
    import pandas as pd

    st.subheader('기업별 특허 출원일자와 특허기술 (국내)')

    options = df_k['출원인'].unique()
    op_default = ['KAI', '한화에어로스페이스', 'LIG넥스원']
    selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)

    if st.button('확인', key='scatter'):
        df = df_k.copy()
        df = df[df['출원인'].isin(selected_options)]
        df = df.dropna(subset=['IPC분류'])
        df['출원일자'] = pd.to_datetime(df['출원일자'], format='%Y-%m-%d')
        df = df[df['출원일자'] >= '2004-01-01']

        counts = df.groupby('기술분류').size().sort_values(ascending=False)
        top = counts.head(20).index
        df = df[df['기술분류'].isin(top)]

        ipc_order = df[['IPC분류', '기술분류']].drop_duplicates().sort_values('기술분류')['IPC분류']
        df['IPC분류'] = pd.Categorical(df['IPC분류'], categories=ipc_order, ordered=True)
        ipc_to_tech = df.drop_duplicates(subset=['IPC분류'])[['IPC분류', '기술분류']].set_index('IPC분류')['기술분류'].to_dict()

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

        original_labels = [ipc_to_tech.get(ipc, ipc) for ipc in df['IPC분류'].cat.categories]
        compressed_labels = keep_center_only(original_labels)
        df['IPC_idx'] = df['IPC분류'].cat.codes

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
        fig.update_yaxes(
            tickmode='array',
            tickvals=list(range(len(compressed_labels))),
            ticktext=compressed_labels,
            tickfont=dict(size=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()
        st.subheader('그래프 분석 예시')
        st.write('''다음은 국내 기업별 특허 기술의 출원일자를 표현한 산점도 입니다.
11개의 기업 중 조회하고자 하는 기업을 선택해 산점도를 확인할 수 있으며,
보시는 산점도는 한화에어로스페이스, 한국항공우주산업, LIG넥스원의 특허기술과 출원시기를 나타냅니다.

한화에어로스페이스는 최근 5년간무기화생방/화력탄약 기술에 집중하고 있고,
한국항공우주산업(KAI)는 대부분 기간에 항공 시스템 기술에 집중하는 것을 학인할 수 있습니다.
한편 LIG 넥스원은 전반적인 ICT 기반 무기 시스템에 고르게 기술을 보유함과 동시에,
출원시기의 분포가 넓어 지속적이고 활발한 투자 추세를 보이고 있습니다.
''')
        st.image(f'image1/산점도_기업별 특허 출원일자와 특허기술 (국내).png', width=700)
        st.subheader('전략적 인사이트')
        st.write('''해당 산점도의 활용을 통해 산업 내의 전략기술 및 중복투자 영역에서 
산학연 협력과 기술 차별화 전략 수립을 고려할 수 있고,
정부나 방위사업청의 특허 포지셔닝 기반 R&D 중복 방지와 효율적 예산 배분을 기대할 수 있습니다.''')
        

# 기업별 특허 출원일자와 특허기술(해외)

def for_ipc_scatter(df_u):
    import streamlit as st
    import plotly.express as px
    import pandas as pd

    st.subheader('기업별 특허 출원일자와 특허기술 (해외)')

    options = df_u['출원인'].unique()
    op_default = ['NORINCO', 'L3Harris Technologies']
    selected_options = st.multiselect('옵션을 선택하세요', options, default=op_default)

    if st.button('확인', key='scatter_for'):
        df = df_u.copy()
        df = df[df['출원인'].isin(selected_options)]
        df = df.dropna(subset=['IPC분류'])
        df['출원일자'] = pd.to_datetime(df['출원일자'], format='%Y-%m-%d')
        df = df[df['출원일자'] >= '2004-01-01']

        counts = df.groupby('기술분류').size().sort_values(ascending=False)
        top = counts.head(20).index
        df = df[df['기술분류'].isin(top)]

        ipc_order = df[['IPC분류', '기술분류']].drop_duplicates().sort_values('기술분류')['IPC분류']
        df['IPC분류'] = pd.Categorical(df['IPC분류'], categories=ipc_order, ordered=True)
        ipc_to_tech = df.drop_duplicates(subset=['IPC분류'])[['IPC분류', '기술분류']].set_index('IPC분류')['기술분류'].to_dict()

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

        original_labels = [ipc_to_tech.get(ipc, ipc) for ipc in df['IPC분류'].cat.categories]
        compressed_labels = keep_center_only(original_labels)
        df['IPC_idx'] = df['IPC분류'].cat.codes

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

        fig.update_yaxes(
            tickmode='array',
            tickvals=list(range(len(compressed_labels))),
            ticktext=compressed_labels,
            tickfont=dict(size=10)
        )

        st.plotly_chart(fig, use_container_width=True)
        
        