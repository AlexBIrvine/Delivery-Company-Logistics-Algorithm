from Package import Package
from Loader import Loader

class Truck:
    '''A truck class that stores and delivers packages'''

    def __init__(self, payload):
        '''Initializes truck with payload list of packages'''   
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
        for i, package in enumerate(self.cargo):
            for j, priority_package in enumerate(self.priority_packages):
                if type(package) == Package and type(priority_package) == Package:
                    if package.address_id == priority_package.address_id:
                        self.priority_packages.append(self.cargo[i])
                        self.cargo[i] = None

        # For all remaining packages, place in regular_packages
        for index, package in enumerate(self.cargo):
            if type(package) == Package: 
                self.regular_packages.append(self.cargo[index])
                self.cargo[index] = None


    def find_next_address(self):
        '''Searches for the next neighest address based on the packages left in the truck'''
        return True

def main():
    loader = Loader()
    payload = loader.get_2nd_truck_packages()
    payload = loader.check_existing_list(payload)

    truck_2 = Truck(payload)

    for p in truck_2.cargo:
        if type(p) == Package: 
            print(f'Cargo - {p.package_id:>2} {p.address_id:>2}')
        else:
            print(f'Cargo - {type(p)}')

    for p in truck_2.regular_packages:
        if type(p) == Package: 
            print(f'Regular - {p.package_id:>2} {p.address_id:>2}')
        else:
            print(f'Regular - {type(p)}')

    for p in truck_2.priority_packages:
        if type(p) == Package: 
            print(f'Priority - {p.package_id:>2} {p.address_id:>2}')
        else:
            print(f'Priority - {type(p)}')

if __name__ == "__main__":
    main()
