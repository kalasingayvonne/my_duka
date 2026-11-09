import psycopg2

conn=psycopg2.connect(host='localhost',port=5434,user='postgres',password='4725',dbname='myduka_db')

cur=conn.cursor()

def get_products():
 cur.execute("select * from products")
 products_data=cur.fetchall()
 return products_data


def insert_products(prod_details):
 cur.execute("insert into products(name,buying_price,selling_price) values(%s,%s,%s)",prod_details)
conn.commit()


product1=('iphone 14',50000,60000)
product2=('rice',200,250)
insert_products(product1)
insert_products(product2)


products_data=get_products()
print(products_data)

def fetch_sales():
 cur.execute("select * from sales")
 sales_data=cur.fetchall()
 return sales_data



def insert_sales(sales_details):
 cur.execute("insert into sales(pid,quantity) values(%s,%s)",sales_details)
conn.commit()


sales1=(14,60)
sales2=(10,50)
insert_sales(sales1)
insert_sales(sales2)

sales_data=fetch_sales()
print(sales_data)

def get_sales_per_product():
 cur.execute(
    """
        select products.name as p_name,sum(products.selling_price * sales.quantity) as total_sales
        from sales join products on products.id = sales.pid group by p_name;
    """)
 sales_per_product = cur.fetchall()
 return sales_per_product


sales_per_product = get_sales_per_product()
print(sales_per_product)


 #fetch stock data
def fetch_stock():
    cur.execute("select * from products;")
    stock = cur.fetchall()
    return stock
 
 
# 2. insert stock data using parameters
def insert_stock(name, buying_price, selling_price,quantity):
    cur.execute(
        """
        insert into products (name, buying_price, selling_price)
        values (%s, %s, %s);
        """,
        (name, buying_price, selling_price),
    )
    conn.commit()

 #3a. sales per day
def get_sales_per_day():
    cur.execute(
        """
        select date(sales.created_at) as day,
               sum(products.selling_price * sales.quantity) as total_sales
        from sales join products on products.id = sales.pid
        group by day
        order by day;
        """
    )
    sales_per_day = cur.fetchall()
    return sales_per_day
 
 
# 3b. profit per product
def get_profit_per_product():
    cur.execute(
        """
        select products.name as p_name,
               sum((products.selling_price - products.buying_price) * sales.quantity) as profit
        from sales join products on products.id = sales.pid
        group by p_name;
        """
    )
    profit_per_product = cur.fetchall()
    return profit_per_product
 
 
# 3c. profit per day
def get_profit_per_day():
    cur.execute(
        """
        select date(sales.created_at) as day,
               sum((products.selling_price - products.buying_price) * sales.quantity) as profit
        from sales join products on products.id = sales.pid
        group by day
        order by day;
        """
    )
    profit_per_day = cur.fetchall()
    return profit_per_day
 
 
insert_stock("Sugar 1kg", 150, 180, 50)
 
print(fetch_stock())
print(get_sales_per_day())
print(get_profit_per_product())
print(get_profit_per_day())
 

