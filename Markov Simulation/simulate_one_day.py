"""
Script to create a supermarket simulation
"""

from supermarket_start import Supermarket
from class_plot_market import PlotMarket

re_netto = Supermarket(brand = 're-netto_2', start='07:00', closed ='22:00')

while re_netto.is_open():
    re_netto.add_new_customers()
    re_netto.print_customers(to_csv=False)
    re_netto.next_minute()
    re_netto.remove_exitsting_customers()

