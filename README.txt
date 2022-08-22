1. Import JSON , SYS and TIME modules from Python standard library
2. Keep grocery.py , Inventory_Marlboro.json, Inventory_Northboro.json and main.py in same folder
3. Run main.py file
3. There are 2 unit tests, one for check_grocery_items() method and other for sales() method
4. Since the code is dynamic and output of each method is based on user input, assert statements need to be changed accordingly.

Current unit test is written for following input

1. To test check_grocery_items() method:
	-select M when prompted to select store
	-C when prompted to enter choice
	-enter 'Milk' to pass the unit test in any format(eg: milk, MILK)
	
2. To test sales() method:
	-select N when prompted to select store
	-S when prompted to enter choice
	-enter 'Milk 5' when prompted to enter item and quantity
	-enter 'yes' when prompted to sell more items
	-enter 'Coffee 2' when prompted to enter item and quantity
	-enter 'no' when prompted to sell more items

Comment out assert statements in line 63 and 66 in main.py to run for different set of inputs to see the overall functionality of application.