from datetime import datetime
from decimal import Decimal as dc
import unittest
import csv

class Medadrangi:
    longitude = dc("35.74317403843504")
    latitude = dc("51.50185488303431")
    Off_rate = 0.1
    def input_checker (instance, type):
        """In this method we check the input and if it was'nt the type that is needed it will raise TypeError"""
        if not isinstance(instance, type):
            raise TypeError(f'Input must be {type}')

    def __init__(self, name: str, price: int, amount: int, made_in: str, factory: str):
        """IN init first off all we check the inputs using input_checker method and then assign them to the object"""
        Medadrangi.input_checker(name, str)
        Medadrangi.input_checker(price, int)
        Medadrangi.input_checker(amount, int)
        Medadrangi.input_checker(made_in, str)
        Medadrangi.input_checker(factory, str)
        if len(name) == 0 or len(made_in) == 0 or len(factory) == 0:
            raise ValueError("Input shoul not be empty") 
        self.name = name
        self.price = price
        self.amount = amount
        self.made_in = made_in
        self.factory = factory
        
        with open("D:\projects\OOP2\Products.csv", "r") as prdct:
            products_reader = csv.DictReader(prdct)
            product = {"name" : self.name, "price" : self.price, "amount" : self.amount, "made_in" : self.made_in, "factory" : self.factory}
            result = False
            for line in products_reader :
                if line["name"] == self.name and line["price"] == (str(self.price)).strip() and line["made_in"] == self.made_in and line["factory"] == self.factory:
                    specific_product = line.copy()
                    result = True
                    m = []
                    for prod in products_reader:
                        if prod != line:
                            m.append(prod)

                    specific_product["amount"] = int(specific_product["amount"]) + self.amount
                    with open("D:\projects\OOP2\Products.csv", "w") as prdc:
                        fieldname = ["name", "price", "amount", "made_in", "factory"]
                        product_writer = csv.DictWriter(prdc, fieldnames=fieldname)
                        product_writer.writeheader()
                        for line in m :
                            product_writer.writerow(line)
                        product_writer.writerow(specific_product)
                        
            if not result:
                with open("D:\projects\OOP2\Products.csv", "a") as prdc:
                    fieldname = ["name", "price", "amount", "made_in", "factory"]
                    product_writer = csv.DictWriter(prdc ,fieldnames=fieldname)
                    product_writer.writerow(product)

    
            
    def final_price (self):
        """IN this mehtod we will return the price after off"""
        return self.price - (Medadrangi.Off_rate*self.price)


    def welcome ():
        now = datetime.now()

        if 6 <= now.hour <= 12:
            return "صبح بخیر"
        elif  12 < now.hour <= 18:
            return "ظهر بخیر"
        else:
            return "عصر بخیر"
    
    def calculate_distance (longitude: dc, latitude: dc):
        Medadrangi.input_checker(longitude, dc)
        Medadrangi.input_checker(latitude, dc)
        pos = (latitude, longitude)
        medadrangi_pos = (Medadrangi.latitude, Medadrangi.longitude)
        return ((medadrangi_pos[0] - pos[0])**2 + (medadrangi_pos[1] - pos[1])**2)**dc("0.5")
    

    def load_csv (path):
        with open (f'{path}', "r") as file :
            csv_reader = csv.DictReader(file)
            with open("Products.csv", "w") as products : 
                products_writer = csv.DictWriter(products)
                for product_information in csv_reader:
                    products_writer.writerow(product_information)

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

class Testclass(unittest.TestCase):

    def test_creating_class1 (self):
        product = Medadrangi("Pencile", 1500, 10, "Iran", "Kian")
        self.assertEqual("Pencile", product.name)
        self.assertEqual("Iran", product.made_in)
        self.assertEqual("Kian", product.factory)
        self.assertEqual(1500, product.price)
        self.assertEqual(1350, product.final_price())
    
    def test_creating_class2 (self):
        with self.assertRaises(TypeError):
            product = Medadrangi("Pen", 12000, 120, 1656, "K&L")
    
    def test_creating_class (self):
        with self.assertRaises(ValueError):
            prodict = Medadrangi("", 1200, 1500, "Iran", "Bankok")
        with self.assertRaises(TypeError):
            prodict = Medadrangi("", 1200, 1500, 156, "Bankok")

    def test_final_price_calculator (self):
        product1 = Medadrangi("Eraser", 13000, 152, "Turkey", "Gardash")
        product2 = Medadrangi("Pen", 15000, 200, "Austrailia", "KKK")
        self.assertEqual(11700, product1.final_price())
        self.assertEqual(13500, product2.final_price())
    
    def test_calculate_dictance (self):
        distance = Medadrangi.calculate_distance(dc("10"), dc("20"))
        self.assertEqual(distance,dc("40.68264827472405891338410901"))

run_tests(Testclass)
