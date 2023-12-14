# import libraries
import requests
from bs4 import BeautifulSoup
import mysql.connector

# getting the input
x = input("Car's name: ")
if '-' in x:
    f = x.split('-')
    f = f[0] + f[1]
else:
    f = x

# scraping data
r = requests.get('https://www.truecar.com/used-cars-for-sale/listings/%s/' %(x))
soup = BeautifulSoup(r.text,'html.parser')
adds = soup.find_all('div',class_="card-content order-3 vehicle-card-body",limit=30)

mydb = mysql.connector.connect(user='root', password='sh.bisto5',
                                  host='localhost',
                                  database= 'cardb')
mycursor = mydb.cursor()

# if the table already elxists, drop the table and create a new one
try:
    mycursor.execute('CREATE TABLE %s(id MEDIUMINT AUTO_INCREMENT, model VARCHAR(200) NOT NULL,price VARCHAR(200) NOT NULL,mileage VARCHAR(200) NOT NULL, PRIMARY KEY (id));' %f)
except:
    mycursor.execute('DROP TABLE %s' %f)
    mycursor.execute('CREATE TABLE %s(id MEDIUMINT AUTO_INCREMENT, model VARCHAR(200) NOT NULL,price VARCHAR(200) NOT NULL,mileage VARCHAR(200) NOT NULL, PRIMARY KEY (id));' %f)
a = mycursor.fetchall()

# inserting data into database
for add in adds:
    model = add.find('div',{'class': ['vehicle-card-header', 'w-full'], 'data-test': 'vehicleCardYearMakeModel'})
    model1 = model.find_next('span',class_="truncate").text
    price = add.find('div',class_="vehicle-card-bottom-pricing-secondary pl-3 lg:pl-2 vehicle-card-bottom-max-50").text
    func = add.find_next('div',{'class': ['truncate', 'text-xs'], 'data-test': 'vehicleMileage'}).text
    price = price.split('$')
    mycursor.execute("INSERT INTO %s(model,price,mileage) VALUES('%s','%s dollors','%s');" %(f,model1,price[1],func))
    s = mycursor.fetchall()
mydb.commit()
mycursor.close()