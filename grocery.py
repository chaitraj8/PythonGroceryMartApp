# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 22:16:31 2022

@author: kulka
"""

import time
import json

class Grocery_mart:
    
    __INVENTORY_THRESHOLD = {'Milk':100,
                           'Eggs':300,
                           'Bread':150,
                           'Apples':300,
                           'Tomatoes':300,
                           'Coffee': 200,
                           'Juice':300}
    
    ''' This class is used to keep track of groceries and operate on the grocery'''
    
    #init to initialize few variables
    def __init__(self,inventory_file,grocery_name = "Hannaford"):
        ''' Instantiate variables'''
        self.__inventory_file = inventory_file
        self.grocery_name = grocery_name
        self.sales_dict = {}        
        with open(self.__inventory_file, 'r') as f:
            self.data = json.load(f)  
        self.unique_items = self.data.keys()
    
    #this method capitalizes items if we write everything as small. Called in different methods
    def __capitalize(self, item):
        return item.strip().capitalize()
    
    #Gets user input if want to repeat for more than one item
    def __get_user_input(self):
         return input("\nDo you want to enter more items? (yes or no):")
    
    #Checks if entered item is present in the json
    def __check_item_present(self, item):
        if item not in self.data.keys():
            return False
        else:
            return True
    
    #Checks for quantity value and handles if entered quantity is not digit or is a negative number
    def __check_quantity(self, quantity):
        if not quantity.isdigit():
            print('\nEnter Quantity as number')
            return None
        if int(quantity) <= 0:
            print ('\nEnter Quantity greater than zero')
            return None
        else:
            return int(quantity)
    
    #Returns the complete data list with all attributes
    def __repr__(self):
        return f'\nImplementation of repr() function below :\nItems present in {self.grocery_name} are {list(self.unique_items)}'
    
    #Magic method used to round the total bill upto 2 decimal
    def __round__(self, para):
        return round(para, 2)
    
    #displays only item and skuid from the dataframe for the manager to see what items are present.
    def display_grocery_items(self):
        ''' Displays grocery items'''
        print("\n")
        print("--------------Grocery Items List-------------")
        print('{:5s} {:10s}  {:8s} {:6s}'.format("SKUID","ITEM","QUANTITY","UNIT"))
        print("---------------------------------------------")
        for _, row in self.data.items():
            print('{:5d} {:10s}  {:8d} {:6s}'.format(row['SKUID'], 
                                                 row['ITEM'], row['QUANTITY'],
                                                 row['UNIT']))

        return 
    
    
    def check_grocery_items(self):
        '''Checks if entered grocery item is present in the mart and gives how much 
        quantity is present in which isle'''
        self.display_grocery_items()
        time.sleep(1)
        Flag = True
        while (Flag):
            user_input = input("\nEnter the items you wish to see seperated by commas:")
            list_of_items = user_input.split(",")
            for item in tuple(list_of_items):
                item = self.__capitalize(item)
                if item in self.data.keys():
                    isle = self.data[item]['ISLE']
                    display_message = item+" is present in isle "+ isle + "."
                    print(display_message)
                    Flag = False
                else:
                    print(item,"not in the inventory at our store or please check the spelling")
                    continue
        return display_message            
     
            
    def update_inventory(self):
        ''' Updates the inventory if the items are  getting over in the stock'''
        while(True):
            item_quantity_input = input("Enter the item you wish to order and its quantity seperated by space :")
            try:
                item_input, quantity_input = item_quantity_input.split(' ')
            except:
                print("\nEnter item and Quantity seperated by space")
            else:
                item = self.__capitalize(item_input)
                if self.__check_item_present(item):
                    quantity_of_item = self.data[item]['QUANTITY']
                else:
                    print("\nItem Unavailable: Please enter item that is present in inventory")
                    continue
                #Check if input isdigit() and greater than zero
                quantity_input = self.__check_quantity(quantity_input)                
                if not quantity_input:
                    continue                         
                if quantity_of_item + quantity_input  >= self.__INVENTORY_THRESHOLD[item]:
                    print("Maximum limit reached. Can only accomodate {} more"
                      .format(self.__INVENTORY_THRESHOLD[item] - quantity_of_item))
                    continue               
                else:
                    self.data[item]['QUANTITY'] = quantity_of_item + quantity_input
                    #save json
                    with open(self.__inventory_file, 'w') as file:
                        json.dump(self.data, file)    
                    print("Inventory updated with latest data")
                    self.display_grocery_items()
                more_items = self.__get_user_input()            
                if more_items == 'yes':
                    continue   
                else:    
                    print("\nThank you for updating.Come back soon for more updates")
            break
        return None
     
    #Sell computes the amount and updates the price for the quantity being purchased
    def __sell(self,item,quantity):
        item_price = self.data[item]['PRICE']
        unit = self.data[item]['UNIT']        
        price_amount = self.__round__(float(quantity) * item_price)        
        print("Total cost for {} {} {} = ${}".format(quantity, unit, item , price_amount))        
        if item in self.sales_dict.keys():
            self.sales_dict[item] = self.sales_dict[item] + price_amount
        else:
            self.sales_dict[item] = price_amount
        return None
    
    # Updates the total sales value and quantity of the item after being sold
    def __update_sales(self,item,quantity):
        present_sales = self.data[item]['TOTAL SALES']
        actual_quantity = self.data[item]['QUANTITY']
        self.data[item]['TOTAL SALES'] = self.__round__(present_sales + self.sales_dict[item])
        self.data[item]['QUANTITY'] = int(actual_quantity) - quantity
        #save json
        with open(self.__inventory_file, 'w') as file:
            json.dump(self.data, file)       
        print("Inventory updated with latest sales and quantity")
        self.display_grocery_items()
        return None
    
    #Computes the total bill for the customer who purchased several items
    def __get_total_bill(self):
        print ("--------------------")
        print ("\tTotal Bill\t")
        print ("--------------------")
        print ("Items\t\tAmount")
        for key_value in self.sales_dict.items():
            print ("{}\t\t${}".format(key_value[0],key_value[1]))
        print ("--------------------")
        totalsum = round(sum(self.sales_dict.values()),2)
        print ("Total Bill to be paid = ${}".format(totalsum))
        return totalsum

    def sales(self):
        '''Gives all the sales details when customer purchases any item, also displays bill and 
        updates the quantity in th csv file back'''
        while(True):
            item_quantity = input("\nEnter the item you wish to sell and its quantity seperated by space :")
            try:
                item, quantity = item_quantity.split(' ')
            except:
                print("\nEnter item and Quantity seperated by space")
            else:
                item = self.__capitalize(item)               
                if self.__check_item_present(item):
                    quantity_of_item = self.data[item]['QUANTITY']
                else:
                    print("\nItem Unavailable: Please enter item that is present in inventory")
                    continue
                quantity_of_item = self.data[item]['QUANTITY']
                quantity_input = self.__check_quantity(quantity)                
                if not quantity_input:
                    continue                
                if quantity_of_item < quantity_input:
                    print("\nNot enough Quantity to sell")
                else:
                    self.__sell(item,quantity_input)
                    self.__update_sales(item,quantity_input)
                more_items = self.__get_user_input()
                if more_items.strip() == 'yes':
                    continue   
                else:
                    total_bill = self.__get_total_bill()
                    print("\nThank you for purchasing. Visit us again")
                break
        return total_bill
