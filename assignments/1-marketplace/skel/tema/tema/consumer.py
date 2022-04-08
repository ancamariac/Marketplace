"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import time
from threading import Thread

from tema.marketplace import Marketplace


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    carts: list
    marketplace: Marketplace
    retry_wait_time: float

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        Thread.__init__(self, **kwargs)

    def run(self):
        id = self.marketplace.new_cart()

        for orders in self.carts:
            for order in orders:
                if order["type"] == "add":
                    i = 0
                    while i < order["quantity"]:
                        check = self.marketplace.add_to_cart(id, order["product"])
                        if check == True:
                            i += 1
                        else:
                            time.sleep(self.retry_wait_time)

                elif order["type"] == "remove":
                    for i in range(order["quantity"]):
                        self.marketplace.remove_from_cart(id, order["product"])

        for product in self.marketplace.place_order(id):
            print(self.getName(), "bought", product)
