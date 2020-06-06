from Package import Package
import csv


global_count = 0

class HashList: 
    '''
    Hash list meant for packages.  
    '''

    # Initialize Hash List  --  works
    def __init__(self, capacity=40): 
        self.package_table = []

        for bucket in range(capacity):
            self.package_table.append([])

    # Create package  --  complete
    def insert_package(self, package):
        global global_count
        global_count = global_count + 1

        bucket = package.package_id % len(self.package_table)
        bucket_list = self.package_table[bucket]
        bucket_list.append(package)

    # Retrieve package data  --  
    def search_package(self, id):
        bucket = id % len(self.package_table)
        bucket_list = self.package_table[bucket]
        return bucket_list[0]  # possible rewrite (for package in bucket, if id == id, return package.  End of loop, return none)

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
                package.address = row[1]
                package.city = row[2]
                package.state = row[3]
                package.zip_code = row[4]
                package.deadline = row[5]
                package.weight = row[6]
                package.instructions = row[7]
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
print(cart)
# print(cart)