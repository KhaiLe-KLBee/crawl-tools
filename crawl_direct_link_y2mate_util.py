import requests
import re
import bs4

def y2mateCrawlLink(youtubeUrl, limitQuantity = '720p'):
    '''
    Gửi yêu cầu lấy link lên server
    '''
    try:
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

        soup = bs4.BeautifulSoup(htmlResultStep1, 'html.parser')
        regex_quantity = re.compile('([0-9]{3,4})p')
        list_a_tag_quantity = soup.findAll('a', {'rel': 'nofollow', 'href': '#'})
        list_quantity = [a.text.split(' ')[1] for a in list_a_tag_quantity]
        list_quantity_new = [q for q in list_quantity if regex_quantity.match(q)]

    except Exception as e:
        return '%s'%e, ''

    regex_id = 'k__id = "(.*?)"'
    regex_v_id = 'k_data_vid = "(.*?)"'
    _id = re.search(regex_id, htmlResultStep1).group(1)
    v_id = re.search(regex_v_id, htmlResultStep1).group(1)

    quantity = ''
    if (limitQuantity in list_quantity_new) == False:
        list_temp = [i for i in list_quantity_new if int(i[:-1]) < int(limitQuantity[:-1])]
        quantity = list_temp[0]
    else:
        quantity = limitQuantity

    '''
    Lấy link điều hướng
    '''
    try:
        requestUrlStep2 = 'https://www.y2mate.com/mates/convert'

        formDataStep2 = {
            'type': 'youtube',
            '_id': _id,
            'v_id': v_id,
            'ajax': '1',
            'ftype': 'mp4',
            'fquality': quantity[:-1]
        }

        dataStep2 = requests.post(requestUrlStep2, headers=headers, data=formDataStep2)
        htmlResultStep2 = dataStep2.json()['result']

        regex_link = '<a href="(.*?)"'
        link = re.search(regex_link, htmlResultStep2).group(1)

        return '', link
    
    except Exception as e:
        return '%s'%e, ''

if __name__ == '__main__':
    youtubeUrl = 'https://www.youtube.com/watch?v=e3h4IiKkRro'
    err, link = y2mateCrawlLink(youtubeUrl)

