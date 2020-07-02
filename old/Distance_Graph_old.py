from Edge import Edge
from Node import Node
import csv

class DistanceGraph:
    '''Contains a 2D list that holds distance data between addresses'''


    def __init__(self):
        '''Initializes the object and calls load_from_csv method'''
        self.graph = []
        # self.adjusted_graph = []
        # self.nodes = []
        # self.edges = []

        self.load_from_csv()
        # self.get_adjusted()


    def load_from_csv(self, file_name='CSV_Data\distances-filled.csv'):
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


    # def clear_nodes(self):
    #     '''helper method to initialize node list'''
    #     self.nodes = []

    #     for i in range(len(self.graph)):
    #         self.nodes.append(Node(i))


    # def dijkstra(self, start_node_id = 0):
    #     '''Runs the dijkstra pathing algorithm and updates node list'''

    #     # Initialize local variables
    #     start_node = self.nodes[start_node_id]
    #     start_node.total_distance = 0.0
    #     visited = []
    #     unvisited = []
    #     for node in self.nodes:
    #         unvisited.append(node)

    #     # While there are unvisited nodes...
    #     while (len(unvisited)) > 0:
    #     # Find the node in unvisited that has the shortest total distance
    #     # Make that node the current node
    #         current_node = unvisited[0]
    #         for node in unvisited:
    #             if node.total_distance < current_node.total_distance:
    #                 current_node = node

    #         # place it in visited list
    #         visited.append(unvisited.pop(unvisited.index(current_node)))

    #         # for each node in unvisited, find the distance from current node to it.  
    #         for i in range(len(unvisited)):
    #             distance = float(self.graph[current_node.id][unvisited[i].id]) + float(current_node.total_distance)
                
    #             # If this distance is less than the nodes previous distance, update that node
    #             if distance < unvisited[i].total_distance:
    #                 unvisited[i].total_distance = distance
    #                 unvisited[i].prev_address = current_node.id

    #     self.nodes = visited


    # def get_adjusted(self):
    #     '''Runs dijkstra's algorithm on everything, adding it to the adjusted graph'''

    #     for i in range(len(self.graph)):
    #         self.clear_nodes()
    #         self.dijkstra(i)
    #         row = []
    #         col = []
    #         for vec in self.nodes:
    #             row.append(vec)
    #         row.sort(key=lambda x: x.id)
    #         for i in row:
    #             col.append(i.total_distance)
    #         self.adjusted_graph.append(col)


    # def get_row(self, row_num):
    #     '''Returns the list found in row_num'''
    #     return self.graph[int(row_num)]


    # def primms(self):

    #     num_address = len(self.graph)
    #     num_edges = 0
    #     selected = [0] * num_address

    #     selected[0] = True

    #     while num_edges < num_address - 1:

    #         smallest = float('inf')
    #         fro = 0
    #         to = 0

    #         for i in range(num_address):
    #             if selected[i]:
    #                 for j in range(num_address):
    #                     if ((not selected[j]) and self.graph[i][j] != 0):
    #                         if float(smallest) > float(self.graph[i][j]):
    #                             smallest = self.graph[i][j]
    #                             fro = i
    #                             to = j
    #         self.edges.append(Edge(fro, to, self.graph[fro][to]))
    #         selected[to] = True
    #         num_edges += 1


    # def print_edges(self):

    #     self.edges.sort(key=lambda x: x.id)
    #     for edge in self.edges:
    #         print(f'From: {int(edge.id):>02}\tTo: {int(edge.to):>02}\tWeight: {float(edge.weight):>4.3}')







def main():
    graph = DistanceGraph()


if __name__ == "__main__":
    main()
