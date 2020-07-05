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

        # Loads data from csv into tables & updates package 9
        self.table_from_csv()
        self.graph_from_csv()
        self.update_package_nine()


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
            return package

    def handload_truck_1(self):
        '''
        Helper method to load truck 1.
        This truck primarily holds the delayed packages
        and other nearby packages.
        '''

        truck_1 = [1,2,4,6,7,17,22,24,25,26,28,29,31,32,33,40]
        packages = []
        for p_id in truck_1:
            packages.append(self.retrieve_package(p_id))
        
        return packages

    def handload_truck_2(self):
        '''
        Helper method to load truck 2.
        This truck primarily holds packages restricted to this truck,
        urgent packages and nearby packages. 
        '''

        truck_1 = [3,8,10,13,14,15,16,18,19,20,30,34,36,37,38,39]
        packages = []
        for p_id in truck_1:
            packages.append(self.retrieve_package(p_id))
        
        return packages

    def handload_truck_3(self):
        '''
        Helper method to load truck 3.
        This truck holds packages not found in other trucks.
        All of these packages go EOD and will be delivered last.  
        '''

        truck_3 = [5,9,11,12,21,23,27,35]
        packages = []
        for p_id in truck_3:
            packages.append(self.retrieve_package(p_id))
        
        return packages

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

    # NEED TO TEST
    def update_package(self, package, value, attribute = 'status'):
        '''
        Updates the <attribute> of the <package> with <value>
        '''

        if attribute == 'address':
            package.address = value
        elif attribute == 'deadline':
            package.deadline = value
        elif attribute == 'city':
            package.city = value
        elif attribute == 'zip':
            package.zip_code = value
        elif attribute == 'weight':
            package.weight = value
        elif attribute == 'status':
            package.status = value

    # NEED TO TEST
    def lookup_package(self, attribute, value):
        '''
        Returns a list of all packages that match the <value> of a given <attribute>. 
        Removes whitespace from <value> and converts to lowercase for reliable searching.
        '''

        found = []
        value = value.strip().lower()

        for p in self.package_table:
            if type(p) == Package and attribute == 'address' and p.address.strip().lower() == value:
                found.append(p)
            elif type(p) == Package and attribute == 'deadline' and p.deadline.strip().lower() == value:
                found.append(p)
            elif type(p) == Package and attribute == 'city' and p.city.strip().lower() == value:
                found.append(p)
            elif type(p) == Package and attribute == 'zip' and p.zip.strip().lower() == value:
                found.append(p)    
            elif type(p) == Package and attribute == 'weight' and p.weight.strip().lower() == value:
                found.append(p)
            elif type(p) == Package and attribute == 'status' and p.status.strip().lower() == value:
                found.append(p)
        
        return found


    def __repr__(self):
        '''
        Prints a table of the package's ID, DEADLINE & STATUS.  
        Used to check if deliveries are arriving on time.  
        '''

        return_string = 'ID\tDEADLINE\t             STATUS\n'
        return_string += '---------------------------------------------------------\n'

        for p in self.package_table:
            if type(p) == Package:
                return_string += f'{p.package_id}\t{p.deadline:<8}\t{p.status}\n'
        
        return return_string
