import csv
import re

def load_from_csv(file_name):

    # Read in CSV file
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        
        # Declare local variables
        site_list = []
        row_count = 0

        # Loop through each row in file
        for i, row in enumerate(reader):

            # Read the first value of the row, which is the name of the property
            # The data contains the name and address in one string value
            # Using regex to remove the address.  
            match = re.match(r'^\D*', row[0])
            if match:
                name = match.group().strip()
                site_list.append(name)

            # Each row contains a list
            # Loops through the list assinging distance to location
            for i, cell in enumerate(row):
                if (i > 1 and cell != '0.0'): 
                    print(f"Distance from {name} to {site_list[i-2]}: {cell}") 
                elif (cell == '0.0'): 
                    break

load_from_csv('CSV_Data\distances.csv')