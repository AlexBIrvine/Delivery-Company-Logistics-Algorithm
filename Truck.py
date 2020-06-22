from Package import Package
from Loader import Loader
from Distance_Table import DistanceTable

class Truck:
    '''A truck class that stores and delivers packages'''


    def __init__(self, payload):
        '''Initializes truck with payload list of packages'''   
        self.address_book = DistanceTable().table
        self.cargo = payload
        self.priority_packages = []
        self.regular_packages = []
        self.millage = 0.0
        self.current_location = 0

        self.sort_packages()


    def sort_packages(self):
        '''Sorts packages based on priority'''
        
        # Finds all packages that need to be delivered before EOD
        for i in range(0, len(self.cargo)):
                if self.cargo[i].deadline != 'EOD':
                    self.priority_packages.append(self.cargo[i])
                    self.cargo[i] = None

        # Finds all packages that share an address already in priority_packages
        for i in range(0, len(self.cargo)):
            for j in range(0, len(self.priority_packages)):
                if type(self.cargo[i]) == Package and type(self.priority_packages[j]) == Package:
                    if self.cargo[i].address_id == self.priority_packages[j].address_id:
                        self.priority_packages.append(self.cargo[i])
                        self.cargo[i] = None

        # For all remaining packages, place in regular_packages
        for index, package in enumerate(self.cargo):
            if type(package) == Package: 
                self.regular_packages.append(self.cargo[index])
                self.cargo[index] = None

        # Removes all 'none' type from cargo
        self.cargo = [i for i in self.cargo if i] 


    def find_closest_package(self, address):
        '''Searches for the next neighest address based on the packages left in the truck'''
        closest_distance = float('inf') 
        closest_package = 0

        if len(self.priority_packages) > 0:
            for i in range(0, len(self.priority_packages)):
                row = self.address_book[int(address)]
                if float(row[i]) < float(closest_distance): 
                    closest_distance = row[i]
                    closest_package = self.priority_packages[i]

        else:
            for i in range(0, len(self.regular_packages)):
                row = self.address_book[int(address)]
                if float(row[i]) < float(closest_distance): 
                    closest_distance = row[i]
                    closest_package = self.regular_packages[i]

        return closest_package


    def deliver_package(self, package):
        '''delivers package'''

        if package in self.priority_packages:
            self.millage += float(self.address_book[int(self.current_location)][int(package.address_id)])
            self.current_location = package.address_id
            self.priority_packages.pop(self.priority_packages.index(package))

        elif package in self.regular_packages:
            self.millage += float(self.address_book[int(self.current_location)][int(package.address_id)])
            self.current_location = package.address_id
            self.regular_packages.pop(self.regular_packages.index(package))

        else: 
            self.millage += float(self.address_book[int(self.current_location)][0])
            self.current_location = 0
        
        print(self)


    def run_deliveries(self):
        '''Delivers all packages on truck'''

        while len(self.priority_packages) + len(self.regular_packages):
            self.deliver_package(self.find_closest_package(self.current_location))
        
        if self.current_location != 0:
            self.deliver_package(self.find_closest_package(self.current_location))


    def __repr__(self):
        '''prints everything'''
        return_string = ''

        return_string += f'Current millage = {self.millage}\n'
        return_string += f'Current location = {self.current_location}\n'
        return_string += f'Total package left = {len(self.priority_packages) + len(self.regular_packages)}\n'

        for p in self.cargo:
            return_string += f'Cargo = {p}\n'

        for p in self.priority_packages:
            return_string += f'Priority\t{p.package_id:>02}\t{p.address_id:>02}\n'

        for p in self.regular_packages:
            return_string += f'Regular\t\t{p.package_id:>02}\t{p.address_id:>02}\n'
        
        return_string += ''

        return return_string

def main():
    receiving = Loader()

    second = receiving.get_2nd_truck_packages()
    receiving.update_package_nine()
    second.extend(receiving.get_delayed_packages())
    second = receiving.check_existing_list(second)

    urgent = receiving.get_urgent_packages()
    urgent = receiving.check_existing_list(urgent)

    remaining = receiving.get_remaining_packages()

    truck_1 = Truck(urgent)
    truck_2 = Truck(second)
    truck_3 = Truck(remaining)

    print('Truck 1')
    print(truck_1)

    print('Truck 2')
    print(truck_2)

    print('Truck 3')
    print(truck_3)

    truck_1.run_deliveries()
    truck_2.run_deliveries()
    truck_3.run_deliveries()

    print(f'''
    Truck 1 Millage = {truck_1.millage}
    Truck 2 Millage = {truck_2.millage}
    Truck 1 Millage = {truck_3.millage}
    Total millage = {truck_1.millage + truck_2.millage + truck_3.millage}
    ''')


if __name__ == "__main__":
    main()
