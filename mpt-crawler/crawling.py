import pymysql
from musinsa_standard_cralwer import data_crawling

AWS_RDS_USER="admin"
AWS_RDS_PORT="3306"
AWS_RDS_PASSWD="kakaocloud3"
AWS_RDS_HOST=""
AWS_RDS_DB="mydb"

conn = pymysql.connect(
    user=AWS_RDS_USER,
    passwd=AWS_RDS_PASSWD,
    host=AWS_RDS_HOST,
    port=int(AWS_RDS_PORT),
    db=AWS_RDS_DB,
    charset='utf8mb4'
    )

cursor = conn.cursor(pymysql.cursors.DictCursor)
price_list=[]
goods_list=[]

data = data_crawling()
for d in data:
    price = (str(d["item_id"]), str(d["price"]), str(d["time"]), str(d["rank"]))
    goods = (str(d["item_id"]), str(d["img"]), str(d["product_name"]),  d["rating_count"], str(d["rating"]), str(d["product_url"]), str(d["price"]), str(d["del_price"]))
    price_list.append(price)
    goods_list.append(goods)
        
print("crawling done!")


price_chart_sql = "INSERT INTO price_chart(id, price, chart_date, goods_rank) VALUES (%s,%s, %s, %s)"
product_sql = """INSERT INTO goods(id, img, name, rating_count, rating, url, price, del_price)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                id = values(id), img = values(img), name = values(name), url = values(url),
                rating = values(rating), rating_count = values(rating_count), price = values(price), del_price = values(del_price)"""

cursor.executemany(product_sql, goods_list)
cursor.executemany(price_chart_sql, price_list)
    
conn.commit()