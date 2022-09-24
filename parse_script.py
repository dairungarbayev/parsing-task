import requests
import bs4 as bs
import json

url = 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'


headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    }
)

phone_dicts_list = []


for num in range(1,14):

    query_param = '?PAGEN_1='+str(num)
    response = requests.get(url+query_param, headers=headers)

    print(f'Page number: {num}')
    print(f'Response status code: {response.status_code}')

    soup = bs.BeautifulSoup(response.text, 'lxml')


    smartphones = soup.find_all('div',class_='bx_catalog_item double')
    print(f'Found {len(smartphones)} items on this page')

    for phone in smartphones:
        name = phone.find('div',class_='bx_catalog_item_title').a.h4.text
        articul = phone.find('div',class_='bx_catalog_item_XML_articul').text.strip()[9:]

        price_div = phone.find('div',class_='bx-more-prices')
        if price_div is not None:
            price_data = price_div.find_all('span')
            for span, ind in zip(price_data, range(len(price_data))):
                if 'Цена в интернет-магазине' in span.text:
                    price = price_data[ind+1].text.replace(' ','')[:-1]
        else:
            continue   # Skip items without price data

        propval_spans = phone.find('div',class_='bx_catalog_item_articul').find_all('span')
        for span, ind in zip(propval_spans,range(len(propval_spans))):
            if 'Объем встроенной памяти:' in span.text:
                memory = propval_spans[ind+1].text


        phone_dict = dict([("name", name),("articul", articul), ("price", price), ("memory-size", memory)])
        print(phone_dict)

        phone_dicts_list.append(phone_dict)



with open('smartphones.json', 'w', encoding='utf-8') as fp:
    json.dump(phone_dicts_list, fp, ensure_ascii=False, indent=4)
