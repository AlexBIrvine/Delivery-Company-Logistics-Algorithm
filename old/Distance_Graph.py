import csv

class DistanceGraph:
    '''
    2D list of distance table
    '''

    def __init__(self):
        self.distance_table = []
        self.load_from_csv()

    def load_from_csv(self, file_name='CSV_Data\distances-filled.csv'):

        # Read in CSV file
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            
            # Declare local variables
            column_count = 0

            # Loop through each row in file
            for row in reader:
                current_row = []
                
                for column in row: 
                    if column_count > 1:
                        current_row.append(column)
                    column_count += 1
                    
                self.distance_table.append(current_row)
                column_count = 0

    def get_row(self, row):
        return self.distance_table[row]

    def lookup_cell(self, column, row):
        return self.distance_table[column][row]

    def clear_row(self, row_num):
        for i in range(len(self.distance_table)): 
            self.distance_table[row_num][i] = -1

    def clear_column(self, column_num):
        for i in range(len(self.distance_table)):
            self.distance_table[i][column_num] = -1

    def __repr__(self):
        return_string = ""

        for index, row in enumerate(self.distance_table):
            return_string += f'{index} = {str(row)}\n'

        return return_string