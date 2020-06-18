from Distance_Graph import DistanceGraph
from Package import Package
import csv
import re

class HashList: 
    '''
    Hash table meant for packages.
    '''

    # Initialize Hash List
    def __init__(self, capacity=50): 
        self.package_table = []
        self.address_table = []
        
        for bucket in range(capacity):
            self.package_table.append([])
            self.address_table.append([])
            
        self.load_from_csv()

    # Create package
    def insert_package(self, package):
        bucket = package.package_id % len(self.package_table)
        bucket_list = self.package_table[bucket]
        bucket_list.append(package)

    # Retrieve package data
    def search_by_id(self, id):
        bucket = id % len(self.package_table)
        bucket_list = self.package_table[bucket]
        
        for package in bucket_list:
            if package.package_id == id:
                return package
                
        return None

    def search_by_address_id(self, id):
        id_list = []

        for bucket in self.package_table: 
            for package in bucket:
                if int(package.address_id) == id:
                    id_list.append(package.package_id)

        return id_list

    # Delete package
    def delete_package(self, id):
        bucket = id % len(self.package_table)
        bucket_list = self.package_table[bucket]

        if id in bucket_list:
            bucket_list.remove(id)

    # Populate hashlist from CSV file  --  
    def load_from_csv(self, file_name='CSV_Data\packages.csv'):

        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            distances = DistanceGraph()
            # distances.load_from_csv()
            
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

    def get_priority_packages(self):
        priority_packages = []

        for bucket in self.package_table:
            for package in bucket:
                if package.deadline != 'EOD':
                    priority_packages.append(package)
                    

        return priority_packages

    def get_undeliverable_packages(self):
        undeliverable_packages = []

        for bucket in self.package_table:
            for package in bucket:
                if package.instructions.lower().find('delay') != -1:
                    undeliverable_packages.append(package)
                if package.instructions.lower().find('wrong') != -1:
                    undeliverable_packages.append(package)

        return undeliverable_packages

    def get_restrictive_packages(self):
        restrictive_packages = []

        for bucket in self.package_table:
            for package in bucket:

                if package.instructions.lower().find('must')  != -1:
                    restrictive_packages.append(package)

                    for match in re.findall(r'\d+', package.instructions):
                        other_package = self.search_by_id(int(match))
                        if other_package not in restrictive_packages:
                            restrictive_packages.append(other_package)
                    
                if package.instructions.lower().find('truck') != -1:
                    restrictive_packages.append(package)

        return restrictive_packages
    
    def get_same_addressed_packages(self, package):
        package_list = []
        
        for id in self.address_table[int(package.address_id)]:
            package_list.append(self.search_by_id(id))

        return package_list

    # Print hash last
    def __repr__(self) -> str:
        boxes = ''

        for bucket in self.package_table:
            for package in bucket:
                if type(package) == Package:
                    boxes += str(package)

        return  f'''
            List of packages
            ----------------
            {boxes}
            '''

test = HashList()

for row in test.address_table:
    print(row)
