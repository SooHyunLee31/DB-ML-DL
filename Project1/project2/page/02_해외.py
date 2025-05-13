import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import json

st.title("해외")
data = pd.read_csv('data/WIPO 전체.csv')
# data = data.drop(columns=['법적상태'])
ipc = pd.read_excel('data/IPC 분류표.xlsx')
ipc_info_df = pd.read_excel('data/IPC코드설명표.xlsx')

# 최상단 메뉴 선택
menu = st.sidebar.radio("선택", ["전체", "기업별"])
# data = data.drop(columns=['법적상태'])
ipc = pd.read_excel('data/IPC 분류표.xlsx')
ipc_info_df = pd.read_excel('data/IPC코드설명표.xlsx')

if menu == '전체':
    tab1, tab2 = st.tabs(["기술별 조회","연도별 조회"])

    def show_tech():
        df1 = data.copy()
        df1 = df1.drop(columns='Unnamed: 0')
        df1 = df1.dropna(subset=['기술분류'])
        tech_options = sorted(df1['기술분류'].unique())
        tech = st.selectbox('기술분류 선택', tech_options)

        st.divider()
        st.header(f"기술분류: {tech}")
        filtered_df = df1[df1['기술분류'] == tech].copy()
        filtered_df['출원일자'] = pd.to_datetime(filtered_df['출원일자'], errors='coerce')
        filtered_df['출원일자'] = filtered_df['출원일자'].dt.date
        filtered_df = filtered_df.set_index('기술분류')

        st.dataframe(filtered_df)
        st.divider()

    with tab1:
        show_tech()

            
    def year_show():
        df1 = data.copy()  # '전체'는 필터 없이 전체 데이터 기준
        df1 = df1.dropna(subset=['출원일자']) 
        df1['출원일자'] = pd.to_datetime(df1['출원일자'])
        df1['연도'] = df1['출원일자'].dt.year.astype(int)
        year_options = sorted(df1['연도'].unique(), reverse=True)
        year = st.selectbox('연도 선택', year_options)
        st.divider()

        st.header(f"전체 특허 기술 - {year}년도")
        df1 = df1[df1['연도']==year].set_index('기술분류')
        df1['출원일자'] = df1['출원일자'].dt.date
        df1 = df1[['IPC분류', '발명의명칭',  '출원인', '출원일자','요약']]
        st.dataframe(df1)
        st.divider()
    with tab2:
        year_show()

if menu == '기업별':
    choice = st.selectbox('기업', ('Lockheed  Martin Corporation','RTX Corporation','Northrop Grumman Corporation','The Boeing Company','General Dynamics Corporation', 
                                 'BAE Systems','Rostec', 'AVIC', 'NORINCO', 'CETC','L3Harris Technologies'))


    tab1, tab2, tab3  = st.tabs(["기업분석","특허기술 분석","연도별 조회"])
    # 기업분석 안에 기업 담당분야 설명 추가, 기업별 특허기술에 IPC 분류코드 df 추가
    with tab1:
        st.title(f'{choice} 정보')
        if choice == 'Lockheed  Martin Corporation':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':["군용항공기","미사일 및 화력통제(MFC)","방위전자 및 통신시스템(RMS)","우주 시스템"],
                '내용':["F-35 등 군용 항공기 개발 및 생산", "공대지 공대공 미사일, 전자광학센서, 화력통제시스템", "헬리콥터 및 해양 시스템", "군산업용 위성, 추적 시스템, 우주발사체"]
            })

            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/록히드 마틴 .png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write('''당사는 1995년에 록히드와 마틴 마리에타의 합병으로 설립된 세계 최고의 항공우주 · 방위산업체입니다. 
                    항공우주기술 부문이 주력 사업이며, F-35 전투기로 대표되는 군용기 사업 외에도 육해공, 해병대, 우주, 사이버의 모든 군사무기, 기술 등을 제공합니다.''')
            st.divider()
            # 주요 사업 내용 표시시
            st.header('주요 사업 내용')
            st.dataframe(df)

        if choice == 'RTX Corporation':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':["항공기 엔진 제조(Pratt & Whitney)","항공기 부품·시스템(Collins Aerospace)","방위산업(Raytheon)"],
                '내용':["항공기 엔진 개발 및 생산","항공우주 시스템 및 부품","미사일 및 방위 시스템"]
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/RTX.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write("당사는 항공우주 및 방위산업 분야의 글로벌 기업으로, 항공기 엔진, 방위 시스템, 우주 시스템 등을 제공합니다.")
            st.divider()
            # 주요 사업 내용 표시시
            st.header('주요 사업 내용')
            st.dataframe(df)

        if choice == 'Northrop Grumman Corporation':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':["군용항공기", "무기체계","방위전자","우주 시스템"],
                '내용':["무인 항공기 및 유인 항공기","정밀타격무기, 고속 추진체","첨단 센서 및 레이더, 통신 네트워크","군산업용 위성, 우주발사체"]
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/노스롭.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write('''당사는 미국의 다국적 항공우주 및 방위 기업입니다. 
                    세계 최대 규모의 무기 제조업체 이자 군사 기술 공급업체 중 하나이며, 항공우주 및 방위산업 분야의 주요 기업으로, 무인 항공기, 우주 시스템, 방위 전자 시스템 등을 개발합니다. 
                    특히 재래식 무기와 핵무기를 투하할 수 있는 장거리 스텔스 전략 폭격기 인 B-21 레이더 개발을 주도하고 있습니다. 
                    이 폭격기 는 세계 유일의 스텔스 폭격기로 알려진 노스럽 그루먼의 B-2 스피릿을 대체할 예정입니다. 
                    노스럽 그루먼의 다른 프로젝트로는 NASA의 우주 발사 시스템(SLS) 프로그램을 위한 고체 로켓 부스터를 생산하고 있습니다.''')
            st.divider()
            # 주요 사업 내용 표시
            st.header('주요 사업 내용')
            st.dataframe(df)

        
        if choice == 'The Boeing Company':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':["상업용 항공기(BCA)", "방위 우주 시스템 (BDS)", "항공기 유지보수(BGS)"],
                '내용':["화물기","군용 항공기,헬리콥터,무인기, 우주 시스템, 방공·미사일 시스템", "항공기 정비·개조·업그레이드,디지털 솔루션"]
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/보잉.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write('''당사는 미국 버지니어주 알링턴에 본사를 둔 세계적인 상업용 항공기, 방위 시스템, 우주 시스템 등을 개발 및 생산하는 글로벌 항공우주 기업으로, 1916년 설립된 이후 100년이 넘는 시간 동안 항공 산업을 선도해 왔습니다. 
                    전 세계 약 150개국 이상에 제품과 서비스를 공급하고 있으며, Boeing은 지속 가능한 항공 산업을 위한 친환경 항공기 개발과 함께 디지털 전환을 가속화하고 있으며, 우주 탐사 영역에서도 NASA와의 협업을 통해 차세대 우주 개발에 적극 참여하고 있습니다.''')
            st.divider()
            # 주요 사업 내용 표시시
            st.header('주요 사업 내용')
            st.dataframe(df)

        if choice == 'General Dynamics Corporation':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':["비즈니스 항공기", "지상무기체계", "IT", "해양 시스템"],
                '내용':["중대형급 제트기(Gulfstream)","장갑차, 무인차량,기관포,탄약","정보감시정찰(ISR), 사이버방어, 국방네트워크 구축및 운영","핵잠수함, 수상함,군수지원함"]
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/제너럴 다이내믹스 .png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write('''당사는 버지니아주에 본사를 둔 항공우주 및 방산 기업으로, 회사의 주요 사업은 크게 항공우주, 해양 시스템, 전투 시스템, 그리고 정보기술 및 통신 시스템 분야를 제공하는 방위산업 입니다.
                    방산 및 민간 부문 모두에서 기술 경쟁력을 바탕으로 세계 각국의 고객에게 전략적 가치를 제공하며, 특히 NATO와 인도·태평양 지역과의 방산 협력을 강화하고 있습니다. 최근에는 친환경 항공 기술과 지능형 군사 시스템 개발에도 집중하면서 지속적인 혁신을 추구하고 있습니다.''')
            st.divider()
            # 주요 사업 내용 표시시
            st.header('주요 사업 내용')
            st.dataframe(df)

        if choice == 'BAE Systems': 
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':["건설기계", "엔진"],
                '내용':["굴착기, 휠로더", 
                    "엔진, 발전기, A/S부품"]
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/베이 시스템즈.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write("당사는 영국의 다국적 방위, 보안, 항공우주 기업으로, 전 세계에 다양한 방위 시스템을 제공합니다.")
            st.divider()
            # 주요 사업 내용 표시시
            st.header('주요 사업 내용')
            st.dataframe(df)

        
        if choice == 'Rostec':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':['방위산업','민간 항공기','전자 및 광학 장비','기계 및 장비'],
                '내용':['방공 및 미사일 시스템, 전자 및 광전자 장비','항공기', '소형화기','방공 및 미사일 시스템']
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/로스텍 로고 .png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write('''당사는 러시아 정부가 2007년에 설립한 국영 복합기업으로, 첨단 기술 산업 제품의 개발, 생산 및 수출을 촉진하는 것을 목적으로 합니다. 
                    군수 산업뿐만 아니라 민간 산업 분야에서도 활동하며, 러시아의 기술 주권 확보와 산업 현대화에 중추적인 역할을 수행하고 있습니다.''')
            st.divider()
            # 주요 사업 내용 표시시
            st.header('주요 사업 내용')
            st.dataframe(df)
        
        if choice == 'AVIC':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':['군용 항공기 및 방위 산업','민간 항공기 및 일반항공','무인기(UAV) 및 드론', '우주 항공 기술'],
                '내용':['전투기,폭격기,수송기','중형 항공기, 민간 항공기', '군용 산업용 무인기','위성플랫폼, 로켓 부품 공급']
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/AVIC.jpg', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write("중국 국무원 산하의 국유 항공우주 및 방산 대기업으로, 군용 및 민간 항공기, 무인기(UAV), 헬리콥터, 항공전자 시스템, 우주항공 기술 등 중국 항공 산업 전반을 대표하는 핵심 기업입니다.")
            st.divider()
            # 주요 사업 내용 표시
            st.header('주요 사업 내용')
            st.dataframe(df)

        
        if choice == 'NORINCO':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':['방위산업','자원 개발','기계 및 차량 제조', '화학 제품 및 산업 장비'],
                '내용':['전차 및 장갑차, 포병 시스템, 로켓 및 미사일, 소화기','석유 및 천연가스 탐가 시추','특수목적 차량(SPV),산업용 중장비, 민수용 SUV','화학 및 폭발물']
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/노린코.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write("당사는 중국 인민해방군(PLA)의 주요 무기 공급업체로서, 육군, 해군, 공군, 로켓군, 전략지원부대, 무장경찰 및 공공안전 부문에 다양한 무기와 기술 지원 서비스를 제공합니다."
    )
            st.divider()
            # 주요 사업 내용 표시
            st.header('주요 사업 내용')
            st.dataframe(df)


        if choice == 'CETC':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':['전자 장비 및 시스템 통합', '기초 소프트웨어 및 하드웨어','네트워크 및 사이버 보안', '인공지능 및 스마트 기술' ],
                '내용':['레이더시스템, 전자전 장비, 통신시스템','운영체제 및 CPU 개발, 마이크로전자 설계, 직접회로(IC)','사이버방어 플랫폼','군사 민사 AI, 딥러닝 프레임워크, 엣지AI칩']
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/CETC.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write("당사는 2002년에 설립된 중국 국유기업 입니다 . 통신장비, 컴퓨터, 전자장비, IT 인프라, 네트워크, 소프트웨어 개발, 연구 서비스, 민간 및 군수용 투자 및 자산 관리 분야를 다룹니다.")
            st.divider()
            # 주요 사업 내용 표시
            st.header('주요 사업 내용')
            st.dataframe(df)


        if choice == 'L3Harris Technologies':
            # 사업 내용 데이터프레임
            df = pd.DataFrame({
                '부문':['통합 임무시스템', '우주 및 항공 시스템', '통신시스템', 'Aerojet Rocketdyne'],
                '내용':['감시 정찰 ISR플랫폼, 전자전 시스템','위성 탑재체, 항법시스템, 항공용 센서','위성통신(SATCOM), 소형 전술 무전기 시리즈(Falcon)','로켓 추진체, 극초음속 무기 추진체']
            })
            
            df = df.set_index('부문')
            # 기업 로고, 소개 내용
            st.header('기업 소개')
            st.divider()
            st.image('image2/L3.png', caption=f'{choice} 로고', width=500)
            st.subheader('소개 내용')
            st.write("당사는 미국의 기술 회사 , 방위 계약자 , 정보 기술 서비스 제공업체로 , 명령 및 통제 시스템, 무선 장비, 전술 무선기, 항공 전자 및 전자 시스템, 야간 투시 장비 , 정보 , 감시 및 정찰 ( C3ISR ) 시스템 및 제품, 해양 시스템 , 계측기 , 항법 제품, 훈련 장치 및 서비스, 그리고 정부, 방위 및 상업 분야에서 사용되는 지상/우주 안테나를 생산합니다.")
            st.divider()
            # 주요 사업 내용 표시
            st.header('주요 사업 내용')
            st.dataframe(df)


        st.write("")

    # 파이차트 상세설명 함수
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
        a = data[data['출원인'] == choice]
        b = a.drop(columns='Unnamed: 0')
        options = np.insert(a['기술분류'].unique(), 0, '전체')
        tech = st.selectbox('기술 분야 선택', options, key=f'{choice}_tech_selectbox')
        st.divider()

        if tech != '전체':
            st.header(f'{choice} 특허 기술 - {tech}')
            st.dataframe(b[b['기술분류'] == tech].set_index('기술분류'))
            st.divider()

            # 선택한 기술분야만 출력
            c = b[b['기술분류'] == tech]
            c_list = c['IPC분류'].unique()
            # IPC 분류 상위 10개 시각화
            ipc_counts = c[c['출원인'] == choice]['IPC분류'].value_counts().reset_index()
            ipc_counts.columns = ['IPC', '빈도수']
            top_ipc = ipc_counts.head(10)
            fig = make_info_fig(top_ipc, ipc_info_df)
            st.header('기술 분야 별 요약')
            st.plotly_chart(fig)
        else:
            st.header(f'{choice} 특허 기술 - {tech}')
            c = b.set_index('기술분류')
            st.dataframe(c)
            st.divider()

            ipc_counts = c[c['출원인'] == choice]['IPC분류'].value_counts().reset_index()
            ipc_counts.columns = ['IPC', '빈도수']
            top_ipc = ipc_counts.head(10)
            fig = make_info_fig(top_ipc, ipc_info_df)

            st.header('기술 분야 별 요약')
            st.plotly_chart(fig)      

    # '특허기술 분석' 탭 클릭 시
    with tab2:
        if choice == 'Lockheed  Martin Corporation':
            make_pie_chart()    

        if choice =='RTX Corporation':
            make_pie_chart()

        if choice =='Northrop Grumman Corporation':
            make_pie_chart()

        if choice =='The Boeing Company':
            make_pie_chart()

        if choice =='General Dynamics Corporation':
            make_pie_chart()

        if choice == 'BAE Systems':
            make_pie_chart()

        if choice == 'Rostec':
            make_pie_chart()

        if choice ==  'AVIC':
            make_pie_chart()

        if choice ==  'NORINCO':
            make_pie_chart()

        if choice == 'CETC':
            make_pie_chart()

        if choice == 'L3Harris Technologies':
            make_pie_chart()

    def make_info_bar(top_ipc, ipc_info_df):
        # 설명 붙이기
        top_ipc = pd.merge(top_ipc, ipc_info_df, on='IPC', how='left')
        # 바 차트 생성
        fig = px.bar(
            top_ipc,
            x='IPC',
            y='빈도수',
            title='상위 10개 기술분류',
            custom_data=['설명']
        )
        # 마우스 오버 시 설명 출력
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>빈도수: %{y}<br>%{customdata[0]}<extra></extra>'
        )
        return fig

    def year_show():
        df1 = data[data['출원인'] == choice]
        df1 = df1.drop(columns='Unnamed: 0')
        df1['출원일자'] = pd.to_datetime(df1['출원일자'])
        df1 = df1.sort_values(by='출원일자').reset_index(drop=True)
        df1['연도'] = df1['출원일자'].dt.year
        year_options = df1['연도'].unique()
        year = st.selectbox('연도 선택', year_options)
        st.divider()

        st.header(f'{choice} 특허 기술 - {year}년도')
        df1 = df1[df1['연도'] == year].set_index('연도')
        df1['출원일자'] = df1['출원일자'].dt.date
        df1 = df1[['발명의명칭', 'IPC분류', '기술분류', '출원일자', '출원인', '요약']]
        st.dataframe(df1)
        st.divider()

        # 선택한 기술분야만 출력
        ipc_list = df1['IPC분류'].unique()
        # IPC 분류 상위 10개 시각화
        ipc_counts = df1[df1['출원인'] == choice]['IPC분류'].value_counts().reset_index()
        ipc_counts.columns = ['IPC', '빈도수']
        top_ipc = ipc_counts.head(10)
        fig = make_info_bar(top_ipc, ipc_info_df)
        st.header(f'{year}년도 특허 기술 분야')
        st.plotly_chart(fig)  


    # 'Lockheed  Martin Corporation','RTX Corporation','Northrop Grumman Corporation','The Boeing Company','General Dynamics Corporation', 
    #  'BAE Systems','Rostec', 'AVIC', 'NORINCO', 'CETC','L3Harris Technologies'


    with tab3:   
        if choice == 'Lockheed  Martin Corporation':
            year_show()

        if choice == 'RTX Corporation':
            year_show()

        if choice == 'Northrop Grumman Corporation':
            year_show()

        if choice == 'The Boeing Company':
            year_show()

        if choice == 'General Dynamics Corporation':
            year_show()

        if choice == 'BAE Systems':
            year_show()

        if choice == 'Rostec':
            year_show()

        if choice == 'AVIC':
            year_show()

        if choice == 'NORINCO':
            year_show()

        if choice == 'CETC':
            year_show()

        if choice == 'L3Harris Technologies':
            year_show()


    # 해외 기업 좌표 파일 불러오기
    # df = pd.read_excel('data/해외기업좌표.xlsx')
    # m = folium.Map(location=[38.89519981858058, -77.06051835952567], zoom_start=0)
    # marker_cluster = MarkerCluster().add_to(m)


    # # 각 기업 위치에 마커 추가
    # for idx, row in df.iterrows():
    #     name = row['기업명']
    #     lat = row['위도']
    #     lon = row['경도']
    #     homepage=row['홈페이지']
    #     html = f"""
    #     <div style="text-align:center;">
    #          <a href="{homepage}" target="_blank" style="font-weight: bold; font-size: 14px;">
    #             {name}
    #         </a>
    #     </div>
    #     """
    #     popup = folium.Popup(html, max_width=250)
    #     folium.Marker(
    #         location=[lat, lon],
    #         popup=folium.Popup(html, max_width=250)
    #         ).add_to(marker_cluster)
    # st_folium(m, width=600, height=300)
    # st.divider()




# 기업별로 설명 (기업 소개. 주력 분야 및 제품)   

