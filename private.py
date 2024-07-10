import requests
import streamlit as st
import pandas as pd
import datetime
import pytz

st.set_page_config(
    page_title="saloa.gg",
    page_icon="😊",
    layout="wide",
)

headers = {
            'accept': 'application/json',
            'authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAwODc4NTYifQ.Kz1Q31XCxpow-7vQUhjx8sejfVuQHi0T7BLfVoIXd4LErYMYJZ82oc9PX3Ls19rVxgvnNrwnpu2a2Ctg3vX8qO0214NgAh1Ab8M2hPPEksai7LY2enjhBGu7nvs8Ic9eq43p4DiGlpHQ68zZBbTo1WFbumayIrWkVAD-m7AHbkuguM0pMuXv8qL7ar6ZR-vVUsOetOuAannv6OpFhss3db1n4PuJM6S1TPyo2-Uo6T2FTp5Ue9C8TmIFnj97ZESorEU5KttbZ9qkL8yYnsK1A6glbYQksGMkCS0zQCp87BRQPccKAw41WlybHWcdjU3Zz3iDtMmQ5zv0GI_s0tzEmQ',
            'Content-Type': 'application/json',
            }


json_auction = {
    'ItemLevelMin': 0,
    'ItemLevelMax': 1700,
    'ItemGradeQuality': 0,
    'Sort': 'BUY_PRICE',
    'CategoryCode': 210000,
    'CharacterClass': '',
    'ItemTier': 3,
    'ItemGrade': '희귀',
    'ItemName': '3레벨',
    'PageNo': 0,
    'SortCondition': 'ASC',
}

response_auction = requests.post('https://developer-lostark.game.onstove.com/auctions/items', headers=headers, json=json_auction)
content_auction = response_auction.json()
item_list = content_auction['Items']

@st.cache_data
def database():
    data_name = []
    data_price = []
    update_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    
    dic = {'재련재료':50000,'배틀아이템':60000,'생활':90000} 
    for value in dic.values():
        for t in range(1,10) :
            json_market = {
            'Sort': '',
            'CategoryCode': value,
            'CharacterClass': '',
            'ItemTier': 0,
            'ItemGrade': '',
            'ItemName': '' ,
            'PageNo': t,
            'SortCondition': 'ASC',
            }
            try:
                response_market =requests.post('https://developer-lostark.game.onstove.com/markets/items', headers=headers, json=json_market)
                content_market = response_market.json()
                item = content_market['Items']
                for i in range(len(item)):
                    data_name.append(item[i]['Name'])
                    data_price.append(item[i]['RecentPrice'])
            except:pass
    data_dict_1 = dict(zip(data_name,data_price))
    data_tuple = (update_time,data_dict_1)
    data_include_time = list(data_tuple)
    return data_include_time

st.title("Saloa")


reset_1 = st.button('데이터 최신화')
if reset_1 :
    st.cache_data.clear()
else:pass


time_gap = datetime.datetime.now(pytz.timezone('Asia/Seoul')) - database()[0]
time_check = time_gap/datetime.timedelta(minutes=3)
       
st.write('Data load : ',database()[0].strftime('%m.%d - %H:%M:%S'))
minute = time_gap.total_seconds()/60
st.write('{}분 전에 최신화되었습니다.'.format(int(minute)))


def price(args):
    return database()[1][args]
def charge(args):
    for n in range(0,database()[1][args]):
        if n+1>=database()[1][args]*0.05>n:
            return n+1
        
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['최상급 오레하 제작','아비도스 제작','배틀아이템 공장','컨텐츠 손익','패키지 효율','경매 입찰가격'])

with tab1:
    st.write('최상급 오레하 융화 재료 가격 : ',price('최상급 오레하 융화 재료'),'골드')
    st.write('제작 수수료 기준 : ',int(276),'골드')
    slide_option_1 = (price('최상급 오레하 융화 재료')-2,price('최상급 오레하 융화 재료')-1,price('최상급 오레하 융화 재료'),price('최상급 오레하 융화 재료')+1,price('최상급 오레하 융화 재료')+2)
    oreha_value_1 = st.selectbox('최상급 오레하 판매 가격',slide_option_1,index=2)
    for n in range(0,oreha_value_1):
        if n+1>=oreha_value_1*0.05>n:
            oreha_charge = n+1

    col3, col4 = st.columns(2)
    with col3:
        st.subheader('고고학 제작')
        slide_option_oreha_1 = (price('오레하 유물')-2,price('오레하 유물')-1,price('오레하 유물'),price('오레하 유물')+1,price('오레하 유물')+2)
        oreha_recipe_blue_1 = st.selectbox('오레하 유물 가격',slide_option_oreha_1,index=2)
        slide_option_oreha_2 = (price('희귀한 유물')-2,price('희귀한 유물')-1,price('희귀한 유물'),price('희귀한 유물')+1,price('희귀한 유물')+2)
        oreha_recipe_green_1 = st.selectbox('희귀한 유물 가격',slide_option_oreha_2,index=2)
        slide_option_oreha_3 = (price('고대 유물')-2,price('고대 유물')-1,price('고대 유물'),price('고대 유물')+1,price('고대 유물')+2)
        oreha_recipe_white_1 = st.selectbox('고대 유물 가격',slide_option_oreha_3,index=2)

        if oreha_recipe_white_1*2 >= oreha_recipe_green_1:
            if oreha_recipe_green_1*2.5/4 >= oreha_recipe_blue_1:
                oreha_legacy = oreha_recipe_blue_1
                oreha_change_tf = '가루 교환 쓰지않음'
            else:
                oreha_legacy = oreha_recipe_green_1*2.5/4
                oreha_change_tf = '가루 교환 사용 (희귀한유물)'
        else:
            if oreha_recipe_white_1*5/4 >= oreha_recipe_blue_1/10:
                oreha_legacy = oreha_recipe_blue_1
                oreha_change_tf = '가루 교환 쓰지않음'
            else:
                oreha_legacy = oreha_recipe_white_1*5/4
                oreha_change_tf = '가루 교환 사용 (고대 유물)'

        recipe_legacy = oreha_legacy*52 + oreha_recipe_green_1*51 + oreha_recipe_white_1*107
        profit_legacy = (oreha_value_1-oreha_charge)*1500-recipe_legacy-27600

        if profit_legacy>=0:
            legacy_result = '1칸 당 '+str(int(profit_legacy/100))+'골드 이득'
        else:
            legacy_result = '만들어 팔면 손해'
        
        legacy_1 = ('오레하 유물 : {}골드, 희귀한 유물 : {}골드, 고대 유물 : {}골드'.format(oreha_recipe_blue_1,oreha_recipe_green_1,oreha_recipe_white_1))
        
        col3.metric(label=legacy_1,value=legacy_result,delta=oreha_change_tf,delta_color='off')
    
    
    with col4:
        st.subheader('낚시 제작')
        slide_option_fish_1 = (price('오레하 태양 잉어')-2,price('오레하 태양 잉어')-1,price('오레하 태양 잉어'),price('오레하 태양 잉어')+1,price('오레하 태양 잉어')+2)
        oreha_recipe_blue_2 = st.selectbox('오레하 태양 잉어 가격',slide_option_fish_1,index=2)
        slide_option_fish_2 = (price('붉은 살 생선')-2,price('붉은 살 생선')-1,price('붉은 살 생선'),price('붉은 살 생선')+1,price('붉은 살 생선')+2)
        oreha_recipe_green_2 = st.selectbox('붉은 살 생선 가격',slide_option_fish_2,index=2)
        slide_option_fish_3 = (price('생선')-2,price('생선')-1,price('생선'),price('생선')+1,price('생선')+2)
        oreha_recipe_white_2 = st.selectbox('생선 가격',slide_option_fish_3,index=2)

        fishing_1 = ('오레하 태양 잉어 : {}골드, 붉은 살 생선 : {}골드, 생선 : {}골드'.format(oreha_recipe_blue_2,oreha_recipe_green_2,oreha_recipe_white_2))
        
        if oreha_recipe_green_2*2.5/4 >= oreha_recipe_blue_2:
            oreha_fishing = oreha_recipe_blue_2
            fishing_2 = '가루 교환 쓰지않음'
        else:
            oreha_fishing = oreha_recipe_green_2*2.5/4
            fishing_2 = '가루 교환 사용'
        recipe_fishing = oreha_fishing*52 + oreha_recipe_green_2*64 + oreha_recipe_white_2*142
        profit_fishing = (oreha_value_1-oreha_charge)*1500 - recipe_fishing -27600
        if profit_fishing >= 0:
            fishing_result = '1칸 당 '+str(int(profit_fishing/100))+' 골드 이득'
        else:
            fishing_result = '만들어 팔면 손해'
        col4.metric(label=fishing_1,value=fishing_result,delta=fishing_2,delta_color='off')

with tab2:
    st.write('아비도스 재료 가격 : ',price('아비도스 융화 재료'),'골드')
    st.write('제작 수수료 기준 : ',int(368),'골드')
    avidos_option_1 = (price('아비도스 융화 재료')-2,price('아비도스 융화 재료')-1,price('아비도스 융화 재료'),price('아비도스 융화 재료')+1,price('아비도스 융화 재료')+2)
    avidos_value_1 = st.selectbox('아비도스 융화 재료 판매 가격',avidos_option_1,index=2)
    for n in range(0,avidos_value_1):
        if n+1>=avidos_value_1*0.05>n:
            avidos_charge_1 = n+1


    st.subheader('고고학 제작')
    avidos_list_legacy = ('아비도스 유물 : {}골드, 희귀한 유물 : {}골드, 고대 유물 : {}골드'.format(price('아비도스 유물'),price('희귀한 유물'),price('고대 유물')))
    if price('희귀한 유물')*2.5/4 >= price('아비도스 유물'):
        avidos_legacy = price('아비도스 유물')
        avidos_legacy_change = '가루 교환 쓰지않음'
    else:
        avidos_legacy = price('희귀한 유물')*2.5/4
        avidos_legacy_change = '가루 교환 사용'
    avidos_recipe_legacy = avidos_legacy*33 + price('희귀한 유물')*45 + price('고대 유물')*86
    avidos_legacy_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_legacy-36800

    if avidos_legacy_profit>=0:
        avidos_legacy_result = '1칸 당 '+str(int(avidos_legacy_profit/100))+'골드 이득'
    else:
        avidos_legacy_result = '만들어 팔면 손해'
    
    st.metric(label=avidos_list_legacy,value=avidos_legacy_result,delta=avidos_legacy_change,delta_color='off')


    st.subheader('채집 제작')
    avidos_list_flower = ('아비도스 들꽃 : {}골드, 수줍은 들꽃 : {}골드, 들꽃 : {}골드'.format(price('아비도스 들꽃'),price('화사한 들꽃'),price('들꽃')))
    if price('화사한 들꽃')*2.5/4 >= price('아비도스 들꽃'):
        avidos_flower = price('아비도스 들꽃')
        avidos_flower_change = '가루 교환 쓰지않음'
    else:
        avidos_legacy = price('화사한 들꽃')*2.5/4
        avidos_flower_change = '가루 교환 사용'
    avidos_recipe_legacy = avidos_legacy*33 + price('화사한 들꽃')*45 + price('들꽃')*86
    avidos_legacy_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_legacy-36800

    if avidos_legacy_profit>=0:
        avidos_legacy_result = '1칸 당 '+str(int(avidos_legacy_profit/100))+'골드 이득'
    else:
        avidos_legacy_result = '만들어 팔면 손해'
    
    st.metric(label=avidos_list_flower,value=avidos_legacy_result,delta=avidos_flower_change,delta_color='off')
    

with tab3:
    '''
    st.subheader('정령의 회복약')
    st.write('정령의 회복약 가격 : ',price('정령의 회복약'),'골드')
    battle_1 = (price('정령의 회복약')-charge('정령의 회복약'))*30 - (price('화사한 들꽃')*6 + price('수줍은 들꽃')*24 + price('들꽃')*5 + 260)
    if battle_1 >= 0:
        st.write('정령의 회복약 : 제작 1칸 당 ',int(battle_1/10),' 골드 이득')
    else:
        st.warning('정령의 회복약 제작 : 손해')
    
    st.subheader('각성 물약')
    st.write('각성 물약 : ',price('각성 물약'),'골드')
    battle_2 = (price('각성 물약')-charge('각성 물약'))*30 - (price('화려한 버섯')*5 + price('싱싱한 버섯')*20 + price('튼튼한 목재')*2 + price('희귀한 유물')*4 + price('투박한 버섯')*4 + 260)
    if battle_2 >= 0:
        st.write('각성 물약 : 제작 1칸 당 ',battle_2/10,' 골드 이득')
    else:
        st.warning('각성 물약 제작 : 손해')

    st.subheader('아드로핀 물약')
    st.write('아드로핀 물약 : ',price('아드로핀 물약'),'골드')
    battle_3 = (price('아드로핀 물약')-charge('아드로핀 물약'))*30 - (price('화사한 들꽃')*6 + price('수줍은 들꽃')*24 + price('단단한 철광석')*2+price('희귀한 유물')*2 + price('들꽃')*5 + 260)
    if battle_3 >= 0:
        st.write('아드로핀 물약 : 제작 1칸 당 ',battle_3/10,' 골드 이득')
    else:
        st.warning('아드로핀 물약 제작 : 손해')    
    
    st.subheader('파괴 폭탄')
    st.write('파괴 폭탄 : ',price('파괴 폭탄'),'골드')
    battle_4 = (price('파괴 폭탄')-charge('파괴 폭탄'))*30 - (price('화려한 버섯')*4+price('싱싱한 버섯')*12+price('묵직한 철광석')*6+price('투박한 버섯')*3.2 + 140)
    if battle_4 >= 0:
        st.write('파괴 폭탄 : 제작 1칸 당 ',battle_4/10,' 골드 이득')
    else:
        st.warning('파괴 폭탄 제작 : 손해')
        

    st.subheader('암흑 수류탄')
    st.write('암흑 수류탄 : ',price('암흑 수류탄'),'골드')
    battle_5 = (price('암흑 수류탄')-charge('암흑 수류탄'))*30 - (price('화려한 버섯')*3+price('싱싱한 버섯')*12+price('부드러운 목재')*3+price('투박한 버섯')*2.4 + 140)
    if battle_5 >= 0:
        st.write('암흑 수류탄 : 제작 1칸 당 ',battle_5/10,' 골드 이득')
    else:
        st.warning('암흑 수류탄 제작 : 손해')

    st.subheader('성스러운 부적')
    st.write('성스러운 부적 : ',price('성스러운 부적'),'골드')
    battle_6 = (price('성스러운 부적')-charge('성스러운 부적'))*30 - (price('화려한 버섯')*3+price('싱싱한 버섯')*18+price('투박한 버섯')*3 + 140)
    if battle_6 >= 0:
        st.write('성스러운 부적 : 제작 1칸 당 ',battle_6/10,' 골드 이득')
    else:
        st.warning('성스러운 부적 제작 : 손해')

    st.subheader('빛나는 성스러운 부적')
    st.write('빛나는 성스러운 부적 : ',price('빛나는 성스러운 부적'),'골드')
    battle_7 = (price('빛나는 성스러운 부적')-charge('빛나는 성스러운 부적'))*20 - (price('성스러운 부적')*30 + price('화려한 버섯')*3 + 140)
    if battle_7 >= 0:
        st.write('빛나는 성스러운 부적 : 제작 1칸 당 ',battle_7/10,' 골드 이득')
    else:
        st.warning('빛나는 성스러운 부적 제작 : 손해')
    '''
        
with tab4:
    select_reward = st.multiselect('필요한 재료 선택',('클리어 골드','명예의 파편','찬란한 명예의 돌파석','정제된 파괴강석','정제된 수호강석','혼돈의 돌'),['클리어 골드','명예의 파편','찬란한 명예의 돌파석','정제된 파괴강석','정제된 수호강석','혼돈의 돌'])
    if '정제된 수호강석' in select_reward:
        price_pr_1 = st.number_input('지역채팅 한 덩이(9999개) 가격',value=1500)
    raid = st.selectbox('컨텐츠',('아브렐슈드 하드','카양겔 하드','일리아칸 노말','일리아칸 하드','혼돈의 상아탑 노말','혼돈의 상아탑 하드','카멘 노말','카멘 하드','에키드나 노말','에키드나 하드'))
    
    if '명예의 파편' in select_reward:
        price_sh = price('명예의 파편 주머니(대)')/1500
    else:
        price_sh = 0
    
    if '찬란한 명예의 돌파석' in select_reward:
        price_st = price('찬란한 명예의 돌파석')
    else:
        price_st = 0

    if '정제된 파괴강석' in select_reward:
        price_de = price('정제된 파괴강석')/10
    else:
        price_de = 0

    if '정제된 수호강석' in select_reward:
        price_pr_2 = price_pr_1/10000
    else:
        price_pr_2 = 0

    if '혼돈의 돌' in select_reward:
        price_ch = 500
    else:
        price_ch = 0


    #레이드 종류

    if '아브렐슈드 하드' not in st.session_state:
        st.session_state['아브렐슈드 하드'] = ['아브렐슈드 하드1관문','아브렐슈드 하드2관문','아브렐슈드 하드3관문','아브렐슈드 하드4관문']

    if '카양겔 하드' not in st.session_state:
        st.session_state['카양겔 하드'] = ['카양겔 하드1관문','카양겔 하드2관문','카양겔 하드3관문']

    if '일리아칸 노말' not in st.session_state:
        st.session_state['일리아칸 노말'] = ['일리아칸 노말1관문','일리아칸 노말2관문','일리아칸 노말3관문']

    if '일리아칸 하드' not in st.session_state:
        st.session_state['일리아칸 하드'] = ['일리아칸 하드1관문','일리아칸 하드2관문','일리아칸 하드3관문']

    if '혼돈의 상아탑 노말' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말'] = ['혼돈의 상아탑 노말1관문','혼돈의 상아탑 노말2관문','혼돈의 상아탑 노말3관문','혼돈의 상아탑 노말4관문']

    if '혼돈의 상아탑 하드' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드'] = ['혼돈의 상아탑 하드1관문','혼돈의 상아탑 하드2관문','혼돈의 상아탑 하드3관문','혼돈의 상아탑 하드4관문']

    if '카멘 노말' not in st.session_state:
        st.session_state['카멘 노말'] = ['카멘 노말1관문','카멘 노말2관문','카멘 노말3관문']
    
    if '카멘 하드' not in st.session_state:
        st.session_state['카멘 하드'] = ['카멘 하드1관문','카멘 하드2관문','카멘 하드3관문','카멘 하드4관문']

    if '에키드나 노말' not in st.session_state:
        st.session_state['에키드나 노말'] = ['에키드나 노말1관문','에키드나 노말2관문']
    
    if '에키드나 하드' not in st.session_state:
        st.session_state['에키드나 하드'] = ['에키드나 하드1관문','에키드나 하드2관문']

    #레이드 보상

    if '아브렐슈드 하드1관문' not in st.session_state:
        st.session_state['아브렐슈드 하드1관문'] = {'컨텐츠 보상':{'명예의 파편':2500,'정제된 파괴강석':56,'정제된 수호강석':112,'찬란한 명예의 돌파석':0,'혼돈의 돌':1.2,'클리어 골드':2000},'더보기':{'명예의 파편':3000,'정제된 파괴강석':52,'정제된 수호강석':104,'찬란한 명예의 돌파석':2.4,'혼돈의 돌':1.2,'더보기 골드':700}}

    if '아브렐슈드 하드2관문' not in st.session_state:
        st.session_state['아브렐슈드 하드2관문'] = {'컨텐츠 보상':{'명예의 파편':2500,'정제된 파괴강석':64,'정제된 수호강석':128,'찬란한 명예의 돌파석':0,'혼돈의 돌':0.8,'클리어 골드':2000},'더보기':{'명예의 파편':4000,'정제된 파괴강석':84,'정제된 수호강석':168,'찬란한 명예의 돌파석':3.2,'혼돈의 돌':1.2,'더보기 골드':900}}
    
    if '아브렐슈드 하드3관문' not in st.session_state:
        st.session_state['아브렐슈드 하드3관문'] = {'컨텐츠 보상':{'명예의 파편':3000,'정제된 파괴강석':80,'정제된 수호강석':160,'찬란한 명예의 돌파석':0,'혼돈의 돌':3.4,'클리어 골드':2000},'더보기':{'명예의 파편':4000,'정제된 파괴강석':128,'정제된 수호강석':256,'찬란한 명예의 돌파석':4.8,'혼돈의 돌':1.4,'더보기 골드':1100}}

    if '아브렐슈드 하드4관문' not in st.session_state:
        st.session_state['아브렐슈드 하드4관문'] = {'컨텐츠 보상':{'명예의 파편':6000,'정제된 파괴강석':160,'정제된 수호강석':320,'찬란한 명예의 돌파석':0,'혼돈의 돌':7,'클리어 골드':3000},'더보기':{'명예의 파편':10000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':8,'혼돈의 돌':2,'더보기 골드':1800}}

    if '카양겔 하드1관문' not in st.session_state:
        st.session_state['카양겔 하드1관문'] = {'컨텐츠 보상':{'명예의 파편':2500,'정제된 파괴강석':80,'정제된 수호강석':160,'찬란한 명예의 돌파석':0,'혼돈의 돌':0.2,'클리어 골드':1000},'더보기':{'명예의 파편':1500,'정제된 파괴강석':70,'정제된 수호강석':140,'찬란한 명예의 돌파석':3,'혼돈의 돌':0.2,'더보기 골드':700}}

    if '카양겔 하드2관문' not in st.session_state:
        st.session_state['카양겔 하드2관문'] = {'컨텐츠 보상':{'명예의 파편':3500,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':0,'혼돈의 돌':0.2,'클리어 골드':2000},'더보기':{'명예의 파편':2000,'정제된 파괴강석':90,'정제된 수호강석':180,'찬란한 명예의 돌파석':4,'혼돈의 돌':0.2,'더보기 골드':900}}
        
    if '카양겔 하드3관문' not in st.session_state:
        st.session_state['카양겔 하드3관문'] = {'컨텐츠 보상':{'명예의 파편':5000,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':0,'혼돈의 돌':5.6,'클리어 골드':3000},'더보기':{'명예의 파편':2500,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':6,'혼돈의 돌':0.6,'더보기 골드':1100}}

    if '일리아칸 노말1관문' not in st.session_state:
        st.session_state['일리아칸 노말1관문'] = {'컨텐츠 보상':{'명예의 파편':3000,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':6,'혼돈의 돌':0.6,'클리어 골드':1500},'더보기':{'명예의 파편':3000,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':6,'혼돈의 돌':0.6,'더보기 골드':900}}

    if '일리아칸 노말2관문' not in st.session_state:
        st.session_state['일리아칸 노말2관문'] = {'컨텐츠 보상':{'명예의 파편':3000,'정제된 파괴강석':160,'정제된 수호강석':320,'찬란한 명예의 돌파석':8,'혼돈의 돌':0.6,'클리어 골드':2000},'더보기':{'명예의 파편':3000,'정제된 파괴강석':160,'정제된 수호강석':320,'찬란한 명예의 돌파석':8,'혼돈의 돌':0.6,'더보기 골드':1100}}
    
    if '일리아칸 노말3관문' not in st.session_state:
        st.session_state['일리아칸 노말3관문'] = {'컨텐츠 보상':{'명예의 파편':4200,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':8,'혼돈의 돌':1,'클리어 골드':4000},'더보기':{'명예의 파편':4200,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':8,'혼돈의 돌':1,'더보기 골드':1500}}

    if '일리아칸 하드1관문' not in st.session_state:
        st.session_state['일리아칸 하드1관문'] = {'컨텐츠 보상':{'명예의 파편':4000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':9,'혼돈의 돌':1.4,'클리어 골드':1750},'더보기':{'명예의 파편':4000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':9,'혼돈의 돌':1.4,'더보기 골드':1200}}

    if '일리아칸 하드2관문' not in st.session_state:
        st.session_state['일리아칸 하드2관문'] = {'컨텐츠 보상':{'명예의 파편':4000,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':12,'혼돈의 돌':1.4,'클리어 골드':2500},'더보기':{'명예의 파편':4000,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':12,'혼돈의 돌':1.4,'더보기 골드':1400}}
    
    if '일리아칸 하드3관문' not in st.session_state:
        st.session_state['일리아칸 하드3관문'] = {'컨텐츠 보상':{'명예의 파편':5500,'정제된 파괴강석':360,'정제된 수호강석':720,'찬란한 명예의 돌파석':18,'혼돈의 돌':1.6,'클리어 골드':5750},'더보기':{'명예의 파편':5500,'정제된 파괴강석':360,'정제된 수호강석':720,'찬란한 명예의 돌파석':18,'혼돈의 돌':1.6,'더보기 골드':1900}}

    if '혼돈의 상아탑 노말1관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말1관문'] = {'컨텐츠 보상':{'명예의 파편':1500,'정제된 파괴강석':80,'정제된 수호강석':160,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'선명한 지혜의 기운':2,'클리어 골드':1500},'더보기':{'명예의 파편':3000,'정제된 파괴강석':100,'정제된 수호강석':200,'찬란한 명예의 돌파석':2,'혼돈의 돌':0,'선명한 지혜의 기운':2,'더보기 골드':700}}

    if '혼돈의 상아탑 노말2관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말2관문'] = {'컨텐츠 보상':{'명예의 파편':1500,'정제된 파괴강석':80,'정제된 수호강석':160,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'선명한 지혜의 기운':2,'클리어 골드':1750},'더보기':{'명예의 파편':3000,'정제된 파괴강석':100,'정제된 수호강석':200,'찬란한 명예의 돌파석':2,'혼돈의 돌':0,'선명한 지혜의 기운':2,'더보기 골드':800}}

    if '혼돈의 상아탑 노말3관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말3관문'] = {'컨텐츠 보상':{'명예의 파편':2000,'정제된 파괴강석':100,'정제된 수호강석':200,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'선명한 지혜의 기운':3,'클리어 골드':2500},'더보기':{'명예의 파편':3000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':2,'혼돈의 돌':0,'선명한 지혜의 기운':3,'더보기 골드':900}}

    if '혼돈의 상아탑 노말4관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말4관문'] = {'컨텐츠 보상':{'명예의 파편':2000,'정제된 파괴강석':100,'정제된 수호강석':200,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'선명한 지혜의 기운':1,'선명한 지혜의 엘릭서':1,'클리어 골드':3250},'더보기':{'명예의 파편':4500,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':3,'혼돈의 돌':0,'선명한 지혜의 기운':1,'선명한 지혜의 엘릭서':1,'더보기 골드':1100}}

    elixer = price('빛나는 지혜의 정수')*6*0.95-250

    if '혼돈의 상아탑 하드1관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드1관문'] = {'컨텐츠 보상':{'명예의 파편':1800,'정제된 파괴강석':100,'찬란한 명예의 돌파석':0,'정제된 수호강석':200,'혼돈의 돌':0,'클리어 골드':2000-elixer/2},'더보기':{'명예의 파편':4000,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':3,'혼돈의 돌':0,'더보기 골드':1000-elixer/2}}

    if '혼돈의 상아탑 하드2관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드2관문'] = {'컨텐츠 보상':{'명예의 파편':1800,'정제된 파괴강석':100,'찬란한 명예의 돌파석':0,'정제된 수호강석':200,'혼돈의 돌':0,'클리어 골드':2500-elixer/2},'더보기':{'명예의 파편':4000,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':3,'혼돈의 돌':0,'더보기 골드':1000-elixer/2}}

    if '혼돈의 상아탑 하드3관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드3관문'] = {'컨텐츠 보상':{'명예의 파편':2400,'정제된 파괴강석':120,'찬란한 명예의 돌파석':0,'정제된 수호강석':240,'혼돈의 돌':0,'클리어 골드':4000-elixer*3/4},'더보기':{'명예의 파편':5000,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':5,'혼돈의 돌':0,'더보기 골드':1500-elixer*3/4}}

    if '혼돈의 상아탑 하드4관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드4관문'] = {'컨텐츠 보상':{'명예의 파편':2400,'정제된 파괴강석':120,'찬란한 명예의 돌파석':0,'정제된 수호강석':240,'혼돈의 돌':0,'클리어 골드':6000-elixer/4-price('빛나는 지혜의 정수')*6},'더보기':{'명예의 파편':5500,'정제된 파괴강석':300,'정제된 수호강석':600,'찬란한 명예의 돌파석':7,'혼돈의 돌':0,'더보기 골드':2000-elixer/4-price('빛나는 지혜의 정수')*6}}

    if '카멘 노말1관문' not in st.session_state:
        st.session_state['카멘 노말1관문'] = {'컨텐츠 보상':{'명예의 파편':2000,'정제된 파괴강석':100,'정제된 수호강석':200,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':3500},'더보기':{'명예의 파편':3500,'정제된 파괴강석':380,'정제된 수호강석':760,'찬란한 명예의 돌파석':13,'혼돈의 돌':0,'더보기 골드':1500}}

    if '카멘 노말2관문' not in st.session_state:
        st.session_state['카멘 노말2관문'] = {'컨텐츠 보상':{'명예의 파편':2500,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':4000},'더보기':{'명예의 파편':4500,'정제된 파괴강석':450,'정제된 수호강석':900,'찬란한 명예의 돌파석':16,'혼돈의 돌':0,'더보기 골드':1800}}

    if '카멘 노말3관문' not in st.session_state:
        st.session_state['카멘 노말3관문'] = {'컨텐츠 보상':{'명예의 파편':3000,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':5500},'더보기':{'명예의 파편':6000,'정제된 파괴강석':600,'정제된 수호강석':1200,'찬란한 명예의 돌파석':20,'혼돈의 돌':0,'더보기 골드':2500}}

    if '카멘 하드1관문' not in st.session_state:
        st.session_state['카멘 하드1관문'] = {'컨텐츠 보상':{'명예의 파편':2400,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':5000},'더보기':{'명예의 파편':5000,'정제된 파괴강석':500,'정제된 수호강석':1000,'찬란한 명예의 돌파석':15,'혼돈의 돌':0,'더보기 골드':2000}}

    if '카멘 하드2관문' not in st.session_state:
        st.session_state['카멘 하드2관문'] = {'컨텐츠 보상':{'명예의 파편':3000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':6000},'더보기':{'명예의 파편':6000,'정제된 파괴강석':600,'정제된 수호강석':1200,'찬란한 명예의 돌파석':21,'혼돈의 돌':0,'더보기 골드':2400}}

    if '카멘 하드3관문' not in st.session_state:
        st.session_state['카멘 하드3관문'] = {'컨텐츠 보상':{'명예의 파편':3600,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':9000},'더보기':{'명예의 파편':7500,'정제된 파괴강석':700,'정제된 수호강석':1400,'찬란한 명예의 돌파석':27,'혼돈의 돌':0,'더보기 골드':2800}}
    
    if '카멘 하드4관문' not in st.session_state:
        st.session_state['카멘 하드4관문'] = {'컨텐츠 보상':{'명예의 파편':4500,'정제된 파괴강석':300,'정제된 수호강석':600,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':21000},'더보기':{'명예의 파편':9000,'정제된 파괴강석':850,'정제된 수호강석':1700,'찬란한 명예의 돌파석':34,'혼돈의 돌':0,'더보기 골드':3600}}

    if '에키드나 노말1관문' not in st.session_state:
        st.session_state['에키드나 노말1관문'] = {'컨텐츠 보상':{'명예의 파편':3600,'정제된 파괴강석':160,'정제된 수호강석':200,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':5000},'더보기':{'명예의 파편':6500,'정제된 파괴강석':450,'정제된 수호강석':760,'찬란한 명예의 돌파석':16,'혼돈의 돌':0,'더보기 골드':2200}}

    if '에키드나 노말2관문' not in st.session_state:
        st.session_state['에키드나 노말2관문'] = {'컨텐츠 보상':{'명예의 파편':4200,'정제된 파괴강석':220,'정제된 수호강석':440,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':9500},'더보기':{'명예의 파편':9500,'정제된 파괴강석':800,'정제된 수호강석':1600,'찬란한 명예의 돌파석':28,'혼돈의 돌':0,'더보기 골드':3400}}

    if '에키드나 하드1관문' not in st.session_state:
        st.session_state['에키드나 하드1관문'] = {'컨텐츠 보상':{'명예의 파편':4000,'정제된 파괴강석':220,'정제된 수호강석':440,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':6000},'더보기':{'명예의 파편':7500,'정제된 파괴강석':650,'정제된 수호강석':1300,'찬란한 명예의 돌파석':28,'혼돈의 돌':0,'더보기 골드':2800}}

    if '에키드나 하드2관문' not in st.session_state:
        st.session_state['에키드나 하드2관문'] = {'컨텐츠 보상':{'명예의 파편':5400,'정제된 파괴강석':280,'정제된 수호강석':560,'찬란한 명예의 돌파석':0,'혼돈의 돌':0,'클리어 골드':12500},'더보기':{'명예의 파편':11000,'정제된 파괴강석':950,'정제된 수호강석':1900,'찬란한 명예의 돌파석':38,'혼돈의 돌':0,'더보기 골드':4100}}

    raid_name = st.session_state[raid]
    df_list = []
    df_reward = []
    for i in range(0,len(raid_name)):
        raid_gate = raid_name[i]
        raid_reward = st.session_state[raid_gate]['컨텐츠 보상']
        raid_reward_plus = st.session_state[raid_gate]['더보기']
        if '클리어 골드' in select_reward:
            reward_price = int(raid_reward['명예의 파편']*price_sh + raid_reward['정제된 파괴강석']*price_de + raid_reward['혼돈의 돌']*price_ch + raid_reward['찬란한 명예의 돌파석']*price_st + raid_reward['정제된 수호강석']*price_pr_2 + raid_reward['클리어 골드'])
            break_even = raid_reward_plus['명예의 파편']*price_sh + raid_reward_plus['정제된 파괴강석']*price_de + raid_reward_plus['혼돈의 돌']*price_ch + raid_reward_plus['찬란한 명예의 돌파석']*price_st + raid_reward_plus['정제된 수호강석']*price_pr_2- raid_reward_plus['더보기 골드']

        else:
            reward_price = int(raid_reward['명예의 파편']*price_sh + raid_reward['정제된 파괴강석']*price_de + raid_reward['혼돈의 돌']*price_ch + raid_reward['찬란한 명예의 돌파석']*price_st + raid_reward['정제된 수호강석']*price_pr_2)
            break_even = raid_reward_plus['명예의 파편']*price_sh + raid_reward_plus['정제된 파괴강석']*price_de + raid_reward_plus['혼돈의 돌']*price_ch + raid_reward_plus['찬란한 명예의 돌파석']*price_st + raid_reward_plus['정제된 수호강석']*price_pr_2

        
        if break_even >= 0 :
            result = '더보기 이득 : {} 골드'.format(int(break_even))
            value_all = reward_price+break_even
            result_all = '보상 밸류 (더보기 포함): {} 골드'.format(int(value_all))
            
        else :
            result = '더보기 손해 : {} 골드'.format(int(break_even))
            value_all = reward_price
            result_all = '보상 밸류 (더보기 하지않음) : {} 골드'.format(int(value_all))
        df_tuple = (raid_gate,reward_price,result,result_all)
        df_list.append(list(df_tuple))
        df_reward.append(value_all)
        
    df = pd.DataFrame(df_list,columns=('관문','컨텐츠 보상','더보기','전체 밸류'))
    st.subheader(raid)
    st.write(df)

    if raid == '카양겔 하드':
        st.write('[시련의 빛] 재료 교환 및 보석 교환 벨류를 계산에 넣지 않은 상태')
    elif '일리아칸' in raid :
        st.write('[쇠락의 눈동자] 재료 교환 벨류를 계산에 넣지 않은 상태')
    elif '에키드나 하드' in raid :
        st.write('[알키오네의 눈] 재료 교환 벨류를 계산에 넣지 않은 상태')
    else:pass

    st.subheader('컨텐츠 전체 밸류 : {} 골드'.format(int(sum(df_reward))))

with tab5:
    #'PC방 패키지' = 명파(대)200개 + 찬명돌600개 + 최상레하250개, 33000원
    #'주간 성장재료 패키지' = 명패(대)60개 + 찬명돌200개 + 최상레하500개, 22000원
    gold_value = st.number_input('가치 비율 100골드:__원',value=70) / 100

    discount = st.checkbox('문화상품권 특가할인 적용한다면 체크')
    if discount:
        discount_rate = st.number_input('특가 % 수치',value=6, min_value=0, max_value=10)
    else:
        discount_rate = 0

    select_package = st.multiselect('필요한 재료 선택',('명예의 파편','찬란한 명예의 돌파석','최상급 오레하 융화 재료'),['명예의 파편','찬란한 명예의 돌파석','최상급 오레하 융화 재료'])
    if '명예의 파편' in select_package:
        package_sh = price('명예의 파편 주머니(대)')
    else :
        package_sh = 0
    if '찬란한 명예의 돌파석' in select_package:
        package_st = price('찬란한 명예의 돌파석')
    else :
        package_st = 0
    if '최상급 오레하 융화 재료' in select_package:
        package_orh = price('최상급 오레하 융화 재료')
    else :
        package_orh = 0

    col5, col6  = st.columns(2)
    with col5:
        st.write('PC방 패키지, 33000원')
        pc_package_gold = package_orh*250 + package_sh*200 + package_st*600
        pc_package_money = 33000*(100-discount_rate)/100
        st.write('골드 가치 : {} 골드'.format(int(pc_package_gold)))
        st.write('골드 이득 : {} 골드'.format(int(pc_package_gold - pc_package_money/gold_value)))
        st.write('현금 이득 : {} 원'.format(int(pc_package_gold*gold_value - pc_package_money)))
    with col6:
        st.write('주간 성장재료 패키지, 22000원, 실링 제외')
        weekly_package_gold = package_orh*500 + package_sh*60 + package_st*200
        weekly_package_money = 22000*(100-discount_rate)/100
        st.write('골드 가치 : {} 골드'.format(int(weekly_package_gold)))
        st.write('골드 이득 : {} 골드'.format(int(weekly_package_gold - weekly_package_money/gold_value)))
        st.write('현금 이득 : {} 원'.format(int(weekly_package_gold*gold_value - weekly_package_money)))




with tab6:
    radio = st.radio("컨텐츠 종류",('4인 컨텐츠','8인 컨텐츠','3인 버스','4인 버스','5인 버스'))
    bid = st.number_input("경매품 가격을 입력하세요")
    if bid == 0.00 :
        pass
    elif radio == '4인 컨텐츠':
        st.write(int(bid*0.95*3/4.4),'골드 이상 ',int(bid*0.95*3/4),'골드 이하')
    elif radio == '8인 컨텐츠':
        st.write(int(bid*0.95*7/8.8),'골드 이상 ',int(bid*0.95*7/8),'골드 이하')
    elif radio == '3인 버스':
        st.write('보석 입찰 가격 ',(int(bid*0.95-50)/2.95),'골드')
    elif radio == '4인 버스':
        st.write('보석 입찰 가격 ',(int(bid*0.95-50)/3.95),'골드')
    elif radio == '5인 버스':
        st.write('보석 입찰 가격 ',(int(bid*0.95-50)/4.95),'골드')        
    elif radio == '6인 버스':
        st.write('보석 입찰 가격 ',(int(bid*0.95-50)/5.95),'골드')
