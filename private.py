import requests
import streamlit as st
import pandas as pd
import pandas

st.set_page_config(
    page_title="saloa.gg",
    page_icon="😊",
    layout="wide",
)

st.title("Saloa")

reset = st.button('갱신하기')
if reset:
    st.cache_data.clear()
else:
    pass



headers = {
            'accept': 'application/json',
            'authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAwODc4NTYifQ.Kz1Q31XCxpow-7vQUhjx8sejfVuQHi0T7BLfVoIXd4LErYMYJZ82oc9PX3Ls19rVxgvnNrwnpu2a2Ctg3vX8qO0214NgAh1Ab8M2hPPEksai7LY2enjhBGu7nvs8Ic9eq43p4DiGlpHQ68zZBbTo1WFbumayIrWkVAD-m7AHbkuguM0pMuXv8qL7ar6ZR-vVUsOetOuAannv6OpFhss3db1n4PuJM6S1TPyo2-Uo6T2FTp5Ue9C8TmIFnj97ZESorEU5KttbZ9qkL8yYnsK1A6glbYQksGMkCS0zQCp87BRQPccKAw41WlybHWcdjU3Zz3iDtMmQ5zv0GI_s0tzEmQ',
            'Content-Type': 'application/json',
            }

@st.cache_data
def database():
    data_name = []
    data_price = []
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
    data_dict = dict(zip(data_name,data_price))
    return data_dict

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


def price(args):
    return database()[args]
def charge(args):
    for n in range(0,database()[args]):
        if n+1>=database()[args]*0.05>n:
            return n+1
        
tab1, tab2, tab3, tab4, tab5 = st.tabs(['전설지도','오레하 공장', '배틀아이템 공장','더보기 손익','경매 입찰가격'])

with tab1:
    Legendmap=price('명예의 파편 주머니(대)')*9 + price('태양의 가호')*4 + price('태양의 축복')*10 + price('태양의 은총')*16 + item_list[1]['AuctionInfo']['BuyPrice']*5
    st.write('판매하지 않는다면 ',Legendmap,'골드')
    st.write('판매한다면 ',Legendmap*0.95,'골드')

with tab2:
    st.write('최상급 오레하 융화 재료 가격 : ',price('최상급 오레하 융화 재료'),'골드')
    slide_option = (price('최상급 오레하 융화 재료')-2,price('최상급 오레하 융화 재료')-1,price('최상급 오레하 융화 재료'),price('최상급 오레하 융화 재료')+1,price('최상급 오레하 융화 재료')+2)
    oreha_value = st.selectbox('판매하려는 가격',slide_option,index=2)
    for n in range(0,oreha_value):
        if n+1>=oreha_value*0.05>n:
            oreha_charge = n+1

    st.subheader('고고학 제작')
    st.write('현재 가격 = [ 오레하 유물 : {}골드, 희귀한 유물 : {}골드, 고대 유물 : {}골드 ]'.format(price('오레하 유물'),price('희귀한 유물'),price('고대 유물')))
    if price('희귀한 유물')*25/4 >= price('오레하 유물'):
        oreha_legacy = price('오레하 유물')
        st.write('가루 교환 쓰지않음')
    else:
        oreha_legacy = price('희귀한 유물')*25/4
        st.write('가루 교환 사용')
    recipe_legacy = oreha_legacy*520 + price('희귀한 유물')*510 + price('고대 유물')*107
    profit_legacy = (oreha_value-oreha_charge)*1500-recipe_legacy-27600
    if profit_legacy>=0:
        st.write('최상급 오레하 융화 재료 : 제작 1칸 당 ',profit_legacy/100,'골드 이득')
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
    profit_fishing = (oreha_value-oreha_charge)*1500 - recipe_fishing -27600
    if profit_fishing >= 0:
        st.write('최상급 오레하 융화 재료 : 제작 1칸 당 ',profit_fishing/100,' 골드 이득')
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
        
with tab4:
    select_reward = st.multiselect('필요한 재료 선택',('명예의 파편','찬란한 명예의 돌파석','정제된 파괴강석','정제된 수호강석','혼돈의 돌'),['명예의 파편','찬란한 명예의 돌파석','정제된 파괴강석','정제된 수호강석','혼돈의 돌'])
    if '정제된 수호강석' in select_reward:
        price_pr_1 = st.number_input('지역채팅 한 덩이(9999개) 가격',value=1500)
    raid = st.selectbox('컨텐츠',('아브렐슈드 하드','카양겔 하드','일리아칸 노말','일리아칸 하드','혼돈의 상아탑 노말','혼돈의 상아탑 하드'))
    
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
        st.session_state['아브렐슈드 하드'] = ['아브렐슈드 하드1관문','아브렐슈드 하드2관문','아브렐슈드 하드3관문','아브렐슈드 하드4관문','아브렐슈드 하드5관문','아브렐슈드 하드6관문']

    if '카양겔 하드' not in st.session_state:
        st.session_state['카양겔 하드'] = ['카양겔 하드1관문','카양겔 하드2관문','카양겔 하드3관문','카양겔 하드4관문']

    if '일리아칸 노말' not in st.session_state:
        st.session_state['일리아칸 노말'] = ['일리아칸 노말1관문','일리아칸 노말2관문','일리아칸 노말3관문']

    if '일리아칸 하드' not in st.session_state:
        st.session_state['일리아칸 하드'] = ['일리아칸 하드1관문','일리아칸 하드2관문','일리아칸 하드3관문']

    if '혼돈의 상아탑 노말' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말'] = ['혼돈의 상아탑 노말1관문','혼돈의 상아탑 노말2관문','혼돈의 상아탑 노말3관문','혼돈의 상아탑 노말4관문']

    if '혼돈의 상아탑 하드' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드'] = ['혼돈의 상아탑 하드1관문','혼돈의 상아탑 하드2관문','혼돈의 상아탑 하드3관문','혼돈의 상아탑 하드4관문']

    #레이드 보상

    if '아브렐슈드 하드1관문' not in st.session_state:
        st.session_state['아브렐슈드 하드1관문'] = {'명예의 파편':1600,'정제된 파괴강석':24,'정제된 수호강석':48,'찬란한 명예의 돌파석':1.6,'혼돈의 돌':0.6,'더보기 골드':700}

    if '아브렐슈드 하드2관문' not in st.session_state:
        st.session_state['아브렐슈드 하드2관문'] = {'명예의 파편':2000,'정제된 파괴강석':36,'정제된 수호강석':72,'찬란한 명예의 돌파석':1.6,'혼돈의 돌':0.8,'더보기 골드':800}
    
    if '아브렐슈드 하드3관문' not in st.session_state:
        st.session_state['아브렐슈드 하드3관문'] = {'명예의 파편':1600,'정제된 파괴강석':36,'정제된 수호강석':72,'찬란한 명예의 돌파석':1.6,'혼돈의 돌':0.6,'더보기 골드':900}    

    if '아브렐슈드 하드4관문' not in st.session_state:
        st.session_state['아브렐슈드 하드4관문'] = {'명예의 파편':2000,'정제된 파괴강석':48,'정제된 수호강석':96,'찬란한 명예의 돌파석':1.6,'혼돈의 돌':0.8,'더보기 골드':1100}

    if '아브렐슈드 하드5관문' not in st.session_state:
        st.session_state['아브렐슈드 하드5관문'] = {'명예의 파편':2400,'정제된 파괴강석':60,'정제된 수호강석':120,'찬란한 명예의 돌파석':2,'혼돈의 돌':0.6,'더보기 골드':1100}
    
    if '아브렐슈드 하드6관문' not in st.session_state:
        st.session_state['아브렐슈드 하드6관문'] = {'명예의 파편':3000,'정제된 파괴강석':90,'정제된 수호강석':180,'찬란한 명예의 돌파석':3,'혼돈의 돌':1,'더보기 골드':1400}    

    if '카양겔 하드1관문' not in st.session_state:
        st.session_state['카양겔 하드1관문'] = {'명예의 파편':1500,'정제된 파괴강석':70,'정제된 수호강석':140,'찬란한 명예의 돌파석':3,'혼돈의 돌':0.2,'더보기 골드':700}

    if '카양겔 하드2관문' not in st.session_state:
        st.session_state['카양겔 하드2관문'] = {'명예의 파편':1500,'정제된 파괴강석':70,'정제된 수호강석':140,'찬란한 명예의 돌파석':3,'혼돈의 돌':0.2,'더보기 골드':700}
        
    if '카양겔 하드3관문' not in st.session_state:
        st.session_state['카양겔 하드3관문'] = {'명예의 파편':2000,'정제된 파괴강석':90,'정제된 수호강석':180,'찬란한 명예의 돌파석':4,'혼돈의 돌':0.2,'더보기 골드':900}

    if '카양겔 하드4관문' not in st.session_state:
        st.session_state['카양겔 하드4관문'] = {'명예의 파편':2500,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':6,'혼돈의 돌':0.6,'더보기 골드':1100}

    if '일리아칸 노말1관문' not in st.session_state:
        st.session_state['일리아칸 노말1관문'] = {'명예의 파편':3000,'정제된 파괴강석':120,'정제된 수호강석':240,'찬란한 명예의 돌파석':6,'혼돈의 돌':0.6,'더보기 골드':900}

    if '일리아칸 노말2관문' not in st.session_state:
        st.session_state['일리아칸 노말2관문'] = {'명예의 파편':3000,'정제된 파괴강석':160,'정제된 수호강석':320,'찬란한 명예의 돌파석':8,'혼돈의 돌':0.6,'더보기 골드':1100}
    
    if '일리아칸 노말3관문' not in st.session_state:
        st.session_state['일리아칸 노말3관문'] = {'명예의 파편':4200,'정제된 파괴강석':240,'정제된 수호강석':480,'정제된 수호강석':480,'찬란한 명예의 돌파석':8,'혼돈의 돌':1,'더보기 골드':1500}    

    if '일리아칸 하드1관문' not in st.session_state:
        st.session_state['일리아칸 하드1관문'] = {'명예의 파편':4000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':9,'혼돈의 돌':1.4,'더보기 골드':1200}

    if '일리아칸 하드2관문' not in st.session_state:
        st.session_state['일리아칸 하드2관문'] = {'명예의 파편':4000,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':12,'혼돈의 돌':1.4,'더보기 골드':1400}
    
    if '일리아칸 하드3관문' not in st.session_state:
        st.session_state['일리아칸 하드3관문'] = {'명예의 파편':5500,'정제된 파괴강석':360,'정제된 수호강석':720,'찬란한 명예의 돌파석':18,'혼돈의 돌':1.6,'더보기 골드':1900}    

    if '혼돈의 상아탑 노말1관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말1관문'] = {'명예의 파편':3000,'정제된 파괴강석':100,'정제된 수호강석':200,'찬란한 명예의 돌파석':2,'혼돈의 돌':0,'선명한 지혜의 기운':2,'더보기 골드':700}

    if '혼돈의 상아탑 노말2관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말2관문'] = {'명예의 파편':3000,'정제된 파괴강석':100,'정제된 수호강석':200,'정제된 수호강석':200,'찬란한 명예의 돌파석':2,'혼돈의 돌':0,'선명한 지혜의 기운':2,'더보기 골드':800}

    if '혼돈의 상아탑 노말3관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말3관문'] = {'명예의 파편':3000,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':2,'혼돈의 돌':0,'선명한 지혜의 기운':3,'더보기 골드':900}

    if '혼돈의 상아탑 노말4관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 노말4관문'] = {'명예의 파편':4500,'정제된 파괴강석':200,'정제된 수호강석':400,'찬란한 명예의 돌파석':3,'혼돈의 돌':0,'선명한 지혜의 기운':1,'선명한 지혜의 엘릭서':1,'더보기 골드':1100}

    elixer = price('빛나는 지혜의 정수')*6*0.95-250

    if '혼돈의 상아탑 하드1관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드1관문'] = {'명예의 파편':4000,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':3,'혼돈의 돌':0,'더보기 골드':1000-elixer/2}

    if '혼돈의 상아탑 하드2관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드2관문'] = {'명예의 파편':4000,'정제된 파괴강석':150,'정제된 수호강석':300,'찬란한 명예의 돌파석':3,'혼돈의 돌':0,'더보기 골드':1000-elixer/2}

    if '혼돈의 상아탑 하드3관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드3관문'] = {'명예의 파편':5000,'정제된 파괴강석':240,'정제된 수호강석':480,'찬란한 명예의 돌파석':5,'혼돈의 돌':0,'더보기 골드':1500-elixer*3/4}

    if '혼돈의 상아탑 하드4관문' not in st.session_state:
        st.session_state['혼돈의 상아탑 하드4관문'] = {'명예의 파편':5500,'정제된 파괴강석':300,'정제된 수호강석':600,'찬란한 명예의 돌파석':7,'혼돈의 돌':0,'더보기 골드':2000-elixer/4-price('빛나는 지혜의 정수')*6}

    raid_name = st.session_state[raid]
    df_list = []
    for i in range(0,len(raid_name)):
        raid_gate = raid_name[i]
        raid_reward = st.session_state[raid_gate]
        break_even = raid_reward['명예의 파편']*price_sh + raid_reward['정제된 파괴강석']*price_de + raid_reward['혼돈의 돌']*price_ch + raid_reward['찬란한 명예의 돌파석']*price_st + raid_reward['정제된 수호강석']*price_pr_2- raid_reward['더보기 골드']
        if break_even >= 0 :
            result = '더보기 이득 : {} 골드'.format(break_even)
        else :
            result = '더보기 손해 : {} 골드'.format(break_even)
        df_tuple = (raid_gate,result)
        df_list.append(list(df_tuple))
        
    df = pd.DataFrame(df_list,columns=('관문','손익'))
    st.subheader(raid)
    st.write(df)


with tab5:
    radio = st.radio("컨텐츠 종류",('4인 컨텐츠','8인 컨텐츠','3인 버스','4인 버스','5인 버스'))
    bid = st.number_input("경매품 가격을 입력하세요")
    if bid == 0.00 :
        pass
    elif radio == '4인 컨텐츠':
        st.write(bid*0.95*3/4.4,'골드 이상 ',bid*0.95*3/4,'골드 이하')
    elif radio == '8인 컨텐츠':
        st.write(bid*0.95*7/8.8,'골드 이상 ',bid*0.95*7/8,'골드 이하')
    elif radio == '3인 버스':
        st.write('보석 입찰 가격 ',(bid*0.95-50)/2.95,'골드')
    elif radio == '4인 버스':
        st.write('보석 입찰 가격 ',(bid*0.95-50)/3.95,'골드')
    elif radio == '5인 버스':
        st.write('보석 입찰 가격 ',(bid*0.95-50)/4.95,'골드')        
    elif radio == '6인 버스':
        st.write('보석 입찰 가격 ',(bid*0.95-50)/5.95,'골드')
