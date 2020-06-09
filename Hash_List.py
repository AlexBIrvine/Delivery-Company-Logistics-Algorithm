from Package import Package
import csv

class HashList: 
    '''
    Hash list meant for packages.
    '''

    # Initialize Hash List  --  works
    def __init__(self, capacity=50): 
        self.package_table = []

        for bucket in range(capacity):
            self.package_table.append([])

    # Create package  --  complete
    def insert_package(self, package):
        bucket = package.package_id % len(self.package_table)
        bucket_list = self.package_table[bucket]
        bucket_list.append(package)

    # Retrieve package data  -- 
    def search_package(self, id):
        bucket = id % len(self.package_table)
        bucket_list = self.package_table[bucket]
        
        for package in bucket_list:
            if package.package_id == id:
                return package
                
        return None


    # Delete package  -- 
    def delete_package(self, id):
        bucket = id % len(self.package_table)
        bucket_list = self.package_table[bucket]

        if id in bucket_list:
            bucket_list.remove(id)

    # Populate hashlist from CSV file  --  
    def load_from_csv(self, file_name):

        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            
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
                self.insert_package(package)

    # Print hash last
    # change this to loop through each bucket
    def __repr__(self) -> str:
        boxes = '\n'.join(f'{p!s}' for p in self.package_table)
        return f'''
        List of packages
        ----------------
        {boxes}
        '''


cart = HashList()
cart.load_from_csv('CSV_Data\packages.csv')
print(cart.search_package(12))