from flask import Flask, render_template, request, redirect, url_for, session
from database import (
    get_products, insert_products,
    fetch_sales, insert_sales,
    fetch_stock, insert_stock,
    get_sales_per_product, get_profit_per_product,
    get_profit_per_day, get_sales_per_day
)

# flask instance
app = Flask(__name__)
app.secret_key = 'change-this-to-any-long-random-text'  # needed for session to work


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
    sales_per_product = get_sales_per_product()
    profit_per_product = get_profit_per_product()
    profit_per_day = get_profit_per_day()
    sales_per_day = get_sales_per_day()
    return render_template(
        'dashboard.html',
        sales_per_product=sales_per_product,
        profit_per_product=profit_per_product,
        profit_per_day=profit_per_day,
        sales_per_day=sales_per_day
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # TODO: check the user against your database here
        session['user'] = email
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # TODO: save the new user to your database here (hash the password!)
        return redirect(url_for('login'))
    return render_template('register.html')


# starts server to run app
if __name__ == '__main__':
    app.run(debug=True)