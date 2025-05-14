import pandas as pd
import numpy as np
import streamlit as st


def kor_info(choice):
    st.title(f'{choice}')
    if choice == '한화에어로스페이스':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['항공','방산','해양','IT서비스 등','항공우주','시큐리티','산업용장비'],
            '내용':["항공기 엔진, 부품 생산 및 정비", 
                "군사장비 제조 및 판매, 방산전자 및 유도무기 솔루션",
                "선박 및 특수선 건조, 해양 제품 생산 및 서비스 제공",
                "전산시스템 설계 및 구축, IT 융합 엔지니어링 서비스, 물류 4PL 서비스 ",
                "지구관측 위성시스템 개발 및 생산",
                "CCTV, DVR, NVR, 모니터 생산",
                "칩마운터 등 SMT장비, 반도체장비, 공작기계 생산"]
        })

        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        # st.header('기업 소개')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/한화에어로스페이스 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('사업 개요')
        st.write('''당사 및 종속회사는 고도의 정밀기계분야의 핵심기술을 바탕으로 
                국내외에서 항공기 가스터빈 엔진 및 구성품, 자주포, 장갑차, 조선 및 해양 제품, 
                우주발사체, 위성시스템 등의 생산 및 판매와 IT기술을 활용한 서비스 제공을 주요 사업으로 하고 있습니다.''')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)

    if choice == '한화시스템':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':["방산","ICT","기타"],
            '내용':["군사장비(방산품)의 제조 및 판매 제조업",
                "IT 아웃소싱 등 서비스 판매",
                "제조업, 신사업기술자, 자료처리업, 응용소프트웨어 공급,IT서비스업, 정보통신업, 선박의 건조 및 판매"]
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.header('사업 개요')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/한화시스템 로고.png', caption=f'{choice} 로고', width=400)
        st.subheader('사업 개요')
        st.write('[방산부문] 방산부문은 방산전자 분야 핵심기술을 바탕으로 군사장비(방산품)의 개발, 생산 및 판매를 주요 사업으로 영위하고 있습니다. [ICT부문] ICT부문은 기업의 전산 시스템을 구축(SI), 유지보수(ITO)하는 서비스 사업을 영위하고 있습니다.')
        st.divider()
        # 주요 사업 내용 표시
        st.header('주요 사업 내용')
        st.dataframe(df)

    if choice == '현대트랜시스':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['차량 부품'],
            '내용':["상용 변속기, 상용 액슬, 승용 변속기, 승용 액슬, 시트 제작 및 판매"]
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/현대트랜시스 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('사업 개요')
        st.write('당사는 자동차의 파워트레인과 시트의 제조 및 판매를 주된 사업으로 영위하고 있습니다.')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)

    
    if choice == '현대로템':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':["디펜스솔루션 부문","에코플랜트 부문", "레일솔루션 부문"],
            '내용':["방산물자", "전동차 내수, 수출","제철프레스환경운반설비"]
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/현대로템 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('사업 개요')
        st.write('현대로템은 1999년 설립되어 K계열 전차와 차륜형장갑차 양산사업, 창정비 사업 등을 수행하는 디펜스솔루션 사업, 국가 기간산업인 철도차량 제작, E&M (Electrical & Mechanical) 및 O&M (Operation & Maintenance) 등을 영위하고 있는 레일솔루션 사업, 그리고 제철설비와 완성차 생산설비, 스마트팩토리 설비 및 수소인프라 설비 등을 납품하는 에코플랜트 사업을 영위하고 있습니다.')
        st.divider()
        # 주요 사업 내용 표시
        st.header('주요 사업 내용')
        st.dataframe(df)

    if choice == '현대위아':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':["모빌리티","모빌리티 솔루션","공작기계(중단영업)", "특수"],
            '내용':["모듈부품, 4WD 부품,등속조인트,엔진,열관리부품", 
                "공장자동화 설비 등",
                "공작기계 등",
                    "방산제품 등"]
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/현대위아 로고 .png', caption=f'{choice} 로고', width=400)
        st.divider()
        st.subheader('사업 개요')
        st.write('당사는 자동차 부품의 기초 소재 가공에서부터 엔진, 모듈, 등속조인트, 4WD 부품 등 자동차 핵심부품 자체생산을 통해 축적된 기술력을 바탕으로 고품질 자동차 생산을 위한 자동차부품 전문 생산업체로 자리매김하였습니다.')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)

    if choice == '현대인프라코어': 
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':["건설기계", "엔진"],
            '내용':["굴착기, 휠로더", 
                "엔진, 발전기, A/S부품"]
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.header('사업 개요')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/HD현대인프라코어 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('소개 내용')
        st.write('당사는 2023년 3월 사명을 HD현대인프라코어 주식회사로 변경하였고, 건설중장비, 엔진 등을 생산 판매하는 사업을 영위하고 있습니다.')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)

    
    if choice == 'KAI':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['고정익', '회전익', '기체', '기타'],
            '내용':['T-50계열(T-50, FA-50 등), KF-21계열, KT-1계열 등',
            'KUH/LAH계열 등 ',
            'Boeing, Airbus 등의 기체구조물 등', 
            '위성, UAV, 훈련체계 등 ']
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.header('사업 개요')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/KAI 로고 .png', caption=f'{choice} 로고', width=400)
        st.subheader('소개 내용')
        st.write('당사와 종속회사는 항공기, 우주선, 위성체, 발사체 및 동 부품에 대한 설계, 제조, 판매, 정비 등의 사업을 영위하고 있습니다. 군수사업의 대부분은 내수로 구성되며 수요자인 한국정부(방위사업청)와 계약을 통해 제품(군용기)의 연구개발, 생산, 성능개량, 후속지원 등을 수행하고 있습니다.')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)
    
    if choice == 'LIG넥스원':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['PGM' , 'ISR', 'AEW', 'C4I' , '기타'],
            '내용':['대공, 대함/대장, 대지, 공대지, 수중무기',
                '탐색, 추적, 영상 레이더, 전자광학장비, 수중감시체계', 
                '항공전자, 함정용/항공기용 전자전, 육군용 전자전',
                '통신단말, 지상/함정 전투체계, Data Link 망관리',
                '무인화, 미래전 무기체계, Cyber전']
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.header('사업 개요')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/LIG 넥스원 로고.png', caption=f'{choice} 로고', width=400)
        st.subheader('소개 내용')
        st.write('당사는 방위사업청, 국방과학연구소, 국방기술품질원 등과의 긴밀한 공조를 기반으로 정밀유도무기, 감시정찰, 지휘통제·통신, 항공전자, 전자전에 이르는 다양한 첨단 무기체계를 연구, 개발 및 양산 해 온 대한민국을 대표하는 종합방위산업체입니다')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)

    
    if choice == '풍산':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['신동부문' , '방산부문'],
            '내용':['산업용 소재', '군용탄, 스포츠탄']
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.header('사업 개요')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/풍산 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('소개 내용')
        st.write('당사 및 연결회사는 신동사업 부문과 방산사업 부문으로 크게 나눌 수 있습니다. 신동사업 부문에서는 동 및 동합금 판ㆍ대, 리드프레임 소재, 봉ㆍ선, 주화용 소전 등을 생산하고 있으며, 방산사업 부문에서는 소구경에서부터 대구경까지 이르는 각종 군용 탄약과 스포츠용 탄약, 추진화약 및 탄약 부분품, 정밀 단조품 등을 생산하고 있습니다. 또한 신규 Alloy, 탄약 기능 개발과 새로운 분야인 전투드론 개발을 위해 지속적인 연구개발을 추진하고 있습니다.')
        st.divider()
        # 주요 사업 내용 표시시
        st.header('주요 사업 내용')
        st.dataframe(df)


    if choice == 'STX엔진':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['민수사업', '특수사업','전자통신'],
            '내용':['해상 선박용 엔진', 
                '전차, 자주포, 구축함, 경비정, 고속정 엔진',
                '탐지장비, 군위성통신 전투체계']
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/STX 엔진 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('사업 개요')
        st.write('당사는 디젤엔진 전문생산업체로 출범하여 엔진, 전자통신, 부품/서비스 사업을 중심으로 하는 엔진, 중전기 종합 회사입니다.')
        st.divider()
        # 주요 사업 내용 표시
        st.header('주요 사업 내용')
        st.dataframe(df)


    if choice == 'SK오션플랜트':
        # 사업 내용 데이터프레임
        df = pd.DataFrame({
            '부문':['해상풍력', '플랜트','특수선','후육강관','조선','수리개조','기타'],
            '내용':['해상풍력 구조물',
                '해양/육상 플랜트',
                '방산 및 관공선 건조',
                '해양/건축구조용 파이프',
                '신조선 건조 및 블록 제작',
                '선박 수리/개조 및 정기검사 ',
                '용역 및 상품']
        })
        
        df = df.set_index('부문')
        # 기업 로고, 소개 내용
        st.header('사업 개요')
        st.divider()
        con = st.container(border=True)
        with con:
            col1, col2, col3 = st.columns([1,4,1])
            with col2:
                st.image('image1/SK 오션플랜트 로고.jpg', caption=f'{choice} 로고', width=400)
        st.subheader('소개 내용')
        st.write('당사는 경상남도 고성군에 위치한 본사를 거점으로 1개의 생산기지와 2개의 가공공장, 기술교육원, 서울, 중국, 베트남 법인사무소를 운영하고 있습니다. 당사 및 당사의 종속기업은 해상풍력 하부구조물, 해양플랜트, 특수선 건조, 후육강관, 조선, 선박 수리/개조를 영위하는 해상풍력·조선·해양 전문 기업입니다.')
        st.divider()
        # 주요 사업 내용 표시
        st.header('주요 사업 내용')
        st.dataframe(df)