import csv
import Package

def load_packages(self, file_name):
        # CSV_Data\packages.csv
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            package = Package()

            for row in csv_reader:
                package.package_id = row[0]
                package.address = row[1]
                package.city = row[2]
                package.state = row[3]
                package.zip_code = row[4]
                package.deadline = row[5]
                package.weight = row[6]
                package.instructions = row[7]

def load_distances(self, file_name):

        # CSV_Data\distances.csv
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                # do stuff 