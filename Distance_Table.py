import csv

class DistanceTable:
    '''Contains a 2D list that holds distance data between addresses'''


    def __init__(self):
        '''Initializes the object and calls load_from_csv method'''
        self.table = []
        self.load_from_csv()

    def load_from_csv(self, file_name='CSV_Data\distances-filled.csv'):
        '''Loads data from csv into table'''
        
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
                
                # Appends current row to distance table
                self.table.append(current_row)

    def get_row(self, row_num):
        '''Returns the list found in row_num'''
        return self.table[int(row_num)]


