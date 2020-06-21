from Hash_Table import HashTable
from Package import Package
import re


class Loader:
    '''Loads packages onto truck'''

    def __init__(self):
        '''Creates a HashTable of packages named warehouse'''
        self.warehouse = HashTable()

    def get_delayed_packages(self):
        '''Returns a list of packages that are delayed'''
        delayed = []

        for bucket in self.warehouse.package_table:
            if type(bucket) == Package and bucket.instructions.lower().find('delay') != -1:
                delayed.append(self.warehouse.retrieve_package(bucket.package_id))
        
        return delayed
                
    def get_urgent_packages(self):
        '''Returns a list of packages that have deadline before EOD'''

        urgent = []

        for bucket in self.warehouse.package_table:
            if type(bucket) == Package and bucket.deadline.lower() != 'eod':
                urgent.append(self.warehouse.retrieve_package(bucket.package_id))
        
        return urgent

    def get_2nd_truck_packages(self):
        '''Returns a list of packages that are restricted to the 2nd truck'''

        second = []

        for bucket in self.warehouse.package_table:
            if type(bucket) == Package and bucket.instructions.lower() == 'can only be on truck 2':
                second.append(self.warehouse.retrieve_package(bucket.package_id))

        return second

    def check_and_get_bundled_packages(self, package):
        '''
        checks if a package needs to be delivered with another package
        if so, returns a list of packages it needs to be delivered with
        '''

        bundled = []

        if package.instructions.lower().find('must be delivered with') != -1:
            for match in re.findall(r'\d+', package.instructions):
                matched = self.warehouse.retrieve_package(int(match))
                if type(matched) == Package:
                    bundled.append(matched)

        return bundled

    def check_existing_list(self, list):
        '''
        Runs check_and_get_bundled_packages() and check_and_get_same_addressed_packages()
        for a given list of packages.  Returns an updated list. 
        '''

        existing = list

        for package in existing:
            existing.extend(self.check_and_get_bundled_packages(package))
            existing.extend(self.check_and_get_same_addressed_packages(package))

        return existing

    def check_and_get_same_addressed_packages(self, package):
        '''
        checks if a package has other packages going to the same address as it.  
        If so, returns a list of packages that share it's address
        '''

        same_address = []

        for id in self.warehouse.address_table[int(package.address_id)]:
            found = self.warehouse.retrieve_package(id)
            if type(found) == Package:
                same_address.append(found)

        return same_address

def main():
    receiving = Loader()
    trucking = receiving.get_2nd_truck_packages()
    # urgent = receiving.get_urgent_packages()

    for p in trucking: 
        trucking = receiving.check_existing_list(trucking)

    # for p in urgent:
    #     urgent = receiving.check_existing_list(urgent)

    print(f'Amount in truck 2: {len(trucking)}')
    for p in trucking:
        print(f'Second - {p.package_id:>02}')

    # print(f'Amount left urget: {len(urgent)}')
    # for p in urgent:
    #     print(f'Urgent - {p.package_id:>02}')




if __name__ == "__main__":
    main()
