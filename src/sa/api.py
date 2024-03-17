import requests
from urllib.parse import quote


def get_claninfo(addr):  # 주소
    url = 'http://barracks.sa.nexon.com/clanhome/board_list.aspx?sn=' + addr
    res = requests.get(url=url).text
    clan_id = res.split('GetClanEventInfo(\'E\',\'')[1].split('\')')[0]
    clan_name = res.split('chhl_clanName\">')[1].split('</p>')[0]
    mark_b = res.split('mark/')[1].split('\" alt')[0]
    mark_f = res.split('mark/')[2].split('\" alt')[0]
    return clan_id, clan_name, mark_b, mark_f


def get_clanMark(clan_id):
    params = {'method':'clan', 'clanNo':clan_id}
    url = 'http://barracks.sa.nexon.com/common/userInfo.aspx'
    res = requests.post(url=url, data=params).json().get('contents')
    m_back = res.split('mark/')[1].split('\' width')[0]
    m_front = res.split('mark/')[2].split('\' width')[0]
    return m_back, m_front


def get_battle(pageNo, strDate, home):
    url = 'http://barracks.sa.nexon.com/clanhome/record.aspx?n4PageNo='+pageNo+'&strDate='+strDate+'&sn='+home
    res = requests.get(url=url).text
    if res.count('클랜전 진행 기록이 없습니다.'):
        return []