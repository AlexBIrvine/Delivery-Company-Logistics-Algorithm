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
        self.graph = []

        # Creates blank bucket_lists for each bucket in the table
        for bucket in range(capacity):
            self.package_table.append(None)
            self.address_table.append([])

        # Loads data from csv into tables
        self.table_from_csv()
        self.graph_from_csv()


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

    def table_from_csv(self, file_name='CSV_Data\packages.csv'):
        '''Loads data from csv into package_table & address_table'''

        # Opens & reads from csv file and creates a distance table to read from
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            
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
                printout += f'Package ID = {bucket.package_id:>02} & Address ID = {bucket.address_id:>02}\n'

            # If bucket is empty, print out the index and delcare it empty
            else:
                printout += f'No package in bucket #: {index:>02}\n'
        
        # Return built printout string
        return printout


    # ----------------------------------------------------------------------------
    #                           Methods from Loader.py
    # ----------------------------------------------------------------------------


    # Does it get the wrong address package?
    # Does the for loop without copying self.package_table[:] ?
    def get_delayed_packages(self):
        '''
        Returns a list of packages that are delayed which includes any packages with wrong addresses
        '''
        delayed = []

        for bucket in self.package_table:
            if type(bucket) == Package and bucket.instructions.lower().find('delay') != -1:
                delayed.append(self.retrieve_package(bucket.package_id))

            if type(bucket) == Package and bucket.instructions.lower().find('wrong') != -1:
                delayed.append(self.retrieve_package(bucket.package_id))

        return delayed


    # Does the for loop without copying self.package_table[:] ?
    def get_urgent_packages(self):
        '''Returns a list of packages that have deadline before EOD'''

        urgent = []

        for bucket in self.package_table:
            if type(bucket) == Package and bucket.deadline.lower() != 'eod':
                urgent.append(self.retrieve_package(bucket.package_id))
        
        return urgent


    # Does the for loop without copying self.package_table[:] ?
    def get_2nd_truck_packages(self):
        '''Returns a list of packages that are restricted to the 2nd truck'''

        second = []

        for bucket in self.package_table:
            if type(bucket) == Package and bucket.instructions.lower() == 'can only be on truck 2':
                second.append(self.retrieve_package(bucket.package_id))

        return second


    # Does the for loop without copying self.package_table[:] ?
    def get_remaining_packages(self):
        '''Returns a list of packages left in the hash table'''

        remaining = []

        for bucket in self.package_table:
            if type(bucket) == Package:
                remaining.append(self.retrieve_package(bucket.package_id))

        return remaining

    
    def check_and_get_bundled_packages(self, package):
        '''
        Checks if a package needs to be delivered with another package
        If so, returns a list of packages it needs to be delivered with
        '''

        bundled = []

        if package.instructions.lower().find('must be delivered with') != -1:
            for match in re.findall(r'\d+', package.instructions):
                matched = self.retrieve_package(int(match))
                if type(matched) == Package:
                    bundled.append(matched)

        return bundled


    def check_and_get_same_addressed_packages(self, package):
        '''
        Checks if a package has other packages going to the same address as it.  
        If so, returns a list of packages that share it's address
        '''

        same_address = []

        for id in self.address_table[int(package.address_id)]:
            found = self.retrieve_package(id)
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
        '''
        Corrects the address for package #9
        '''

        # Pulls package from warehouse
        nine = self.retrieve_package(9)
        
        # Updates attributes
        nine.address_id = 19
        nine.address = '410 S State St'
        nine.city = 'Salt Lake City'
        nine.zip = '84111'

        # Insets package back into package_graph
        self.insert_package(nine)


    # ----------------------------------------------------------------------------
    #                           Methods from Distance_Graph.py
    # ----------------------------------------------------------------------------

    def graph_from_csv(self, file_name='CSV_Data\distances-filled.csv'):
        '''Loads data from csv into graph'''
        
        # opens & reads from csv file 
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            
            # Declare local variables
            column_count = 0

            # Loop through each row in file
            for row in reader:
                current_row = []
                
                # Ignores the first column in csv file, as site name will not be used in the project
                for c_index, column in enumerate(row): 
                    if c_index > 1:
                        current_row.append(column)
                
                # Appends current row to distance graph
                self.graph.append(current_row)



def main():
    print('Does nothing right now')

if __name__ == "__main__":
    main()
