"""
Module of Customer class for the Markov chain simulation
"""

import numpy as np

class Customer:
    """Constructs a customer with its movement probabilities"""
    def __init__(self, customer_no):
        self.customer_no = customer_no
        self.location = "entrance"
        self.active = True
        #### Adding variable for visualisation
        self.prior_location = 'entrance'
        #### Adding variable for visualisation
        self.geo_x = np.random.choice(range(70,120))
        self.geo_y = np.random.choice(range(0,15))
        self.probs = {"checkout" : [1, 0, 0, 0, 0,],
                    "dairy" : [0.103, 0.737, 0.059, 0.050, 0.051],
                    "drinks" : [0.216, 0.0110000000000001, 0.598, 0.088, 0.087],
                    "entrance" : [0.000, 0.288, 0.154, 0.377, 0.181],
                    "fruit" : [0.202, 0.096, 0.055, 0.597, 0.050],
                    "spices" : [0.151, 0.193, 0.163, 0.091, 0.402]
                    }
        
        
    def __repr__(self):
        return f'This is customer number {self.customer_no} at {self.location}'

    def is_active(self):
        """Checks customer location and updated the active attribute accordingly"""
        if self.location == 'checkout':
            self.active = False
        return None
    
    #### Function to locate customer visualy #####
    def update_geolocation(self):
        """This function returns new coordinates, if the customer changed locations. 

        Returns:
            None: The tuple self.geo will be adapted with random numbers within a threshholded location
        """
        #### Constant dictionary representing X and Y values ranges on the later supermarket plot
        LOCATION_COORDINATES = {"checkout": [0,50,0,10],
                                "dairy": [38,45,25,45],
                                "drinks":[10,21,25,45],
                                "entrance":[90,100,0,10],
                                "fruit": [90,100,25,45],
                                "spices": [68,78,25,45],
                                }
        #### If location did not change, keep your location, else get assigned new locations randomly 
        # (based on the valid coordinate ranges of the location itself)
        if self.location != self.prior_location:
            self.geo_x = np.random.choice(range(LOCATION_COORDINATES[self.location][0],LOCATION_COORDINATES[self.location][1]))
            self.geo_y = np.random.choice(range(LOCATION_COORDINATES[self.location][2],LOCATION_COORDINATES[self.location][3]))
        return None

    def move(self):
        """Moves the customer around the supermarket based on the probabilities matrix"""
        if self.active:
            self.prior_location = self.location
            self.location = np.random.choice(["checkout","dairy",
                                              "drinks","fruit",
                                              "spices"],p=self.probs[self.location])
            self.update_geolocation()
            return None
        else:
            print('Error: A checked out customer tries to move')
