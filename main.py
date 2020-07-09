from Truck import Truck
from Hash_Table import HashTable
from Package import Package 
import datetime
import re

# Creates the Hash Table & datetime global objects for the project
receiveing = HashTable()
global_time = datetime.datetime(2020,7,8,8,00)

# Creates the trucks with preloaded packages and sets their start times.  
# Truck 3 has a temporary time set since it's true time will be when the first truck completes deliveries.  
start_1 = datetime.datetime(2020,7,8,9,5)
start_3 = datetime.datetime(2020,7,8,23,59)
truck1 = Truck(receiveing.handload_truck_1(), start_1, 1, receiveing)
truck2 = Truck(receiveing.handload_truck_2(), global_time, 2, receiveing)
truck3 = Truck(receiveing.handload_truck_3(), start_3, 3, receiveing)



def run_deliveries(delivery_time = datetime.datetime(2020,7,8,23,59)):
    '''Runs all deliveries, printing the result.'''
    global global_time

    while global_time < delivery_time:
        if truck3.status == 'AT HUB, START OF DAY' and truck2.status == 'Deliveries complete' or truck1.status == 'Deliveries complete':
            truck3.time = global_time
        if global_time == truck1.time:
            truck1.tick()
        if global_time == truck2.time:
            truck2.tick()
        if global_time == truck3.time:
            truck3.tick()
        
        if truck1.status == 'Deliveries complete' and truck2.status == 'Deliveries complete' and truck3.status == 'Deliveries complete':
            break

        global_time  += datetime.timedelta(0, 20)

    print(receiveing)
    print(truck1)
    print(truck2)
    print(truck3)
    print(f'Total miles driven = {round(truck1.millage + truck2.millage + truck3.millage, 2)}')






def deliver_packages_to_time():

    input_time = input("Please enter a time in hours and seconds - ")
    match = re.match(r'(\d+)\D+(\d+)', input_time)

    if match and match.lastindex == 2:
            hour = int(match.group(1))
            minute = int(match.group(2))
            run_deliveries(datetime.datetime(2020,7,8,hour,minute))
    else:
        run_deliveries()
    

def get_package_details():
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
    if receiveing.lookup_package('address', address):
        address_id = receiveing.lookup_package('address', address)[0].address_id

    
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
    

def main():
    '''Main controller of the program, controls the UI'''

    get_package_details()
    print(receiveing)


    # What actions do I need to accommodate?  
    # - Interface to insert a package
    # - Interface to lookup status at any time
    # - 






if __name__ == "__main__":
    main()