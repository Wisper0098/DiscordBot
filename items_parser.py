from bs4 import BeautifulSoup
import requests

def parse(server, item): 
    servers = {"Саргас":"sargas", 
               "Скорпион": "scorpio", 
               "Титан": "titan", 
               "Фобос": "fobos"} # servers
    
    iTem = item.replace(" ", "+") # 

    if server in servers:
        URL = f"https://pwcats.info/{servers[server]}/search?item={iTem}"
        headers = {"Accept-Language": "ru-RU, ru;q=0.9"}
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find('tbody')
        
        if items.find("tr") == None: # if content of body == none
            return "Предмет не найден"
        
        #----------------------------------------------------------

        item_name = items.find("a").get_text(strip=True) # getting item name from <a> tag
        item_id = items.find("a").get("href") # item_id
        sell_price = items.find("td", class_="sell").get_text(strip=True)
        purchase_price = items.find("td", class_="buy").get_text(strip=True)
        itemS = dict()
        #for i in items.find_all("a"):
        #    item_name = i.get_text(strip=True)
        #    item_price = i.find("td")
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

parse("Фобос", "Амулет")


