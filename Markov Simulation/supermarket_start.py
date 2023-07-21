"""
Module of Supermarket class for the Markov chain simulation.
"""

import csv
import numpy as np
from class_customer import Customer


class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

######### Initiation with possible own open times #####
    def __init__(self,brand = 're-netto', start='07:00', closed='22:00'):
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.last_id = 0
        self.name = brand
        self.opening_time = start
        self.closing_time = closed

#####  Added __repr__ by GK
    def __repr__(self):
        return f'''This is a supermarket object of the brand {self.name}.
                It is opened from {self.opening_time} to {self.closing_time}'''

#####  Added parmameter closing time by GK
    def is_open(self):
        """Method to check if the supermarket is open"""
        return self.get_time() != self.closing_time

    def get_time(self):
        """current time in HH:MM format,
        """
        hour = 7 + self.minutes // 60
        minutes = self.minutes % 60
        timestamp = f"{hour:02d}:{minutes:02d}"
        return timestamp

    def print_customers(self, to_csv=False):
        """print all customers with the current time, id, location in CSV format.
        params: to_csv True/False to output the results to a csv file. It takes
        the simulation name defined on Brand for the file name and append the results.
        """
        for customer in self.customers:
            print(f"{self.get_time()}, {customer.customer_no}, {customer.location},{customer.geo_x},{customer.geo_y}")
            if to_csv:
                row = [self.get_time(),customer.customer_no,customer.location]
                with open(f're-netto-project/data/{self.name}_simulation.csv', 'a',
                        encoding='UTF8') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)

    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.minutes = self.minutes + 1
        for customer in self.customers:
            customer.move()

    def remove_exitsting_customers(self):
        """removes every customer that is not active any more"""
        for customer in self.customers:
            customer.is_active()
            if customer.active:
                pass
            else:
                self.customers.remove(customer)

##### Added new customer by GK
    def add_new_customers(self, cust_number=1):
        """randomly creates new customers."""
        # if wanted, controll Number of executions
        for _ in range(cust_number):
            # exclusion list to secure unique numbers
            number_taken = []
            unique = False
            for customer in self.customers:
                number_taken.append(customer.customer_no)
            # loop while number is not unique
            while not unique:
                number = np.random.choice(range(9999))
                # if number not taken, create a customer with it
                if number not in number_taken:
                    self.customers.append(Customer(number))
                    unique = True
