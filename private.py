import requests
import json
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="saloa.gg",
    page_icon="😊",
    layout="wide",
)

st.title("Market/Auction")

dic = {'재련재료':50000,'배틀아이템':60000,'생활':90000}
market_name = []
market_price = []   
for value in dic.values():
    headers = {
        'accept': 'application/json',
        'authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAwODc4NTYifQ.Kz1Q31XCxpow-7vQUhjx8sejfVuQHi0T7BLfVoIXd4LErYMYJZ82oc9PX3Ls19rVxgvnNrwnpu2a2Ctg3vX8qO0214NgAh1Ab8M2hPPEksai7LY2enjhBGu7nvs8Ic9eq43p4DiGlpHQ68zZBbTo1WFbumayIrWkVAD-m7AHbkuguM0pMuXv8qL7ar6ZR-vVUsOetOuAannv6OpFhss3db1n4PuJM6S1TPyo2-Uo6T2FTp5Ue9C8TmIFnj97ZESorEU5KttbZ9qkL8yYnsK1A6glbYQksGMkCS0zQCp87BRQPccKAw41WlybHWcdjU3Zz3iDtMmQ5zv0GI_s0tzEmQ',
        'Content-Type': 'application/json',
        }

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
                market_name.append(item[i]['Name'])
                market_price.append(item[i]['RecentPrice'])
        except:pass

json_auction = {
    'ItemLevelMin': 0,
    'ItemLevelMax': 1700,
    'ItemGradeQuality': 0,
    'Sort': 'BUY_PRICE',
    'CategoryCode': 210000,
    'CharacterClass': '',
    'ItemTier': 3,
    'ItemGrade': '영웅',
    'ItemName': '3레벨',
    'PageNo': 0,
    'SortCondition': 'ASC',
}

response_auction = requests.post('https://developer-lostark.game.onstove.com/auctions/items', headers=headers, json=json_auction)
content_auction = response_auction.json()
item_list = content_auction['Items']


market_list = dict(zip(market_name,market_price))
def price(args):
    return market_list[args]
def charge(args):
    for n in range(0,market_list[args]):
        if n+1>=market_list[args]*0.05>n:
            return n+1
tab1, tab2, tab3 = st.tabs(['전설지도','오레하 공장', '배틀아이템 공장'])

with tab1:
    Legendmap=price('명예의 파편 주머니(대)')*11 + price('태양의 가호')*4 + price('태양의 축복')*10 + price('태양의 은총')*16 + item_list[1]['AuctionInfo']['BuyPrice']*5
    st.write('판매하지 않는다면 ',Legendmap,'골드')
    st.write('판매한다면 ',Legendmap*0.95,'골드')

with tab2:
    st.write('최상급 오레하 융화 재료 가격 : ',price('최상급 오레하 융화 재료'),'골드')
    st.subheader('고고학 제작')
    st.write('현재 가격 = [ 오레하 유물 : {}골드, 희귀한 유물 : {}골드, 고대 유물 : {}골드 ]'.format(price('오레하 유물'),price('희귀한 유물'),price('고대 유물')))
    if price('희귀한 유물')*25/4 >= price('오레하 유물'):
        oreha_legacy = price('오레하 유물')
        st.write('가루 교환 쓰지않음')
    else:
        oreha_legacy = price('희귀한 유물')*25/4
        st.write('가루 교환 사용')
    recipe_legacy = oreha_legacy*520 + price('희귀한 유물')*510 + price('고대 유물')*107
    profit_legacy = (price('최상급 오레하 융화 재료')-charge('최상급 오레하 융화 재료'))*1500-recipe_legacy-27600
    if profit_legacy>=0:
        st.write('최상급 오레하 융화 재료 : 제작 1칸 당 ',profit_legacy/10,'골드 이득')
    else:
        st.warning('최상급 오레하 융화 재료 : 손해')
    st.subheader('낚시 제작')
    st.write('현재 가격 = [ 오레하 태양 잉어 : {}골드, 자연산 진주 : {}골드, 붉은 살 생선 : {}골드, 생선 : {}골드 ]'.format(price('오레하 태양 잉어'),price('자연산 진주'),price('붉은 살 생선'),price('생선')))
    if price('붉은 살 생선')*25/4 >= price('오레하 태양 잉어'):
        oreha_fishing = price('오레하 태양 잉어')
        st.write('가루 교환 쓰지않음')
    else:
        oreha_fishing = price('붉은 살 생선')*25/4
        st.write('가루 교환 사용')
    recipe_fishing = oreha_fishing*520 + price('자연산 진주')*640 + price('생선')*142
    profit_fishing = (price('최상급 오레하 융화 재료')-charge('최상급 오레하 융화 재료'))*1500 - recipe_fishing -27600
    if profit_fishing >= 0:
        st.write('최상급 오레하 융화 재료 : 제작 1칸 당 ',profit_fishing/10,' 골드 이득')
    else:
        st.warning('최상급 오레하 융화 재료 : 손해')
with tab3:
    
    st.subheader('정령의 회복약')
    st.write('정령의 회복약 가격 : ',price('정령의 회복약'),'골드')
    battle_1 = (price('정령의 회복약')-charge('정령의 회복약'))*30 - (price('화사한 들꽃')*6 + price('수줍은 들꽃')*24 + price('들꽃')*5 + 260)
    if battle_1 >= 0:
        st.write('정령의 회복약 : 제작 1칸 당 ',battle_1/10,' 골드 이득')
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
