from Hash_Table import HashTable
from Package import Package
import re


class Loader:
    '''Loads packages onto truck'''



    def __init__(self):
        '''Creates a HashTable of packages named warehouse'''
        self.warehouse = HashTable()

    def get_delayed_packages(self):
        '''Returns a list of packages that are delayed which includes any packages with wrong addresses'''
        delayed = []

        for bucket in self.warehouse.package_table:
            if type(bucket) == Package and bucket.instructions.lower().find('delay') != -1:
                delayed.append(self.warehouse.retrieve_package(bucket.package_id))

            if type(bucket) == Package and bucket.instructions.lower().find('wrong') != -1:
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

    def get_remaining_packages(self):
        '''Returns a list of packages left in the hash table'''

        remaining = []

        for bucket in self.warehouse.package_table:
            if type(bucket) == Package:
                remaining.append(self.warehouse.retrieve_package(bucket.package_id))

        return remaining

    def check_and_get_bundled_packages(self, package):
        '''
        Checks if a package needs to be delivered with another package
        If so, returns a list of packages it needs to be delivered with
        '''

        bundled = []

        if package.instructions.lower().find('must be delivered with') != -1:
            for match in re.findall(r'\d+', package.instructions):
                matched = self.warehouse.retrieve_package(int(match))
                if type(matched) == Package:
                    bundled.append(matched)

        return bundled

    def check_and_get_same_addressed_packages(self, package):
        '''
        Checks if a package has other packages going to the same address as it.  
        If so, returns a list of packages that share it's address
        '''

        same_address = []

        for id in self.warehouse.address_table[int(package.address_id)]:
            found = self.warehouse.retrieve_package(id)
            if type(found) == Package:
                same_address.append(found)

        return same_address

    def check_existing_list(self, existing_list):
        '''
        Runs check_and_get_bundled_packages() and check_and_get_same_addressed_packages()
        for a given list of packages.  Returns an updated list. 
        '''

        existing = existing_list

        for i in range(0, len(existing)):
            existing.extend(self.check_and_get_bundled_packages(existing[i]))
            existing.extend(self.check_and_get_same_addressed_packages(existing[i]))

        return existing

    def update_package_nine(self):
        '''Corrects the address for package #9'''

        # Pulls package from warehouse
        nine = self.warehouse.retrieve_package(9)
        
        # Updates attributes
        nine.address_id = 19
        nine.address = '410 S State St'
        nine.city = 'Salt Lake City'
        nine.zip = '84111'

        # Insets package back into warehouse
        self.warehouse.insert_package(nine)







def main():
    print('Does nothing right now')

if __name__ == "__main__":
    main()
