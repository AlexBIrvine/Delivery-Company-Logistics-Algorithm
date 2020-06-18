from Distance_Table import DistanceTable
from Package import Package
import csv
import re

class HashTable:
    '''
    Hash table that stores all package data.  
    Implements direct hashing using the package ID as the key.
    '''

    def  __init__(self, capacity=50):
        '''
        Initializes a HashTable with buckets equal to the capacity (default = 50).
        Loads data into table from csv file.
        '''
        # Initializes package & address table.  
        self.package_table = []
        self.address_table = []

        # Creates blank bucket_lists for each bucket in the table
        for bucket in range(capacity):
            self.package_table.append(None)
            self.address_table.append([])

        # Loads data from csv into tables
        self.load_from_csv()

    def insert_package(self, package):
        '''Takes package as argument, hashes it based on id, and inserts the package into table'''

        bucket = package.package_id % len(self.package_table)
        self.package_table[bucket] = package

    def retrieve_package(self, package_id):
        '''Retrieves package by ID'''

        bucket = package_id % len(self.package_table)
        
        # If package found in bucket, set that bucket to none and return the package
        if type(self.package_table[bucket]) != None:
            package = self.package_table[bucket]
            self.package_table[bucket] = None
            return package

    def retrieve_packages_by_address_id(self, address_id):
        '''Return a list of packages that share the address ID'''

        packages = []

        # If the list is not empty...
        #   Find packages listed in address table
        #   and add them to the packages list to return
        if self.address_table[address_id]:
            for id in self.address_table[address_id]:
                packages.append(self.retrieve_package(id))

        # Return packages list
        return packages

    def retrieve_priority_packages(self):
        '''Returns a list of packages that do not have an 'EOD' deadline and the other packages going to the same address'''

        priority_packages = []

        for bucket in self.package_table:
            if type(bucket) == Package and bucket.deadline != 'EOD':
                priority_packages.extend(self.retrieve_packages_by_address_id(int(bucket.address_id)))
        
        return priority_packages
                


    def load_from_csv(self, file_name='CSV_Data\packages.csv'):
        '''Loads data from csv into package_table & address_table'''

        # Opens & reads from csv file and creates a distance table to read from
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            distances = DistanceTable()

            # Loop through each row in file, create package based on it's information
            for row in reader:
                package = Package(int(row[0]))
                package.address_id = row[1]
                package.address = row[2]
                package.city = row[3]
                package.state = row[4]
                package.zip_code = row[5]
                package.deadline = row[6]
                package.weight = row[7]
                package.instructions = row[8]
                package.distances = distances.get_row(int(row[1]))
                self.address_table[int(row[1])].append(int(row[0]))
                self.insert_package(package)

    def __repr__(self):
        '''Prints a list of all packages in Hash Table'''
        
        # Declares empty string to build before returning
        printout = ''

        # Loops through all buckets in package table
        for index, bucket in enumerate(self.package_table):
            # If bucket contains a package, print it's ID & Address ID
            if type(bucket) == Package:
                printout += f'Package ID = {bucket.package_id} & Address ID = {bucket.address_id}\n'

            # If bucket is empty, print out the index and delcare it empty
            else:
                printout += f'No package in bucket #: {index}\n'
        
        # Return built printout string
        return printout


def main():
    tab = HashTable()
    zips = dict()

    for package in tab.package_table:
        if type(package) == Package: 
            if package.zip_code in zips:
                zips[package.zip_code] += 1
            else:
                zips[package.zip_code] = 1

    print(zips)

if __name__ == "__main__":
    main()
