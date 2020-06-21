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
        for index, package in enumerate(self.cargo):
            if type(package) == Package:
                if package.deadline != 'EOD':
                    self.priority_packages.append(self.cargo[index])
                    self.cargo[index] = None

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

        for p in self.priority_packages:
            return_string += f'Priority\t{p.package_id:>02}\t{p.address_id:>02}\n'

        for p in self.regular_packages:
            return_string += f'Regular\t\t{p.package_id:>02}\t{p.address_id:>02}\n'
        
        return_string += ''

        return return_string

def main():
    loader = Loader()
    payload = loader.get_2nd_truck_packages()
    payload = loader.check_existing_list(payload)
    truck_2 = Truck(payload)
    print(truck_2)
    truck_2.run_deliveries()
    print(truck_2)


if __name__ == "__main__":
    main()
