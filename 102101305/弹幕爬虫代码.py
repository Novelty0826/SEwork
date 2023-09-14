import requests
import json
import re
import jieba
import wordcloud
import numpy as np
from PIL import Image
import pandas as pd

def get_search(v_keyword,v_max_page):
    for page in range(1,v_max_page +1):
        # 请求地址
        url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
            'Referer': 'https://www.bilibili.com/video/',
            'Accept': 'application/json, text/plain, */*',
            'Cookie': "buvid3=9BA66FD7-589E-4AF5-87E8-C695F18E4E55167635infoc; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; DedeUserID=72329711; DedeUserID__ckMd5=563d1c2e3fa3501e; LIVE_BUVID=AUTO2416525855441113; _uuid=6172FC11-3B10E-10C64-D2D6-DECD4D5B97A216369infoc; rpdid=|(u))kkYu|Y|0J'uYYmkuJlY|; fingerprint=e0c14ccac3346e53d1101a8a44a82044; buvid_fp=e0c14ccac3346e53d1101a8a44a82044; b_nut=100; header_theme_version=CLOSE; b_ut=5; FEED_LIVE_VERSION=V8; home_feed_column=4; buvid4=4C2151C5-0534-640F-978A-07CB1BE48D7D41658-022030217-Mk4wjKcJQ44%2Bkvvj7i7OOXhcbFnqUxJLIK599OdxPHJTV3r7W7Ql3A%3D%3D; nostalgia_conf=-1; CURRENT_FNVAL=4048; browser_resolution=1082-656; SESSDATA=10b2e975%2C1710070648%2C12014%2A91CjC1c8y1iWcfkjRVFRyLLyBDEs50YaQxJw2zzt53UkRIUrZmQ5rjwOXqEMT8W0g9SGcSVjVoZXFMX0V3SVd5X2czNXgtYzBQWDRuWVRwMTNZTTQzZVNrMmp1Y0VwT2t6WnU0RzZrcndueU55RThRYTRuQ3pVUjZyYlNGWWEwQ1c0VjFXa2dGNkJBIIEC; bili_jct=c07e9da7a1e6123d935368687d89d68e; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQ3Nzk3ODAsImlhdCI6MTY5NDUyMDU4MCwicGx0IjotMX0.CJbJiPjrXnrvGbq6UFSvbymiAO6cx75A0gNcNP4XZoo; bili_ticket_expires=1694779780; sid=7hv97gqi; bp_video_offset_72329711=840455495619706914; b_lsid=10A18F73C_18A89946B0A; PVID=1; CURRENT_QUALITY=80"
        }
        # 请求参数
        params = {
            '__refresh__': 'true',
            '_extra': '',
            'context': '',
            'page': page,
            'page_size': 30,
            'from_source': '',
            'from_spmid': '333.337',
            'platform': 'pc',
            'highlight': '1',
            'single_column': '0',
            'keyword': v_keyword,
            'qv_id': 'zv2B6HhWqYvAFxesiXAQQFxOifMOsPoe',
            'ad_resource': '5654',
            'source_tag': '3',
            'gaia_vtoken': '',
            'category_id': '',
            'search_type': 'video',
            'dynamic_offset': 36,
            'web_location': '1430654',
            'w_rid': '0775703a753e9316d09c4bb77a9a5de0',
            'wts': '1694586356'
        }
        # 向页面发送请求
        r = requests.get(url, headers=headers, params=params)
        # 获得视频bv号
        for index in r.json()['data']['result']:
            bv_id = index['bvid']
            with open('bv_id_1.txt', mode='a', encoding='utf-8') as f:
                f.write(bv_id)
                f.write('\n')
                # print(bv_id)
                # 获得视频弹幕地址
                cid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bv_id + '&jsonp=jsonp'
                response = requests.get(url=cid_url, headers=headers).content.decode('utf-8')
                res_dict = json.loads(response)
                values = res_dict['data']
                for cid_values in values:
                    cid = cid_values.get('cid')
                    cid = str(cid)
                    # print(cid)
                    url_1 = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + cid
                    response = requests.get(url=url_1, headers=headers).content.decode('utf-8')
                    # print(response.text)
                    print(response)
                    content_list = re.findall('<d p=".*?">(.*?)</d>', response)
                    print(content_list)
                    # for 遍历输出内容
                    for content in content_list:
                        with open('弹幕文本.txt', mode='a', encoding='utf-8') as f:
                            f.write(content)
                            f.write('\n')
                        print(content)

def get_wordcloud():
    f = open('弹幕文本.txt', encoding='utf-8')
    txt = f.read()
    print(txt)
    string = ' '.join(jieba.lcut(txt))
    print(string)
    mask = np.array(Image.open("photo_4.png"))
    wc = wordcloud.WordCloud(
        width=1000,
        height=700,
        background_color='white',
        font_path='msyh.ttc',
        scale=15,
        colormap='Blues',
        mask=mask
    )
    # wc.recolor()
    wc.generate(string)
    wc.to_file('词云图.png')

def get_excel():
    with open('弹幕文本.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    line_counts = {}
    for line in lines:
        content = line.strip()  # 去除行尾换行符等空白字符
        if content in line_counts:
            line_counts[content] += 1
        else:
            line_counts[content] = 1

    df = pd.DataFrame(list(line_counts.items()), columns=['弹幕', '出现次数'])
    df_sorted = df.sort_values(by='出现次数', ascending=False)
    df_sorted.to_excel('结果统计.xlsx', index=False)


if __name__=='__main__':
    search_keyword = '日本核污染水排海'
    max_page = 10
    get_search(v_keyword=search_keyword.encode('utf8'),
               v_max_page=max_page
               )
    get_wordcloud()
    get_excel()