from bs4 import BeautifulSoup
import requests
import urllib.request
from datetime import datetime
from pytz import timezone
import re

def get_total_page():
    try :
        site = "https://www.musinsa.com/brands/musinsastandard?category3DepthCodes=&category2DepthCodes=&category1DepthCode=&colorCodes=&startPrice=&endPrice=&exclusiveYn=&includeSoldOut=&saleGoods=&timeSale=&includeKeywords=&sortCode=SALE_ONE_DAY&tags=&page=1&size=90&listViewType=big&campaignCode=&groupSale=&outletGoods=&plusDelivery="
        source = requests.get(site).text
        soup = BeautifulSoup(source, "html.parser")
        total_page_num = int(re.sub('<.+?>', '', str(soup.select('.totalPagingNum')[0])))
        return total_page_num
    except :
        print(f"error parsing total pages")
        return 1
    
def data_crawling():
    data = []
    #category = ['001', '002', '003', '004', '005', '007', '022', '008', '026', '011']
    # [상의, 아우터, 바지, 가방, 신발, 모자, 스커트, 양말/레그웨어, 속옷, 액세서리]
    kst = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%dT%H:%M')
    total_page = get_total_page()
    rank_cnt = 1   
    for page in range(1, total_page+1):
        try :
            site = "https://www.musinsa.com/brands/musinsastandard?category3DepthCodes=&category2DepthCodes=&category1DepthCode=&colorCodes=&startPrice=&endPrice=&exclusiveYn=&includeSoldOut=&saleGoods=&timeSale=&includeKeywords=&sortCode=SALE_ONE_DAY&tags=&page="+str(page)+"&size=90&listViewType=big&campaignCode=&groupSale=&outletGoods=&plusDelivery="
            source = requests.get(site).text
            soup = BeautifulSoup(source, "html.parser")
            items = soup.select("#searchList")[0].findAll("li", "li_box")
        except :
            print(f"error in {page}th page")
            break
        dict_list = []    
        for item in items:
            item_dict = {}
            item_dict["item_id"] = int(item.select("p.txt_cnt_like")[0].get("data-goodsno"))  
            item_dict["product_url"] = item.select("p.list_info > a")[0].get("href")
            item_dict["img"] = item.find("img").get("data-original") #img_url
            item_dict["rank"] = rank_cnt
            rank_cnt+=1
            item_dict["product_name"] = item.select("p.list_info > a")[0].get('title').strip() 
            try:
                item_dict["rating_count"] = int(re.sub('<.+?>', '', str(item.find("span", "count"))).replace(",", ""))
                item_dict["rating"] = float(item.select("span.bar")[0].get("style").strip().split(":")[1].replace("%", ""))
            except:
                item_dict["rating_count"] = 0
                item_dict["rating"] = 0
            item_dict["price"] = int(re.sub('<.+?>', '', str(item.select("span.txt_price_member")[0])).strip().split("원")[0].replace(",", ""))
            # product_url = //www.musinsa.com/app/goods/product_id

            try:
                item_dict["del_price"] = int(re.sub('<.+?>', '', str(item.select("p.price > del")[0])).strip().split("원")[0].replace(",", ""))
            except:
                item_dict["del_price"] = item_dict["price"]
                
            item_dict["time"] = kst
            dict_list.append(item_dict)
        data.extend(dict_list)
        print("page : " + str(page) + " done")
    return data


#img_urls 따로 만들어야
# product, category 인 category_info 테이블 하나 더 만들어 카테고리에 대한 크롤링 따로 진행, insert_ignore

