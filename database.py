import psycopg2

conn = psycopg2.connect(host='localhost', port=5434, user='postgres', password='4725', dbname='myduka_db')
cur = conn.cursor()


def get_products():
    cur.execute("select * from products")
    products_data = cur.fetchall()
    return products_data


def insert_products(prod_details):
    cur.execute("insert into products(name,buying_price,selling_price) values(%s,%s,%s)", prod_details)
    conn.commit()


def fetch_sales():
    cur.execute("select * from sales")
    sales_data = cur.fetchall()
    return sales_data


def insert_sales(pid, quantity):
    cur.execute("insert into sales(pid,quantity) values(%s,%s)", (pid, quantity))
    conn.commit()


def get_sales_per_product():
    cur.execute(
        """
        select products.name as p_name, sum(products.selling_price * sales.quantity) as total_sales
        from sales join products on products.id = sales.pid group by p_name;
        """
    )
    sales_per_product = cur.fetchall()
    return sales_per_product


def fetch_stock():
    cur.execute(
        """
        select stock.id, products.name, stock.stock_quantity, stock.created_at
        from stock join products on products.id = stock.pid
        order by stock.created_at desc;
        """
    )
    stock_data = cur.fetchall()
    return stock_data


def insert_stock(pid, stock_quantity):
    cur.execute(
        "insert into stock(pid, stock_quantity) values (%s, %s)",
        (pid, stock_quantity),
    )
    conn.commit()


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

def check_user_exists(email):
    cur.execute('select * from user where users.email = %s',(email,))
    user = cur.fetchone()
    return user











def insert_user(user_details):
    cur.execute("insert into users(full_name,email,phone_number,password)values(%s,%s,%s,%s)",user_details)
    conn.commit()