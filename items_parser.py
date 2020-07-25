from bs4 import BeautifulSoup
import requests

def parse(server, item):   # типа /get_cats_info "Название предмета", "сервер"
    servers = {"Саргас":"sargas", 
               "Скорпион": "scorpio", 
               "Титан": "titan", 
               "Фобос": "fobos"} # servers
    
    iTem = item.replace(" ", "+")

    if server in servers:
        URL = f"https://pwcats.info/{servers[server]}/search?item={iTem}"
        headers = {"Accept-Language": "ru-RU, ru;q=0.9"}
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find('tbody')
        
        if items.find("tr") == None:
            return "Предмет не найден"
        
        #----------------------------------------------------------

        item_name = items.find("a").get_text(strip=True)
        item_id = items.find("a").get("href")
        sell_price = items.find("td", class_="sell").get_text(strip=True)
        purchase_price = items.find("td", class_="buy").get_text(strip=True)

        #----------------------------------------------------------
            
        url = f"https://pwcats.info{item_id}/"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        prices = soup.find("tbody")

        #-----------------------------------------------------------

        itemSeller_name = prices.find("tr").find("td").find("a").get_text(strip=True)
        result = f"Продавец: {itemSeller_name}\nГород: Комиссионка\nЦена продажы: {sell_price}\nЦена покупки: {purchase_price}"
        
        return result


    else:
        return False


