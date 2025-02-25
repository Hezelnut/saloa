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
    
    for t in range(1,6) :
        json_market = {
        'Sort': '',
        'CategoryCode': 40000,
        'CharacterClass': '',
        'ItemTier': 0,
        'ItemGrade': '유물',
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
        
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(['재료','융화 재료 제작','배틀아이템 제작','4티어 컨텐츠 손익','유물 각인 가격','경매 입찰가격'])

with tab0 :
    if 'modify' not in st.session_state:
        st.session_state['modify'] = True
    modify_recipe = st.checkbox('재료 가격 수정하기')
    if modify_recipe:
        st.session_state['modify'] = False
    else:
        st.session_state['modify'] = True

    col_recipe_1, col_recipe_2, col_recipe_3 = st.columns(3)
    with col_recipe_1:
        st.subheader('고고학')
        legacy_recipe_blue_avidos = st.number_input('아비도스 유물 가격',value=price('아비도스 유물'),disabled=st.session_state['modify'])
        legacy_recipe_blue_oreha = st.number_input('오레하 유물 가격',value=price('오레하 유물'),disabled=st.session_state['modify'])
        legacy_recipe_green = st.number_input('희귀한 유물 가격',value=price('희귀한 유물'),disabled=st.session_state['modify'])
        legacy_recipe_white = st.number_input('고대 유물 가격',value=price('고대 유물'),disabled=st.session_state['modify'])
    with col_recipe_2 :
        st.subheader('낚시')
        fishing_recipe_blue_avidos = st.number_input('아비도스 태양 잉어 가격',value=price('아비도스 태양 잉어'),disabled=st.session_state['modify'])
        fishing_recipe_blue_oreha = st.number_input('오레하 태양 잉어 가격',value=price('오레하 태양 잉어'),disabled=st.session_state['modify'])
        fishing_recipe_green = st.number_input('붉은 살 생선 가격',value=price('붉은 살 생선'),disabled=st.session_state['modify'])
        fishing_recipe_white = st.number_input('생선 가격',value=price('생선'),disabled=st.session_state['modify'])
    with col_recipe_3:
        st.subheader('벌목')
        tree_recipe_blue_avidos = st.number_input('아비도스 목재 가격',value=price('아비도스 목재'),disabled=st.session_state['modify'])
        tree_recipe_blue_oreha = st.number_input('튼튼한 목재 가격',value=price('튼튼한 목재'),disabled=st.session_state['modify'])
        tree_recipe_green = st.number_input('부드러운 목재 가격',value=price('부드러운 목재'),disabled=st.session_state['modify'])
        tree_recipe_white = st.number_input('목재 가격',value=price('목재'),disabled=st.session_state['modify'])
    st.write('')
    
    col_recipe_4,col_recipe_5, col_recipe_6 = st.columns(3)

    with col_recipe_4 :
        st.subheader('채광')
        mining_recipe_blue_avidos = st.number_input('아비도스 철광석 가격',value=price('아비도스 철광석'),disabled=st.session_state['modify'])
        mining_recipe_blue_oreha = st.number_input('단단한 철광석 가격',value=price('단단한 철광석'),disabled=st.session_state['modify'])
        mining_recipe_green = st.number_input('묵직한 철광석 가격',value=price('묵직한 철광석'),disabled=st.session_state['modify'])
        mining_recipe_white = st.number_input('철광석 가격',value=price('철광석'),disabled=st.session_state['modify'])
    with col_recipe_5:
        st.subheader('채집')
        flower_recipe_blue_avidos = st.number_input('아비도스 들꽃 가격',value=price('아비도스 들꽃'),disabled=st.session_state['modify'])
        flower_recipe_blue_oreha = st.number_input('화사한 들꽃 가격',value=price('화사한 들꽃'),disabled=st.session_state['modify'])
        flower_recipe_green = st.number_input('수줍은 들꽃 가격',value=price('수줍은 들꽃'),disabled=st.session_state['modify'])
        flower_recipe_white = st.number_input('들꽃 가격',value=price('들꽃'),disabled=st.session_state['modify'])
    with col_recipe_6 :
        st.subheader('수렵')
        hunting_recipe_blue_avidos = st.number_input('아비도스 두툼한 생고기 가격',value=price('아비도스 두툼한 생고기'),disabled=st.session_state['modify'])
        hunting_recipe_blue_oreha = st.number_input('오레하 두툼한 생고기',value=price('오레하 두툼한 생고기'),disabled=st.session_state['modify'])
        hunting_recipe_green = st.number_input('다듬은 생고기 가격',value=price('다듬은 생고기'),disabled=st.session_state['modify'])
        hunting_recipe_white = st.number_input('두툼한 생고기 가격',value=price('두툼한 생고기'),disabled=st.session_state['modify'])

with tab1:
    #harmonize = 융화재
    harmonize_setting = st.multiselect('영지 세팅', # 라벨
                                       ['여신의 가호','뒤집어요 카드놀이','곡예사의 대기실','찬란한 소원 나무','[실리안] 마성의 상속자','[페일린] 베른 무도회','[니아] 기본 의복'], # 전체 선택
                                       ['뒤집어요 카드놀이','곡예사의 대기실','찬란한 소원 나무','[실리안] 마성의 상속자','[페일린] 베른 무도회','[니아] 기본 의복'] #디폴트 옵션
                                      )
    harmonize_discount = 4
    if '뒤집어요 카드놀이' in harmonize_setting :
        harmonize_discount += 2
    else:pass
    if '여신의 가호' in harmonize_setting :
        harmonize_discount += 1
    else:pass
    if '찬란한 소원 나무' in harmonize_setting :
        harmonize_discount += 2
    else:pass
    if '곡예사의 대기실' in harmonize_setting :
        harmonize_discount += 4
    else:pass
    if '[실리안] 마성의 상속자' in harmonize_setting :
        harmonize_discount += 1
    else:pass
    if '[페일린] 베른 무도회' in harmonize_setting :
        harmonize_discount += 2
    else:pass
    if '[니아] 기본 의복' in harmonize_setting :
        harmonize_discount += 1
    else:pass
        
    harmonize = ['아비도스 융화 재료','최상급 오레하 융화 재료']
    choice = st.radio('제작할 융화 재료 선택',harmonize)
    if choice == '최상급 오레하 융화 재료':
        st.write('')
        st.write('')
        st.write('최상급 오레하 융화 재료 가격 : ',price('최상급 오레하 융화 재료'),'골드')
        st.write('제작 수수료 기준 : ',int(300-3*harmonize_discount),'골드')

        oreha_value_1 = st.number_input('최상급 오레하 판매 가격',value=price('최상급 오레하 융화 재료'))
        for n in range(0,oreha_value_1):
            if n+1>=oreha_value_1*0.05>n:
                oreha_charge = n+1
        st.write('')
        st.write('')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('고고학 제작')        

            if legacy_recipe_white*2 >= legacy_recipe_green:
                if legacy_recipe_green*6.25 >= legacy_recipe_blue_oreha:
                    oreha_legacy = legacy_recipe_blue_oreha
                    oreha_change_tf = '가루 교환 쓰지않음'
                else:
                    oreha_legacy = legacy_recipe_green*6.25
                    oreha_change_tf = '가루 교환 사용 (희귀한유물)'
            else:
                if legacy_recipe_white*5/4 >= legacy_recipe_blue_oreha/10:
                    oreha_legacy = legacy_recipe_blue_oreha
                    oreha_change_tf = '가루 교환 쓰지않음'
                else:
                    oreha_legacy = legacy_recipe_white*50/4
                    oreha_change_tf = '가루 교환 사용 (고대 유물)'

            recipe_legacy = oreha_legacy*52 + legacy_recipe_green*51 + legacy_recipe_white*107
            profit_legacy = (oreha_value_1-oreha_charge)*1500-recipe_legacy-100*(300-3*harmonize_discount)

            if profit_legacy>=0:
                legacy_result = '1칸 당 '+str(int(profit_legacy/100))+'골드 이득'
            else:
                legacy_result = '만들어 팔면 손해'
            
            legacy_1 = ('오레하 유물 : {}골드, 희귀한 유물 : {}골드, 고대 유물 : {}골드'.format(legacy_recipe_blue_oreha,legacy_recipe_green,legacy_recipe_white))
            
            col3.metric(label=legacy_1,value=legacy_result,delta=oreha_change_tf,delta_color='off')
        
        
        with col4:
            st.subheader('낚시 제작')

            fishing_1 = ('오레하 태양 잉어 : {}골드, 붉은 살 생선 : {}골드, 생선 : {}골드'.format(fishing_recipe_blue_oreha,fishing_recipe_green,fishing_recipe_white))
            
            if fishing_recipe_green*6.25 >= fishing_recipe_blue_oreha:
                oreha_fishing = fishing_recipe_blue_oreha
                fishing_2 = '가루 교환 쓰지않음'
            else:
                if fishing_recipe_green >= fishing_recipe_white*2:
                    oreha_fishing = fishing_recipe_white*12.5
                    fishing_2 = '가루 교환 사용 (생선)'
                else:
                    oreha_fishing = fishing_recipe_green*6.25
                    fishing_2 = '가루 교환 사용 (붉은 살 생선)'
            recipe_fishing = oreha_fishing*52 + fishing_recipe_green*64 + fishing_recipe_white*142
            profit_fishing = (oreha_value_1-oreha_charge)*1500 - recipe_fishing - 100*(300-3*harmonize_discount)
            if profit_fishing >= 0:
                fishing_result = '1칸 당 '+str(int(profit_fishing/100))+' 골드 이득'
            else:
                fishing_result = '만들어 팔면 손해'
            col4.metric(label=fishing_1,value=fishing_result,delta=fishing_2,delta_color='off')
    elif choice == '아비도스 융화 재료':
        st.write('')
        st.write('')
        st.write('아비도스 재료 가격 : ',price('아비도스 융화 재료'),'골드')
        st.write('제작 수수료 기준 : ',int(400-4*harmonize_discount),'골드')
        avidos_value_1 = st.number_input('아비도스 융화 재료 판매 가격',value=price('아비도스 융화 재료'))
        for n in range(0,avidos_value_1):
            if n+1>=avidos_value_1*0.05>n:
                avidos_charge_1 = n+1
        
        st.write('')
        st.write('')

        col_avidos_1,col_avidos_2 = st.columns(2)
        with col_avidos_1:

            st.subheader('고고학 제작')
            avidos_list_legacy = ('아비도스 유물 : {}골드, 희귀한 유물 : {}골드, 고대 유물 : {}골드'.format(legacy_recipe_blue_avidos,legacy_recipe_green,legacy_recipe_white))
            
            if legacy_recipe_green >= legacy_recipe_white*2:
                if legacy_recipe_blue_avidos >= legacy_recipe_white*12.5:
                    avidos_legacy = legacy_recipe_white*12.5
                    avidos_legacy_change = '가루 교환 사용 (고대 유물)'
                else:    
                    avidos_legacy = legacy_recipe_blue_avidos
                    avidos_legacy_change = '가루 교환 사용하지 않음'
            else:
                if legacy_recipe_blue_avidos >= legacy_recipe_green*6.25:
                    avidos_legacy = legacy_recipe_green*6.25
                    avidos_legacy_change = '가루 교환 사용 (희귀한 유물)'
                else:    
                    avidos_legacy = legacy_recipe_blue_avidos
                    avidos_legacy_change = '가루 교환 사용하지 않음'

            avidos_recipe_legacy = avidos_legacy*33 + legacy_recipe_green*45 + legacy_recipe_white*86
            avidos_legacy_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_legacy-100*(400-4*harmonize_discount)

            if avidos_legacy_profit>=0:
                avidos_legacy_result = '1칸 당 '+str(int(avidos_legacy_profit/100))+'골드 이득'
            else:
                avidos_legacy_result = '만들어 팔면 손해'
            
            st.metric(label=avidos_list_legacy,value=avidos_legacy_result,delta=avidos_legacy_change,delta_color='off')

            st.write('')

            st.subheader('낚시 제작')
            avidos_list_fishing = ('아비도스 태양 잉어 : {}골드, 붉은 살 생선 : {}골드, 생선 : {}골드'.format(fishing_recipe_blue_avidos,fishing_recipe_green,fishing_recipe_white))
            
            if fishing_recipe_green >= fishing_recipe_white*2:
                if fishing_recipe_blue_avidos >= fishing_recipe_white*12.5:
                    avidos_fishing = fishing_recipe_white*12.5
                    avidos_fishing_change = '가루 교환 사용 (생선)'
                else:    
                    avidos_fishing = fishing_recipe_blue_avidos
                    avidos_fishing_change = '가루 교환 사용하지 않음'
            else:
                if fishing_recipe_blue_avidos >= fishing_recipe_green*6.25:
                    avidos_fishing = fishing_recipe_green*6.25
                    avidos_fishing_change = '가루 교환 사용 (붉은 살 생선)'
                else:    
                    avidos_fishing = fishing_recipe_blue_avidos
                    avidos_fishing_change = '가루 교환 사용하지 않음'
                    
            avidos_recipe_fishing = avidos_fishing*33 + fishing_recipe_green*45 + fishing_recipe_white*86
            avidos_fishing_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_fishing-100*(400-4*harmonize_discount)

            if avidos_fishing_profit>=0:
                avidos_fishing_result = '1칸 당 '+str(int(avidos_fishing_profit/100))+'골드 이득'
            else:
                avidos_fishing_result = '만들어 팔면 손해'
            
            st.metric(label=avidos_list_fishing,value=avidos_fishing_result,delta=avidos_fishing_change,delta_color='off')

            st.write('')

            st.subheader('벌목 제작')
            avidos_list_tree = ('아비도스 목재 : {}골드, 부드러운 목재 : {}골드, 목재 : {}골드'.format(tree_recipe_blue_avidos,tree_recipe_green,tree_recipe_white))
            
            if tree_recipe_green >= tree_recipe_white*2:
                if tree_recipe_blue_avidos >= tree_recipe_white*12.5:
                    avidos_tree = tree_recipe_white*12.5
                    avidos_tree_change = '가루 교환 사용 (목재)'
                else:    
                    avidos_tree = tree_recipe_blue_avidos
                    avidos_tree_change = '가루 교환 사용하지 않음'
            else:
                if tree_recipe_blue_avidos >= tree_recipe_green*6.25:
                    avidos_tree = tree_recipe_green*6.25
                    avidos_tree_change = '가루 교환 사용 (부드러운 목재)'
                else:    
                    avidos_tree = tree_recipe_blue_avidos
                    avidos_tree_change = '가루 교환 사용하지 않음'
                    
            avidos_recipe_tree = avidos_tree*33 + tree_recipe_green*45 + tree_recipe_white*86
            avidos_tree_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_tree-100*(400-4*harmonize_discount)

            if avidos_tree_profit>=0:
                avidos_tree_result = '1칸 당 '+str(int(avidos_tree_profit/100))+'골드 이득'
            else:
                avidos_tree_result = '만들어 팔면 손해'
            
            st.metric(label=avidos_list_tree,value=avidos_tree_result,delta=avidos_tree_change,delta_color='off')
        
        with col_avidos_2:

            st.subheader('채광 제작')
            avidos_list_mining = ('아비도스 철광석 : {}골드, 묵직한 철광석 : {}골드, 철광석 : {}골드'.format(mining_recipe_blue_avidos,mining_recipe_green,mining_recipe_white))
            
            if mining_recipe_green >= mining_recipe_white*2:
                if mining_recipe_blue_avidos >= mining_recipe_white*12.5:
                    avidos_mining = mining_recipe_white*12.5
                    avidos_mining_change = '가루 교환 사용 (철광석)'
                else:    
                    avidos_mining = mining_recipe_blue_avidos
                    avidos_mining_change = '가루 교환 사용하지 않음'
            else:
                if mining_recipe_blue_avidos >= mining_recipe_green*6.25:
                    avidos_mining = mining_recipe_green*6.25
                    avidos_mining_change = '가루 교환 사용 (묵직한 철광석)'
                else:    
                    avidos_mining = mining_recipe_blue_avidos
                    avidos_mining_change = '가루 교환 사용하지 않음'
                    
            avidos_recipe_mining = avidos_mining*33 + mining_recipe_green*45 + mining_recipe_white*86
            avidos_mining_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_mining-100*(400-4*harmonize_discount)

            if avidos_mining_profit>=0:
                avidos_mining_result = '1칸 당 '+str(int(avidos_mining_profit/100))+'골드 이득'
            else:
                avidos_mining_result = '만들어 팔면 손해'
            
            st.metric(label=avidos_list_mining,value=avidos_mining_result,delta=avidos_mining_change,delta_color='off')

            st.write('')

            st.subheader('채집 제작')
            avidos_list_flower = ('아비도스 들꽃 : {}골드, 수줍은 들꽃 : {}골드, 들꽃 : {}골드'.format(flower_recipe_blue_avidos,flower_recipe_green,flower_recipe_white))
            
            if flower_recipe_green >= flower_recipe_white*2:
                if flower_recipe_blue_avidos >= flower_recipe_white*12.5:
                    avidos_flower = flower_recipe_white*12.5
                    avidos_flower_change = '가루 교환 사용 (들꽃)'
                else:    
                    avidos_flower = flower_recipe_blue_avidos
                    avidos_flower_change = '가루 교환 사용하지 않음'
            else:
                if flower_recipe_blue_avidos >= flower_recipe_green*6.25:
                    avidos_flower = flower_recipe_green*6.25
                    avidos_flower_change = '가루 교환 사용 (수줍은 들꽃)'
                else:    
                    avidos_flower = flower_recipe_blue_avidos
                    avidos_flower_change = '가루 교환 사용하지 않음'
                    
            avidos_recipe_flower = avidos_flower*33 + flower_recipe_green*45 + flower_recipe_white*86
            avidos_flower_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_flower-100*(400-4*harmonize_discount)

            if avidos_flower_profit>=0:
                avidos_flower_result = '1칸 당 '+str(int(avidos_flower_profit/100))+'골드 이득'
            else:
                avidos_flower_result = '만들어 팔면 손해'
            
            st.metric(label=avidos_list_flower,value=avidos_flower_result,delta=avidos_flower_change,delta_color='off')

            st.write('')

            st.subheader('수렵 제작')
            avidos_list_hunting = ('아비도스 두툼한 생고기 : {}골드, 다듬은 생고기 : {}골드, 두툼한 생고기 : {}골드'.format(hunting_recipe_blue_avidos,hunting_recipe_green,hunting_recipe_white))
            
            if hunting_recipe_green >= hunting_recipe_white*2:
                if hunting_recipe_blue_avidos >= hunting_recipe_white*12.5:
                    avidos_hunting = hunting_recipe_white*12.5
                    avidos_hunting_change = '가루 교환 사용 (두툼한 생고기)'
                else:    
                    avidos_hunting = hunting_recipe_blue_avidos
                    avidos_hunting_change = '가루 교환 사용하지 않음'
            else:
                if hunting_recipe_blue_avidos >= hunting_recipe_green*6.25:
                    avidos_hunting = hunting_recipe_green*6.25
                    avidos_hunting_change = '가루 교환 사용 (다듬은 생고기)'
                else:    
                    avidos_hunting = hunting_recipe_blue_avidos
                    avidos_hunting_change = '가루 교환 사용하지 않음'
                    
            avidos_recipe_hunting = avidos_hunting*33 + hunting_recipe_green*45 + hunting_recipe_white*86
            avidos_hunting_profit = (avidos_value_1-avidos_charge_1)*1000-avidos_recipe_hunting-100*(400-4*harmonize_discount)

            if avidos_hunting_profit>=0:
                avidos_hunting_result = '1칸 당 '+str(int(avidos_hunting_profit/100))+'골드 이득'
            else:
                avidos_hunting_result = '만들어 팔면 손해'
            
            st.metric(label=avidos_list_hunting,value=avidos_hunting_result,delta=avidos_hunting_change,delta_color='off')
    else:
        st.warning('수정이 필요한 상태')
    

with tab2:
    st.subheader('정령의 회복약')
    st.write('정령의 회복약 가격 : ',price('정령의 회복약'),'골드')
    battle_1 = (price('정령의 회복약')-charge('정령의 회복약'))*300 - (price('화사한 들꽃')*8 + price('수줍은 들꽃')*25 + price('들꽃')*33 + 2500)
    if battle_1 >= 0:
        st.write('정령의 회복약 : 제작 1칸 당 ',int(battle_1/100),' 골드 이득')
    else:
        st.warning('정령의 회복약 제작 : 손해')
    
    st.subheader('각성 물약')
    st.write('각성 물약 : ',price('각성 물약'),'골드')
    battle_2 = (price('각성 물약')-charge('각성 물약'))*300 - (price('진귀한 유물')*8 + legacy_recipe_green*24 + legacy_recipe_white*32 + 2500)
    if battle_2 >= 0:
        st.write('각성 물약 : 제작 1칸 당 ',battle_2/100,' 골드 이득')
    else:
        st.warning('각성 물약 제작 : 손해')

    st.subheader('아드로핀 물약')
    st.write('아드로핀 물약 : ',price('아드로핀 물약'),'골드')
    battle_3 = (price('아드로핀 물약')-charge('아드로핀 물약'))*300 - (price('진귀한 유물')*6 + price('수줍은 들꽃')*8 + legacy_recipe_green*17 + legacy_recipe_white*75 + 2500)
    if battle_3 >= 0:
        st.write('아드로핀 물약 : 제작 1칸 당 ',battle_3/100,' 골드 이득')
    else:
        st.warning('아드로핀 물약 제작 : 손해')    
    
    st.subheader('파괴 폭탄')
    st.write('파괴 폭탄 : ',price('파괴 폭탄'),'골드')
    battle_4 = (price('파괴 폭탄')-charge('파괴 폭탄'))*300 - (price('단단한 철광석')*4+price('묵직한 철광석')*15+price('철광석')*30 + 1400)
    if battle_4 >= 0:
        st.write('파괴 폭탄 : 제작 1칸 당 ',battle_4/100,' 골드 이득')
    else:
        st.warning('파괴 폭탄 제작 : 손해')
        

    st.subheader('암흑 수류탄')
    st.write('암흑 수류탄 : ',price('암흑 수류탄'),'골드')
    battle_5 = (price('암흑 수류탄')-charge('암흑 수류탄'))*300 - (price('튼튼한 목재')*4+price('부드러운 목재')*12+price('목재')*17 + 1400)
    if battle_5 >= 0:
        st.write('암흑 수류탄 : 제작 1칸 당 ',battle_5/100,' 골드 이득')
    else:
        st.warning('암흑 수류탄 제작 : 손해')

    st.subheader('성스러운 부적')
    st.write('성스러운 부적 : ',price('성스러운 부적'),'골드')
    battle_6 = (price('성스러운 부적')-charge('성스러운 부적'))*300 - (price('단단한 철광석')*4+price('묵직한 철광석')*14+price('철광석')*28 + 1400)
    if battle_6 >= 0:
        st.write('성스러운 부적 : 제작 1칸 당 ',battle_6/100,' 골드 이득')
    else:
        st.warning('성스러운 부적 제작 : 손해')

    st.subheader('빛나는 성스러운 부적')
    st.write('빛나는 성스러운 부적 : ',price('빛나는 성스러운 부적'),'골드')
    battle_7 = (price('빛나는 성스러운 부적')-charge('빛나는 성스러운 부적'))*200 - (price('성스러운 부적')*300 + price('단단한 철광석')*4 + 1400)
    if battle_7 >= 0:
        st.write('빛나는 성스러운 부적 : 제작 1칸 당 ',battle_7/100,' 골드 이득')
    else:
        st.warning('빛나는 성스러운 부적 제작 : 손해')
    
        
with tab3:
    select_reward = st.multiselect('필요한 재료 선택',('클리어 골드','운명의 파편','운명의 돌파석','운명의 파괴석','운명의 수호석','운명의 돌'),['클리어 골드','운명의 파편','운명의 돌파석','운명의 파괴석','운명의 수호석','운명의 돌'])
    raid_multiselect = st.multiselect('컨텐츠',
                                      ['카멘 하드','베히모스 노말','에키드나 하드','에기르 노말','에기르 하드','아브렐슈드 노말','아브렐슈드 하드', '모르둠 노말', '모르둠 하드'], # 전체 옵션
                                      ['에기르 하드','아브렐슈드 하드','모르둠 하드'] # 기본 선택 옵션
                                     )
    
    if '운명의 파편' in select_reward:
        price_sh = min([price('운명의 파편 주머니(대)')/3000,price('운명의 파편 주머니(중)')/2000,price('운명의 파편 주머니(소)')/1000])
    else:
        price_sh = 0
    
    if '운명의 돌파석' in select_reward:
        price_st = price('운명의 돌파석')
    else:
        price_st = 0

    if '운명의 파괴석' in select_reward:
        price_de = price('운명의 파괴석')/10
    else:
        price_de = 0

    if '운명의 수호석' in select_reward:
        price_pr_2 = price('운명의 수호석')/10
    else:
        price_pr_2 = 0

    if '운명의 돌' in select_reward:
        price_ch = 500
    else:
        price_ch = 0


    #레이드 종류
    if '카멘 하드' not in st.session_state:
        st.session_state['카멘 하드'] = ['카멘 하드1관문','카멘 하드2관문','카멘 하드3관문','카멘 하드4관문']

    if '베히모스 노말' not in st.session_state:
        st.session_state['베히모스 노말'] = ['베히모스 노말1관문','베히모스 노말2관문']

    if '에키드나 하드' not in st.session_state:
        st.session_state['에키드나 하드'] = ['에키드나 하드1관문','에키드나 하드2관문']

    if '에기르 노말' not in st.session_state:
        st.session_state['에기르 노말'] = ['에기르 노말1관문','에기르 노말2관문']

    if '에기르 하드' not in st.session_state:
        st.session_state['에기르 하드'] = ['에기르 하드1관문','에기르 하드2관문']

    if '아브렐슈드 노말' not in st.session_state:
        st.session_state['아브렐슈드 노말'] = ['아브렐슈드 노말1관문','아브렐슈드 노말2관문']

    if '아브렐슈드 하드' not in st.session_state:
        st.session_state['아브렐슈드 하드'] = ['아브렐슈드 하드1관문','아브렐슈드 하드2관문']
        
    if '모르둠 노말' not in st.session_state:
        st.session_state['모르둠 노말'] = ['모르둠 노말1관문','모르둠 노말2관문','모르둠 노말3관문']

    if '모르둠 하드' not in st.session_state:
        st.session_state['모르둠 하드'] = ['모르둠 하드1관문','모르둠 하드2관문','모르둠 하드3관문']



    #레이드 보상

    if '카멘 하드1관문' not in st.session_state:
        st.session_state['카멘 하드1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':0,
                '운명의 파괴석':30,
                '운명의 수호석':60,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':5000}
                ,
            '더보기':{
                '운명의 파편':0,
                '운명의 파괴석':100,
                '운명의 수호석':200,
                '운명의 돌파석':3,
                '혼돈의 돌':0,
                '더보기 골드':2000
                }
            }
    if '카멘 하드2관문' not in st.session_state:
        st.session_state['카멘 하드2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':0,
                '운명의 파괴석':40,
                '운명의 수호석':80,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':6000}
                ,
            '더보기':{
                '운명의 파편':0,
                '운명의 파괴석':120,
                '운명의 수호석':480,
                '운명의 돌파석':4.2,
                '혼돈의 돌':0,
                '더보기 골드':2400
                }
            }
    if '카멘 하드3관문' not in st.session_state:
        st.session_state['카멘 하드3관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':0,
                '운명의 파괴석':48,
                '운명의 수호석':96,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':9000}
                ,
            '더보기':{
                '운명의 파편':0,
                '운명의 파괴석':140,
                '운명의 수호석':280,
                '운명의 돌파석':5.4,
                '혼돈의 돌':0,
                '더보기 골드':2800
                }
            }
    if '카멘 하드4관문' not in st.session_state:
        st.session_state['카멘 하드4관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':0,
                '운명의 파괴석':60,
                '운명의 수호석':120,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':21000}
                ,
            '더보기':{
                '운명의 파편':0,
                '운명의 파괴석':170,
                '운명의 수호석':340,
                '운명의 돌파석':6.8,
                '혼돈의 돌':0,
                '더보기 골드':3600
                }
            }


    if '베히모스 노말1관문' not in st.session_state:
        st.session_state['베히모스 노말1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':3000,
                '운명의 파괴석':210,
                '운명의 수호석':420,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':7000}
                ,
            '더보기':{
                '운명의 파편':4000,
                '운명의 파괴석':600,
                '운명의 수호석':800,
                '운명의 돌파석':14,
                '혼돈의 돌':0,
                '더보기 골드':3100
                }
            }
    if '베히모스 노말2관문' not in st.session_state:
        st.session_state['베히모스 노말2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4000,
                '운명의 파괴석':270,
                '운명의 수호석':540,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':14500}
                ,
            '더보기':{
                '운명의 파편':6000,
                '운명의 파괴석':900,
                '운명의 수호석':1800,
                '운명의 돌파석':21,
                '혼돈의 돌':0,
                '더보기 골드':4900
                }
            }

    if '에키드나 하드1관문' not in st.session_state:
        st.session_state['에키드나 하드1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':2700,
                '운명의 파괴석':200,
                '운명의 수호석':400,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':6000}
                ,
            '더보기':{
                '운명의 파편':3800,
                '운명의 파괴석':550,
                '운명의 수호석':1100,
                '운명의 돌파석':12,
                '혼돈의 돌':0,
                '더보기 골드':2800
                }
            }
    if '에키드나 하드2관문' not in st.session_state:
        st.session_state['에키드나 하드2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':3800,
                '운명의 파괴석':260,
                '운명의 수호석':520,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':12500}
                ,
            '더보기':{
                '운명의 파편':5800,
                '운명의 파괴석':850,
                '운명의 수호석':1700,
                '운명의 돌파석':19,
                '혼돈의 돌':0,
                '더보기 골드':4100
                }
            }
        
    if '에기르 노말1관문' not in st.session_state:
        st.session_state['에기르 노말1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':3600,
                '운명의 파괴석':480,
                '운명의 수호석':960,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':7500}
                ,
            '더보기':{
                '운명의 파편':6500,
                '운명의 파괴석':700,
                '운명의 수호석':1400,
                '운명의 돌파석':16,
                '혼돈의 돌':0,
                '더보기 골드':3200
                }
            }
    if '에기르 노말2관문' not in st.session_state:
        st.session_state['에기르 노말2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4400,
                '운명의 파괴석':580,
                '운명의 수호석':1160,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':15500}
                ,
            '더보기':{
                '운명의 파편':9500,
                '운명의 파괴석':1000,
                '운명의 수호석':2000,
                '운명의 돌파석':28,
                '혼돈의 돌':0,
                '더보기 골드':5300
                }
            }
        
    if '에기르 하드1관문' not in st.session_state:
        st.session_state['에기르 하드1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4200,
                '운명의 파괴석':580,
                '운명의 수호석':1160,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':9000}
                ,
            '더보기':{
                '운명의 파편':7500,
                '운명의 파괴석':850,
                '운명의 수호석':1700,
                '운명의 돌파석':28,
                '혼돈의 돌':0,
                '더보기 골드':4100
                }
            }
    if '에기르 하드2관문' not in st.session_state:
        st.session_state['에기르 하드2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':5400,
                '운명의 파괴석':660,
                '운명의 수호석':1320,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':18500}
                ,
            '더보기':{
                '운명의 파편':11000,
                '운명의 파괴석':1150,
                '운명의 수호석':2300,
                '운명의 돌파석':38,
                '혼돈의 돌':0,
                '더보기 골드':6600
                }
            }
    
    if '아브렐슈드 노말1관문' not in st.session_state:
        st.session_state['아브렐슈드 노말1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4000,
                '운명의 파괴석':540,
                '운명의 수호석':1080,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':8500}
                ,
            '더보기':{
                '운명의 파편':7000,
                '운명의 파괴석':800,
                '운명의 수호석':1600,
                '운명의 돌파석':18,
                '혼돈의 돌':0,
                '더보기 골드':3800
                }
            }
    if '아브렐슈드 노말2관문' not in st.session_state:
        st.session_state['아브렐슈드 노말2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4600,
                '운명의 파괴석':640,
                '운명의 수호석':1280,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':16500}
                ,
            '더보기':{
                '운명의 파편':10500,
                '운명의 파괴석':1050,
                '운명의 수호석':2100,
                '운명의 돌파석':30,
                '혼돈의 돌':0,
                '더보기 골드':5200
                }
            }
        
    if '아브렐슈드 하드1관문' not in st.session_state:
        st.session_state['아브렐슈드 하드1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4600,
                '운명의 파괴석':640,
                '운명의 수호석':1280,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':10000}
                ,
            '더보기':{
                '운명의 파편':8000,
                '운명의 파괴석':950,
                '운명의 수호석':1900,
                '운명의 돌파석':32,
                '혼돈의 돌':0,
                '더보기 골드':4500
                }
            }
    if '아브렐슈드 하드2관문' not in st.session_state:
        st.session_state['아브렐슈드 하드2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':6000,
                '운명의 파괴석':700,
                '운명의 수호석':1400,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':20000}
                ,
            '더보기':{
                '운명의 파편':14000,
                '운명의 파괴석':1400,
                '운명의 수호석':2800,
                '운명의 돌파석':48,
                '혼돈의 돌':0,
                '더보기 골드':7200
                }
            }
        
    if '모르둠 노말1관문' not in st.session_state:
        st.session_state['모르둠 노말1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':2600,
                '운명의 파괴석':320,
                '운명의 수호석':640,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':6000
                }
                ,
            '더보기':{
                '운명의 파편':4800,
                '운명의 파괴석':500,
                '운명의 수호석':1000,
                '운명의 돌파석':18,
                '혼돈의 돌':0,
                '더보기 골드':2400
                }
            }
        
    if '모르둠 노말2관문' not in st.session_state:
        st.session_state['모르둠 노말2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':3000,
                '운명의 파괴석':400,
                '운명의 수호석':800,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':9500}
                ,
            '더보기':{
                '운명의 파편':5600,
                '운명의 파괴석':620,
                '운명의 수호석':1240,
                '운명의 돌파석':20,
                '혼돈의 돌':0,
                '더보기 골드':3200
                }
            }
        
    if '모르둠 노말3관문' not in st.session_state:
        st.session_state['모르둠 노말3관문'] = {
        '컨텐츠 보상':{
            '운명의 파편':4200,
            '운명의 파괴석':520,
            '운명의 수호석':1040,
            '운명의 돌파석':0,
            '혼돈의 돌':0,
            '클리어 골드':12500}
            ,
        '더보기':{
            '운명의 파편':7400,
            '운명의 파괴석':840,
            '운명의 수호석':1680,
            '운명의 돌파석':26,
            '혼돈의 돌':0,
            '더보기 골드':4200
            }
        }
                          
    if '모르둠 하드1관문' not in st.session_state:
        st.session_state['모르둠 하드1관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':3400,
                '운명의 파괴석':440,
                '운명의 수호석':880,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':7000}
                ,
            '더보기':{
                '운명의 파편':7000,
                '운명의 파괴석':830,
                '운명의 수호석':1660,
                '운명의 돌파석':31,
                '혼돈의 돌':0,
                '더보기 골드':2700
                }
            }
    if '모르둠 하드2관문' not in st.session_state:
        st.session_state['모르둠 하드2관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':4000,
                '운명의 파괴석':520,
                '운명의 수호석':1040,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':11000}
                ,
            '더보기':{
                '운명의 파편':9900,
                '운명의 파괴석':1140,
                '운명의 수호석':2280,
                '운명의 돌파석':36,
                '혼돈의 돌':0,
                '더보기 골드':4100
                }
            }
    if '모르둠 하드3관문' not in st.session_state:
        st.session_state['모르둠 하드3관문'] = {
            '컨텐츠 보상':{
                '운명의 파편':5600,
                '운명의 파괴석':640,
                '운명의 수호석':1280,
                '운명의 돌파석':0,
                '혼돈의 돌':0,
                '클리어 골드':20000}
                ,
            '더보기':{
                '운명의 파편':16800,
                '운명의 파괴석':2080,
                '운명의 수호석':4160,
                '운명의 돌파석':64,
                '혼돈의 돌':0,
                '더보기 골드':5800
                }
            }
        
    for k in range(0,len(raid_multiselect)):
        raid = raid_multiselect[k]
        raid_name = st.session_state[raid]
        df_list = []
        df_reward = []
        for i in range(0,len(raid_name)):
            raid_gate = raid_name[i]
            raid_reward = st.session_state[raid_gate]['컨텐츠 보상']
            raid_reward_plus = st.session_state[raid_gate]['더보기']
            if '클리어 골드' in select_reward:
                reward_price = int(raid_reward['운명의 파편']*price_sh + raid_reward['운명의 파괴석']*price_de + raid_reward['혼돈의 돌']*price_ch + raid_reward['운명의 돌파석']*price_st + raid_reward['운명의 수호석']*price_pr_2 + raid_reward['클리어 골드'])
                break_even = raid_reward_plus['운명의 파편']*price_sh + raid_reward_plus['운명의 파괴석']*price_de + raid_reward_plus['혼돈의 돌']*price_ch + raid_reward_plus['운명의 돌파석']*price_st + raid_reward_plus['운명의 수호석']*price_pr_2- raid_reward_plus['더보기 골드']

            else:
                reward_price = int(raid_reward['운명의 파편']*price_sh + raid_reward['운명의 파괴석']*price_de + raid_reward['혼돈의 돌']*price_ch + raid_reward['운명의 돌파석']*price_st + raid_reward['운명의 수호석']*price_pr_2)
                break_even = raid_reward_plus['운명의 파편']*price_sh + raid_reward_plus['운명의 파괴석']*price_de + raid_reward_plus['혼돈의 돌']*price_ch + raid_reward_plus['운명의 돌파석']*price_st + raid_reward_plus['운명의 수호석']*price_pr_2

            
            if break_even >= 0 :
                result = '더보기 이득 : {} 골드'.format(int(break_even))
                value_all = reward_price+break_even
                result_all = '보상 밸류 (더보기 포함): {} 골드'.format(int(value_all))
                
            else :
                result = '더보기 손해 : {} 골드'.format(int(break_even))
                value_all = reward_price
                result_all = '보상 밸류 (더보기 하지않음) : {} 골드'.format(int(value_all))
            df_tuple = (raid_gate,raid_reward['클리어 골드'],reward_price,result,result_all)
            df_list.append(list(df_tuple))
            df_reward.append(value_all)
            
        df = pd.DataFrame(df_list,columns=('관문','클리어 골드','골드 & 재료 벨류','더보기','전체 밸류'))
        st.subheader(raid)
        st.write(df)

        #심연의 재료 보조 재료 주머니
        sub_reward = (price('용암의 숨결')*2+price('빙하의 숨결')*5)/2
        
        if raid == '베히모스 노말':
            st.write('**[베히모스의 비늘]** 재료 교환 가치를 계산에 넣지 않은 상태')
        elif '에기르 하드' in raid :
            st.write('**[업화의 쐐기돌]** 1관문 8개 | 2관문 12개')
            st.write(f'<더보기> → 보조 재료 주머니 4개 가치 : {sub_reward*4} 골드')
            st.write(f'<경매 재료> → 보조 재료 주머니 2개 가치 : {sub_reward*2} 골드')
        elif '에기르 노말' in raid :
            st.write('**[업화의 쐐기돌]** 1관문 4개 | 2관문 6개')
            st.write(f'<더보기> → 보조 재료 주머니 2개 가치 : {sub_reward*2} 골드')
            st.write(f'<경매 재료> → 보조 재료 주머니 1개 가치 : {sub_reward*1} 골드')
        elif '에키드나 하드' in raid :
            st.write('**[알키오네의 눈]** 재료 교환 벨류를 계산에 넣지 않은 상태')
        elif '아브렐슈드 노말' in raid :
            st.write('**[카르마의 잔영 ]** 1관문 4개 | 2관문 6개')
            st.write(f'<더보기> → 보조 재료 주머니 2개 가치 : {sub_reward*2} 골드')
            st.write(f'<경매 재료> → 보조 재료 주머니 1개 가치 : {sub_reward*1} 골드')
        elif '아브렐슈드 하드' in raid :
            st.write('**[카르마의 잔영 ]** 1관문 8개 | 2관문 12개')
            st.write(f'<더보기> → 보조 재료 주머니 4개 가치 : {sub_reward*4} 골드')
            st.write(f'<경매 재료> → 보조 재료 주머니 2개 가치 : {sub_reward*2} 골드')
        elif '모르둠 노말' in raid :
            st.write('**[낙뢰의 뿔]** 1관문 3개 | 2관문 5개 | 3관문 10개')
            st.write('**[낙뢰의 뿔]** 총 18개 | 더보기 18개')
        elif '모르둠 하드' in raid :
            st.write('**[우레의 뇌옥]** 1관문 3개 | 2관문 5개 | 3관문 10개')
            st.write('**[우레의 뇌옥]** 총 18개 | 더보기 18개')
        else:pass

        st.write('컨텐츠 전체 밸류 : **{} 골드**'.format(int(sum(df_reward))))
        st.write('')
        st.write('')

with tab4:
    st.write(f"원한 {price('원한 각인서')} 골드")
    st.write('')
    st.write(f"아드레날린 {price('아드레날린 각인서')} 골드")
    st.write('')
    st.write(f"예리한 둔기 {price('예리한 둔기 각인서')} 골드")
    st.write('')
    st.write(f"돌격대장 {price('돌격대장 각인서')} 골드")
    st.write('')
    st.write(f"저주받은 인형 {price('저주받은 인형 각인서')} 골드")
    st.write('')
    st.write(f"기습의 대가 {price('기습의 대가 각인서')} 골드")
    st.write('')
    st.write(f"질량 증가 {price('질량 증가 각인서')} 골드")
    st.write('')
    st.write(f"타격의 대가 {price('타격의 대가 각인서')} 골드")

    






with tab5:
    radio = st.radio("컨텐츠 종류",('4인 컨텐츠','8인 컨텐츠','3인 버스','4인 버스','베히 8인 버스'))
    bid = st.number_input("경매품 가격을 입력하세요")
    if radio == '4인 컨텐츠':
        st.write(int(bid*0.95*3/4.4),'골드 이상 ',int(bid*0.95*3/4),'골드 이하')
    elif radio == '8인 컨텐츠':
        st.write(int(bid*0.95*7/8.8),'골드 이상 ',int(bid*0.95*7/8),'골드 이하')
    elif radio == '3인 버스':
        st.write('보석 입찰 가격 ',(int(bid*0.95-50)/3),'골드')
    elif radio == '4인 버스':
        st.write('**[유물각인서]** 보석 입찰 가격 ',f"{int(int(bid*0.95-50)/4)} 골드")
        st.write('**[유물각인서]** 경매 입찰 가격 ',f"{int(int(bid*0.95)*3/4)} 골드")
        st.write('')
        bus4_1 = st.number_input("미참 손님 가격",value=15000)
        bus4_2 = st.number_input("독식 손님 가격",value=18000)
        st.write('보석 거래 가격 : ',int( bus4_1 + (bus4_2-bus4_1)/8),'골드 / 독식 입찰 가격 : ',int( (bus4_2-bus4_1)*7/8 ),'골드')
    elif radio == '베히 8인 버스':
        st.write('**[유물각인서]** 보석 입찰 가격 ',f"{int(int(bid*0.95-50)/8)} 골드")
        st.write('**[유물각인서]** 경매 입찰 가격 ',f"{int(int(bid*0.95)*7/8)} 골드")
        st.write('')
        behemoth_1 = st.number_input("미참 손님 가격",value=10000)
        behemoth_2 = st.number_input("독식 손님 가격",value=12000)
        st.write('보석 거래 가격 : ',int( behemoth_1 + (behemoth_2-behemoth_1)/16),'골드 / 독식 입찰 가격 : ',int( (behemoth_2-behemoth_1)*15/16 ),'골드')
        

