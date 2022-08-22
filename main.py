# -*- coding: utf-8 -*-
"""
Chaitra Joshi
Class: CS 521 - Summer 21
Date: 08/15/2022
Python Project
"""
import grocery
import sys
import time
     
#Method to select any one of the two outlets of Hannaford
def select_store():
    while (True):
        time.sleep(1)
        store = input("Select store you want to Manage (M for Marlboro or N for Northboro): ")
        store = store.capitalize()
        if store.strip() == 'M':
            print("\nYou are viewing Hannford Marlboro")
            return store.strip()
        elif store.strip() == 'N':
            print("\nYou are viewing Hannford Northboro")
            return store.strip()
        else:
            print ('Please Enter either M or N')
            continue

def union(Marlboro,Northboro):
    items_set = set(Marlboro.unique_items).union(set(Northboro.unique_items))
    print ('\nItems present in both the outlets',items_set)
    return None
    

if __name__ == "__main__":
    
    Marlboro = grocery.Grocery_mart("Inventory_Marlboro.json","Hannaford_Marlboro")
    Northboro = grocery.Grocery_mart("Inventory_Northboro.json","Hannaford_Northboro")
    store_dict =  {'M': Marlboro,
                'N': Northboro}
    user_store = select_store()
    
    while True:
        try:
            user_selection = input("\nPress\nC to Check items in store\n"+
                                   "S to Sell items\n"+
                                   "U to Update item inventory\n"+
                                   "A to Switch between store\n"+
                                   "D to Check items in all outlets\n"+
                                   "P to View store object\n"+
                                   "E to Exit\n"+
                                   "Enter your choice : ")
            user_selection = user_selection.capitalize()
            
        except ValueError:
            print("\nERROR: Choose only alphabets from the given option")
            continue
        else:
             
            
            store_object = store_dict[user_store.strip()]
            if user_selection == 'C':
                message = store_object.check_grocery_items()
                #assert message == "Milk is present in isle A1.", "check_grocer_items: Display message not matching"
            elif user_selection == 'S':
                total_value = store_object.sales()
                #assert total_value == 15.43, "sales: Total bill is not matching"
            elif user_selection == 'U':
                store_object.update_inventory() 
            elif user_selection == 'A':
                 user_store = select_store()
            elif user_selection == 'D':
                union(Marlboro, Northboro)
            elif user_selection == 'P':
                print(store_object)
            elif user_selection == 'E':
                sys.exit()
            