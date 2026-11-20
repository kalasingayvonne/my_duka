from database import get_products

products=get_products()
print(products)


for i in products:
    print(i[0])