from flask import Flask, render_template, request, redirect, url_for, session,flash
from database import (
    get_products, insert_products,
    fetch_sales, insert_sales,
    fetch_stock, insert_stock,
    get_sales_per_product, get_profit_per_product,
    get_profit_per_day, get_sales_per_day,
    insert_user,check_user_exists,
  
)
from flask_bcrypt import  Bcrypt
# flask instance
app = Flask(__name__)


bcrypt = Bcrypt(app)
app.secret_key = '00emnd03ii09fj300wjdj92djjffkfkkffg' # needed for session to work


@app.route('/')  # decorator func
def home():  # view func
    return render_template('index.html')


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['p_name']
        buying_price = request.form['b_price']
        selling_price = request.form['s_price']
        insert_products((name, buying_price, selling_price))
        return redirect(url_for('products'))

    products_data = get_products()
    return render_template('products.html', products_data=products_data)


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        pid = request.form['pid']
        quantity = request.form['quantity']
        insert_sales(pid, quantity)
        return redirect(url_for('sales'))

    sales_data = fetch_sales()
    products_data = get_products()
    return render_template('sales.html', sales_data=sales_data, products_data=products_data)


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        pid = request.form['pid']
        stock_quantity = request.form['stock_quantity']
        insert_stock(pid, stock_quantity)
        return redirect(url_for('stock'))

    stock_data = fetch_stock()
    products_data = get_products()
    return render_template('stock.html', stock_data=stock_data, products_data=products_data)


@app.route('/dashboard')
def dashboard():
    product_sales = get_sales_per_product()
    daily_sales = get_sales_per_day()

    product_profit = get_profit_per_product()
    daily_profit = get_profit_per_day()

    product_names = [i[0] for i in product_sales]
    sales_p = [ float(i[1]) for i in product_sales]
    profit_p = [float(i[1]) for i in product_profit]


    days = [ str(i[0]) for i in daily_sales ]
    sales_day = [ float(i[1]) for i in daily_sales ]
    profit_day = [ float(i[1]) for i in daily_profit ]
    
    return render_template('dashboard.html',
        product_names = product_names ,sales_p = sales_p, profit_p = profit_p,
        days= days, sales_day = sales_day, profit_day = profit_day                 
                           )



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = check_user_exists(email) 

        if not existing_user:
            flash("User with this email doesn't exist,register instead",'danger')
            return redirect(url_for('register'))
        else:
            check_password = bcrypt.check_password_hash(existing_user[-1],password)
            if check_password:
                flash("Logged in successfully",'success')
                redirect(url_for('dashboard'))
            else:
                flash("Incorrect password ,try again",'danger')
                return redirect(url_for('login'))


    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
      if request.method == "POST":

        full_name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        existing_user = check_user_exists(email)

        if existing_user :
            flash("User already exists,login instead",'danger')
            return redirect(url_for('login'))
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = (full_name,email,phone,hashed_password)
            insert_user(new_user)
            flash("User registered succesfully",'success')
            return redirect(url_for('login'))

      return render_template('register.html')




# starts server to run app
if __name__ == '__main__':
    app.run(debug=True)