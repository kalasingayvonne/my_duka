# Concepts Behind MyDuka

This document covers the core concepts applied while building MyDuka, Flask fundamentals, PostgreSQL integration, authentication, and the reasoning behind key design decisions.

## 1. Flask Basics

Flask is a Python **framework**, a set of prebuilt tools for building applications quickly, while requiring developers to follow its conventions (as opposed to a **library**, which is more flexible but requires more setup).

- **Routing** maps URLs to Python functions using the `@app.route()` decorator.
- Each route is paired with a **view function** that returns a response.
- `app.run()` starts a local development server.

```python
@app.route('/products')
def products():
    return "Products Page"
```

Every view function in the app must have a **unique name**, since Flask uses it internally as the route's endpoint.

## 2. Templates and Jinja

Instead of returning plain text, Flask apps return full HTML pages using `render_template()`. These HTML files live in a `templates/` folder, and static assets (CSS, JS, images) live in `static/`.

**Template inheritance** avoids repeating the same navbar and footer on every page:
- A `base.html` defines shared structure using `{% block content %}{% endblock %}`
- Other pages extend it: `{% extends 'base.html' %}`

**Jinja syntax:**
- Variables: `{{ variable }}`
- Control structures: `{% for x in list %} ... {% endfor %}`, `{% if condition %} ... {% endif %}`

## 3. Connecting to PostgreSQL with psycopg2

`psycopg2` is a database adapter that connects Python to PostgreSQL.

```python
conn = psycopg2.connect(host='localhost', port=5432, user='postgres', password='...', dbname='myduka_db')
cur = conn.cursor()
```

- `cur.execute()` runs a SQL query
- `cur.fetchall()` returns all matching rows as a **list of tuples**
- `cur.fetchone()` returns a single tuple
- `conn.commit()` saves changes (required after any INSERT, UPDATE, or DELETE)

Parameterized queries (`%s` placeholders) are used instead of string-formatting SQL directly, this prevents SQL injection:

```python
cur.execute("INSERT INTO products (name, buying_price, selling_price) VALUES (%s, %s, %s)", (name, buying_price, selling_price))
```

## 4. Querying Across Tables

Reports like "sales per product" or "profit per day" require joining `sales` and `products`:

```sql
SELECT products.name AS p_name, SUM(products.selling_price * sales.quantity) AS total_sales
FROM sales
JOIN products ON products.id = sales.pid
GROUP BY p_name;
```

## 5. Handling Form Submissions (POST)

1. A form is rendered with `method="POST"` and `action="/route_name"`
2. Flask reads submitted data via `request.form['field_name']`, where `field_name` matches the form input's `name` attribute
3. The extracted data is passed to an insert function
4. The user is redirected using `redirect(url_for('route_name'))`

**HTTP methods used in this project:**
- `GET` — retrieve and display data (e.g. viewing products)
- `POST` — submit new data (e.g. recording a sale)

## 6. Authentication

**Registration flow:** collect user details → check if the email already exists → hash the password → insert the new user → flash a success message → redirect to login.

**Login flow:** collect credentials → check if the user exists → compare the hashed password → store user info in the session → redirect to the dashboard.

**Password hashing** (via `flask_bcrypt`) converts a plain-text password into an irreversible hash before storing it. The same password always produces the same hash, allowing safe comparison without ever storing the original password.

- **Salting** adds random data to a password before hashing, making precomputed "rainbow table" attacks far less effective.
- Hashing is one-way: a hash can be verified against a password, but never reversed back into the original password.

## 7. Flash Messaging and Sessions

Flash messages are one-time notifications (success, error, warning, info) shown after an action, stored temporarily in the session. They require a Flask `secret_key` to work securely.

## 8. Dashboard and Data Visualization

- **Line chart:** sales/profit per day (x-axis: day, y-axis: amount)
- **Bar chart:** sales/profit per product (x-axis: product name, y-axis: amount)

## 9. Object-Oriented Programming (OOP)

OOP organizes programs around **classes** (blueprints) and **objects** (instances of those classes). Every class has:
- **Identity** — its name
- **State** — its attributes (variables)
- **Behaviour** — its methods (functions)

Core OOP concepts: inheritance, encapsulation, abstraction, and polymorphism.

## Database Schema

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    buying_price NUMERIC(20,2) NOT NULL CHECK (buying_price >= 0),
    selling_price NUMERIC(20,2) NOT NULL CHECK (selling_price >= 0)
);

CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    pid INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    pid INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);
```
