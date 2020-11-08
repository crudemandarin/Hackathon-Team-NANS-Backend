import requests #access a URL and pull out the data from that website
from bs4 import BeautifulSoup #parse data from the data "page"

def scrape():
    URL = "https://www.bradsdeals.com/blog/student-discounts"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

    page = requests.get(URL, headers=headers)  # returns all the data from the website
    soup = BeautifulSoup(page.content, 'html.parser')

    template = {
        'href': '',
        'company': '',
        'discount': ''
    }
    Dlist = []
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            template['href'] = link.attrs['href']
            Dlist.append(template)
            template = {
                'href': '',
                'company': '',
                'discount': ''
            }

    # DELETING ALL THE JUNK FROM THE LINKS
    remove_list = []
    for element in Dlist:
        if element['href'][0] != 'h':
            remove_list.append(element)
            continue

    for x in remove_list:
        Dlist.remove(x)

    # DELETING THE EXTRA LINKS
    Dlist = Dlist[0:-9]

    firstH3 = soup.find('h3')  # Start here
    uls = []
    for nextSibling in firstH3.findNextSiblings():
        if nextSibling.name == 'h2':
            break
        if nextSibling.name == 'ul':
            uls.append(nextSibling)

    JSON = []

    for ul in uls:
        for li in ul.findAll('li'):
            my_item = next((item for item in Dlist if item['href'] == li.a.get('href')), None)
            if my_item is not None:
                trash = li.text.replace('\xa0', '')
                if trash.find(':') != -1:
                    trash2 = trash.split(':')
                    my_item['company'] = trash2[0]
                    my_item['discount'] = trash2[1][1:]
                else:
                    my_item['company'] = trash
                    my_item['discount'] = "Discounts may vary"
                JSON.append(my_item)

    for k in range(0,10): JSON[k]['tag'] = 'Travel'
    for k in range(10,88): JSON[k]['tag'] = 'Clothing'
    for k in range(88,123): JSON[k]['tag'] = 'Electronics/Accesories/Computer'
    for k in range(123,154): JSON[k]['tag'] = 'Health & Beauty'
    for k in range(154,168): JSON[k]['tag'] = 'Entertainment'
    for k in range(168,175): JSON[k]['tag'] = 'Books/Magazines'
    for k in range(175,188): JSON[k]['tag'] = 'Food'
    for k in range(188,193): JSON[k]['tag'] = 'Insurance'
    for k in range(193,204): JSON[k]['tag'] = 'Jewelry/Bags'
    for k in range(203,209): JSON[k]['tag'] = 'Games'
    for k in range(209,216): JSON[k]['tag'] = 'Flowers/Gifts'
    for k in range(216,219): JSON[k]['tag'] = 'Moving'
    for k in range(219, 243): JSON[k]['tag'] = 'Other'

    # for el in JSON:
    #     print('Company:', el['company'])
    #     print('Benefit:', el['discount'])
    #     print('Link:', el['href'])
    #     print('Tag:', el['tag'])
    #     print()
    return JSON

# scrape()