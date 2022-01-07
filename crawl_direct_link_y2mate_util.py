import requests
import re


def y2mateCrawlLink(youtubeUrl):
    '''
    Gửi yêu cầu lấy link lên server
    '''
    requestUrlStep1 = 'https://www.y2mate.com/mates/en163/analyze/ajax'

    headers = {
        'accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with':'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    formDataStep1 = {
        'url': youtubeUrl,
        'q_auto': '0',
        'ajax': '1'
    }

    dataStep1 = requests.post(requestUrlStep1, headers = headers, data = formDataStep1)
    htmlResultStep1 = dataStep1.json()['result'].replace('\\', '')

    regex_id = 'k__id = "(.*?)"'
    regex_v_id = 'k_data_vid = "(.*?)"'
    _id = re.search(regex_id, htmlResultStep1).group(1)
    v_id = re.search(regex_v_id, htmlResultStep1).group(1)

    '''
    Lấy link điều hướng
    '''
    requestUrlStep2 = 'https://www.y2mate.com/mates/convert'

    formDataStep2 = {
        'type': 'youtube',
        '_id': _id,
        'v_id': v_id,
        'ajax': '1',
        'ftype': 'mp4',
        'fquality': '1080'
    }

    dataStep2 = requests.post(requestUrlStep2, headers=headers, data=formDataStep2)
    htmlResultStep2 = dataStep2.json()['result']

    regex_link = '<a href="(.*?)"'
    link = re.search(regex_link, htmlResultStep2).group(1)

    return link

if __name__ == '__main__':
    youtubeUrl = 'https://www.youtube.com/watch?v=e3h4IiKkRro'
    link = y2mateCrawlLink(youtubeUrl)

