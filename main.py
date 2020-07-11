from datetime import datetime, timedelta
from Hash_Table import HashTable
from Package import Package 
from Truck import Truck
import re

# Creates the global variables for this project (Hash Table, Time, Trucks)
receiveing = HashTable()
global_time = datetime(2020,1,1,8,00)
truck1 = Truck(receiveing.handload_truck_1(), datetime(2020,1,1,9,5), 1, receiveing)
truck2 = Truck(receiveing.handload_truck_2(), datetime(2020,1,1,8,00), 2, receiveing)
truck3 = Truck(receiveing.handload_truck_3(), datetime(2020,1,1,23,59), 3, receiveing)



# Needs finalization
def run_deliveries(delivery_time = datetime(2020,1,1,23,59)):
    '''Runs all deliveries, printing the result.'''
    global global_time

    while global_time < delivery_time:

        #
        if truck3.status == 'AT HUB, START OF DAY' and truck2.status == 'Deliveries complete' or truck1.status == 'Deliveries complete':
            truck3.time = global_time

        # Update package 9 at 10:20 AM
        if global_time == datetime(2020,1,1,10,20):
            receiveing.update_package_nine()

        #
        if global_time == truck1.time:
            truck1.tick()
        if global_time == truck2.time:
            truck2.tick()
        if global_time == truck3.time:
            truck3.tick()


        if truck1.status == 'Deliveries complete' and truck2.status == 'Deliveries complete' and truck3.status == 'Deliveries complete':
            break

        #
        global_time  += timedelta(0, 20)

    # Sets Global time to equal deliver time, 
    #  in case the delivery time exceeds time needed to deliver packages
    global_time = delivery_time

# Needs finalization
def deliver_packages_to_time():

    # 
    input_time = input("Please enter a time in hours and minute [hh:mm]\nOr press <enter> to set time to EOD            - ")
    match = re.match(r'(\d+)\D+(\d+)', input_time)

    if match and match.lastindex == 2:
        hour = int(match.group(1))
        minute = int(match.group(2))
        run_deliveries(datetime(2020,1,1,hour,minute))
    else:
        run_deliveries()

# Needs finalization
def create_new_package():
    '''
    Prompts user for package details
    '''
    global receiveing

    print("Please enter package details below.")
    address = input("Address: ")
    city = input("City: ")
    state = input("State: ")
    zip_code = input("Zip: ")
    weight = input("Weight: ")
    deadline = input("Deadline: ")
    instructions = input("Instructions: ")
    package_id = -1
    address_id = -1

    # Find empty bucket in Hash Table, get index for package_id
    for i in range(len(receiveing.package_table)):
        print(f'Index {i} is type {type(receiveing.package_table[i])}')
        if type(receiveing.package_table[i]) != Package:
            print(f'Index {i} is free!')
            package_id = i
            break
        
    # If no empty bucket was found, then hash table full.  
    # Inform user and exit function
    if package_id == -1:
        print('NO MORE ROOM IN HASH TABLE')
        return

    # Find matching address ID for package
    if receiveing.lookup_packages('address', address):
        address_id = receiveing.lookup_packages('address', address)[0].address_id
    else:
        address_id = receiveing.num_addresses

    
    # Create package
    package = Package(package_id)
    package.address_id = address_id
    package.address = address
    package.city = city
    package.state = state
    package.zip_code = zip_code
    package.weight = weight
    package.deadline = deadline
    package.instructions = instructions

    print(f'Package address ID = {package.address_id}')
    receiveing.insert_package(package)

# Needs finalization
def print_status():
    '''
    Prints status of trucks & hash table.  
    '''

    # Prints everything
    print(receiveing)
    print(truck1)
    print(truck2)
    print(truck3)
    print(f'\nTotal miles driven = {round(truck1.millage + truck2.millage + truck3.millage, 1)}')
    print(f'Current time = {global_time.time()}')

    # Waits for user to press enter before moving on
    input()

# Needs finalization
def main():
    '''
    Main controller of the program, controls the UI.  
    '''
    
    # Prints welcome screen in ASCII art.  
    print(f'''
        ******************************************************************************************************************************
        * __          _______ _    _ _____   _____    _____           _                       _____       _ _                        *
        * \ \        / / ____| |  | |  __ \ / ____|  |  __ \         | |                     |  __ \     | (_)                       *
        *  \ \  /\  / / |  __| |  | | |__) | (___    | |__) |_ _  ___| | ____ _  __ _  ___   | |  | | ___| |___   _____ _ __ _   _   *
        *   \ \/  \/ /| | |_ | |  | |  ___/ \___ \   |  ___/ _` |/ __| |/ / _` |/ _` |/ _ \  | |  | |/ _ \ | \ \ / / _ \ '__| | | |  *
        *    \  /\  / | |__| | |__| | |     ____) |  | |  | (_| | (__|   < (_| | (_| |  __/  | |__| |  __/ | |\ V /  __/ |  | |_| |  *
        *     \/  \/   \_____|\____/|_|    |_____/   |_|   \__,_|\___|_|\_\__,_|\__, |\___|  |_____/ \___|_|_| \_/ \___|_|   \__, |  *
        *                                                                        __/ |                                        __/ |  *
        *                                                                       |___/                                        |___/   *
        *                                                                                                                            *
        ******************************************************************************************************************************                                                                    
    ''')

    # Main loop.  Prompts user for actions until exit is chosen. 
    while True:
        print(f''' 
        Current time = {global_time.time()}

        1) Set time of day
        2) Print current package & truck status
        3) Insert new package
        4) Lookup package based on address
        5) Lookup package based on city
        6) Lookup package based on zip code
        7) Lookup package based on weight
        8) Lookup package based on deadline
        9) Lookup package based on status
        0) Exit program
        ''')

        selection = input('Please select an option: ').strip()

        # 1) Set time of day
        if selection == '1':
            deliver_packages_to_time()
        
        # 2) Print current package & truck status
        elif selection == '2':
            print_status()
        
        # 3) Insert new package
        elif selection == '3':
            create_new_package()
        
        # 4) Lookup package based on address
        elif selection == '4':
            address = input('Enter the address you would like to lookup: ')
            addresses = receiveing.lookup_packages('address', address)
        
            print(f'Packages with Address: {address}\n----------------------')
            for p in addresses:
                print(str(p))

            input()

        # 5) Lookup package based on city
        elif selection == '5':
            city = input('Enter the city you would like to lookup: ')
            cities = receiveing.lookup_packages('city', city)

            print(f'Packages with City: {city}\n-------------------')
            for p in cities:
                print(str(p))

            input()
        
        # 6) Lookup package based on zip code
        elif selection == '6':
            zip_code = input('Enter the zip you would like to lookup: ')
            zips = receiveing.lookup_packages('zip_code', zip_code)

            print(f'Packages with Zip: {zip_code}\n------------------')
            for p in zips:
                print(str(p))

            input()
        
        # 7) Lookup package based on weight
        elif selection == '7':
            weight = input('Enter the weight you would like to lookup: ')
            weights = receiveing.lookup_packages('weight', weight)

            print(f'Packages with Weight: {weight}\n---------------------')
            for p in weights:
                print(str(p))

            input()

        # 8) Lookup package based on deadline
        elif selection == '8':
            deadline = input('Enter the deadline you would like to lookup: ')
            deadlines = receiveing.lookup_packages('deadline', deadline)

            print(f'Packages with deadline: {deadline}\n-----------------------')
            for p in deadlines:
                print(str(p))

            input()
        
        # 9) Lookup package based on status
        elif selection == '9':
            status = input('Enter the status you would like to lookup: ')
            statuses = receiveing.lookup_packages('status', status)

            print(f'Packages with status: {status}\n---------------------')
            for p in statuses:
                print(str(p))

            input()
        
        # 0) Exit program
        elif selection == '0':
            input('Thank you for choosing WGUPS!\nGoodbye....')
            exit()

        # Invalid input
        else:
            input('Invalid input, please try again')


if __name__ == "__main__":
    main()