import streamlit as st 
import pandas as pd
from utils.bar_all import info_show, wordcloud_info
from utils.show_tech_all import show_tech
from utils.pie_com import make_pie_chart
from utils.bar_year_com import make_bar_year
from utils.cumulative_line import kor_cumulative_line, for_cumulative_line
from utils.ipc_scatter import kor_ipc_scatter, for_ipc_scatter

from utils.kor_info import kor_info
from utils.for_info import for_info

from utils_compare.compare import render_comparison_tab

st.set_page_config(
    page_title='안되면 되게 해조',
    page_icon='💡'
)

data = pd.read_csv('data/KIPRIS 전체.csv')
data2 = pd.read_csv('data/WIPO 전체.csv')

ipc = pd.read_excel('data/IPC 분류표.xlsx')
ipc_info_df = pd.read_excel('data/IPC코드설명표.xlsx')

# 연도별 그래프 만들 때 쓰는 데이터 프레임
df = data.copy()
df = df.drop(columns='Unnamed: 0')
df['출원일자'] = pd.to_datetime(df['출원일자'])
df['연도'] = df['출원일자'].dt.year.astype(int)

df2 = data2.copy()
df2 = df2.drop(columns='Unnamed: 0')
df2 = df2.dropna(subset=['출원일자'])
df2['출원일자'] = pd.to_datetime(df2['출원일자'])
df2['연도'] = df2['출원일자'].dt.year.astype(int)

# 기술 분류 selectbox 옵션
tech_options = sorted(df['기술분류'].unique())
options1 = ['전체'] + tech_options

tech_options2 = sorted(df['기술분류'].unique())
options11 = ['전체'] + tech_options2

# 연도 분류 selectbox 옵션
year_options = sorted(df['연도'].unique())
options2 = ['전체'] + year_options

year_options2 = sorted(df['연도'].unique())
options22 = ['전체'] + year_options2


# 세션 상태로 탭 상태를 관리
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = '국내'  # 기본 탭 설정

# 사이드바에서 선택하는 탭
with st.sidebar:
    select_tab = st.selectbox('메뉴', ['국내', '해외', '비교'])

    # 선택된 탭 상태 저장
    if select_tab != st.session_state.selected_tab:
        st.session_state.selected_tab = select_tab

# 탭에 맞는 내용 표시
if st.session_state.selected_tab == '국내':
    with st.sidebar.expander("국내", expanded=True):
        select1 = st.selectbox('분류', options=('기업별', '전체'), key='국내')

    if select1 == '기업별':
        st.title("국내 기업별")
        choice = st.selectbox('기업', ('한화에어로스페이스','한화시스템','현대트랜시스','현대로템','현대위아', '현대인프라코어',
                                'KAI', 'LIG넥스원', '풍산', 'STX엔진','SK오션플랜트'))
        
        tab1, tab2, tab3  = st.tabs(["기업분석","특허기술 분석","연도별 조회"])
        
        with tab1:
            kor_info(choice)
        
        with tab2:
            make_pie_chart(data, choice)
            st.markdown(
    """
    <hr> 
    <p style='text-align: left; font-size: 13px;'>
    [출처] <br>
    <a href='https://www.kipris.or.kr' target='_blank'>특허정보넷 키프리스(KIPRIS)</a><br>
    <a href='https://www.kipo.go.kr/ko/kpoContentView.do?menuCd=SCD0200273' target='_blank'>국가과학기술표준 - IPC, CPC</a>
    </p>
    """,
    unsafe_allow_html=True
)
     
            
        with tab3:
            make_bar_year(data, choice, ipc_info_df)
    
    elif select1 == '전체':
        st.title("국내 전체")
        st.divider()
        tab1, tab2, tab3, tab4 = st.tabs(['수치, 비율', '누적 출원수', 'IPC 산점도', '워드클라우드'])
        with tab1:
            tech = st.selectbox('기술분류 선택', options1)
            year = st.selectbox('연도 선택', options2)
            
            st.divider()
            # 국내 전체 내용 로직
            info_show(df, tech, year, ipc_info_df)

            show_tech(df, tech, year)
            st.markdown(
    """
    <hr> 
    <p style='text-align: left; font-size: 13px;'>
    [출처] <br>
    <a href='https://www.kipris.or.kr' target='_blank'>특허정보넷 키프리스(KIPRIS)</a><br>
    <a href='https://www.kipo.go.kr/ko/kpoContentView.do?menuCd=SCD0200273' target='_blank'>국가과학기술표준 - IPC, CPC</a>
    </p>
    """,
    unsafe_allow_html=True
)
        
        with tab2:
            kor_cumulative_line(df)

        with tab3:
            kor_ipc_scatter(df)

        with tab4:
            k1 = ['자동차_철도차량', '무기센서및제어', '국방플랫폼', '생산기반기술', 
                '정보통신모듈_부품', '건설시공_재료', '로봇_자동화기계', '정보이론', 
                '항공시스템', '디지털방송']

            v1 = ['차량, 회전, 장치, 포함, 시트',
                '신호, 표적, 장치, 수신, 정보',
                '장치, 포함, 발사, 회전, 표적',
                '장치, 포함, 공구, 회전, 형성',
                '신호, 안테나, 주파수, 포함, 장치',
                '제어, 건설, 기계, 포함, 장치',
                '장치, 제어, 포함, 로봇, 위치',
                '데이터, 정보, 장치, 단계, 포함',
                '항공기, 장치, 포함, 비행, 제어',
                '영상, 카메라, 장치, 감시, 방법']
            choice1 = st.selectbox('기술분류 선택 (상위 10개)', k1,
                                key='wordcloud2')
            st.image(f'image1/국내_{choice1}.png', caption=f'{choice1} 워드클라우드', width=700)
            wordcloud_info(choice1, k1, v1 , data)


elif st.session_state.selected_tab == '해외':
    with st.sidebar.expander("해외", expanded=True):
        select2 = st.selectbox('분류', options=('기업별', '전체'), key='해외')

    if select2 == '기업별':
        st.title("해외 기업별")
        choice = st.selectbox('기업', ('Lockheed  Martin Corporation','RTX Corporation','Northrop Grumman Corporation','The Boeing Company','General Dynamics Corporation', 
                                 'BAE Systems','Rostec', 'AVIC', 'NORINCO', 'CETC','L3Harris Technologies'))
        
        tab1, tab2, tab3  = st.tabs(["기업분석","특허기술 분석","연도별 조회"])
        
        with tab1:
            for_info(choice)
            
        with tab2:
            make_pie_chart(data2, choice)
            st.markdown(
    """
    <hr> 
    <p style='text-align: left; font-size: 13px;'>
    [출처] <br>
    <a href='https://www.wipo.int' target='_blank'>WIPO (국제특허기구)</a><br>
    <a href='https://www.kipo.go.kr/ko/kpoContentView.do?menuCd=SCD0200273' target='_blank'>국가과학기술표준 - IPC, CPC</a>
    </p>
    """,
    unsafe_allow_html=True
)
         
            
        with tab3:
            make_bar_year(data2, choice, ipc_info_df)
            

    elif select2 == '전체':
        st.title("해외 전체")
        st.divider()
        tab1, tab2, tab3, tab4 = st.tabs(['수치, 비율', '누적 출원수', 'IPC 산점도', '워드클라우드'])
        with tab1:
            tech = st.selectbox('기술분류 선택', options11)
            year = st.selectbox('연도 선택', options22)
            
            st.divider()
            # 해외 전체 내용 로직
            info_show(df2, tech, year, ipc_info_df)

            show_tech(df2, tech, year)
            st.markdown(
    """
    <hr> 
    <p style='text-align: left; font-size: 13px;'>
    [출처] <br>
    <a href='https://www.wipo.int' target='_blank'>WIPO (국제특허기구)</a><br>
    <a href='https://www.kipo.go.kr/ko/kpoContentView.do?menuCd=SCD0200273' target='_blank'>국가과학기술표준 - IPC, CPC</a>
    </p>
    """,
    unsafe_allow_html=True
)
        
        with tab2:
            for_cumulative_line(df2)
        
        with tab3:
            for_ipc_scatter(df2)
            
        with tab4:
            k2 = ['항공시스템', '생산기반기술', '정보통신모듈_부품', 
                                                '정보이론', '로봇_자동화기계', '자동차_철도차량', 
                                                '천문학', '국방플랫폼', '정밀생산기계', '반도체소자_시스템']
            v2 = ['aircraft, system, control, surface, structure',
                'end, connector, part, structure, contact',
                'frequency, system, antenna, circuit, data',
                'data, system, method, model, invention',
                'system, control, method, device, surface',
                'vehicle, system, end, member, device',
                'fiber, system, device, image, surface',
                'system, device, vehicle, control, invention',
                'material, surface, method, structure, tool',
                'layer, circuit, structure, voltage, device']
            choice2 = st.selectbox('기술분류 선택 (상위 10개)', k2,
                                key='wordcloud2')
            st.image(f'image2/해외_{choice2}.png', caption=f'{choice2} 워드클라우드', width=700)
            wordcloud_info(choice2, k2, v2 , data)

elif st.session_state.selected_tab == '비교':
    render_comparison_tab(df, df2)
