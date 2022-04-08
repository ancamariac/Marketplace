"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from tema.marketplace import Marketplace
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """
    products: list
    marketplace: Marketplace
    republish_wait_time: float

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        Thread.__init__(self, **kwargs)

    def run(self):
        id = self.marketplace.register_producer()
        while True:
            for product in self.products:
                i = 0
                while i < product[1]:
                    check = self.marketplace.publish(id, product[0])
                    if check == True:
                        i += 1
                        time.sleep(product[2])
                    else:
                        time.sleep(self.republish_wait_time)


