from Package import Package
from Hash_Table import HashTable

class Edge:
    '''
    Helper class that represents edges in a tree.  
    Used with the Truck class when finding the minimum spanning tree
    '''

    def __init__(self, fro, to, weight):
        self.fro = fro
        self.to = to
        self.weight = weight


class Truck:
    '''A truck class that stores and delivers packages'''


    def __init__(self, payload):
        '''Initializes truck with payload list of packages'''   
        self.address_book = HashTable().graph
        self.cargo = payload
        self.edges = []
        self.millage = 0.0
        self.current_location = 0


    # Rewritten, now clean up
    def deliver_package(self, package):
        '''delivers package'''

        self.millage += float(self.address_book[int(self.current_location)][int(package.address_id)])
        print(f'Package {package.package_id:>02} at {package.address_id:>02} for {float(self.address_book[int(self.current_location)][int(package.address_id)]):>4.2} miles now at {self.millage}')
        self.current_location = package.address_id
        package.status = 'DELIVERED at time...'        # Make hashtable update instead?

    # Rewritten, now clean up
    def run_deliveries(self):
        '''Delivers all packages on truck'''

        self.find_minimum_spanning_tree()
        path = self.get_dfs_path()
        deliveries = []

        for address in path:
            deliveries.extend(self.get_packages_from_address(address))

        for package in deliveries:
            self.deliver_package(package)

        self.millage += float(self.address_book[int(self.current_location)][0])
        self.current_location = 0

    # Rewritten, now clean up
    def get_packages_from_address(self, address):
        '''Returns a packages from cargo in list form based on address_id'''

        packages = []

        # Iterates through a copy of cargo.  
        # If package address matches address id, remove from cargo and add to packages
        for package in self.cargo[:]:
            if int(package.address_id) == int(address):
                packages.append(self.cargo.pop(self.cargo.index(package)))

        return packages

    # Rewritten, now clean up
    def find_minimum_spanning_tree(self):

        addresses = [0]

        for i in self.cargo:
            if int(i.address_id) not in addresses:
                addresses.append(int(i.address_id))
        
        num_address = len(addresses)
        num_edges = 0
        selected = [0] * num_address
        selected[0] = True

        while num_edges < num_address - 1:

            smallest = float('inf')
            fro = 0
            to = 0

            for i in range(num_address):
                if selected[i]:
                    for j in range(num_address):
                        x = int(addresses[i])
                        y = int(addresses[j])

                        if ((not selected[j]) and self.address_book[x][y] != 0):
                            if float(smallest) > float(self.address_book[x][y]):
                                smallest = float(self.address_book[x][y])
                                fro = x
                                to = y
            self.edges.append(Edge(fro, to, float(self.address_book[fro][to])))
            selected[addresses.index(to)] = True
            num_edges += 1

    #Rewritten, now clean up
    def get_dfs_path(self):

        visited = [0]
        unvisited = []

        for i in self.cargo:
            if int(i.address_id) not in unvisited:
                unvisited.append(int(i.address_id))

        current = 0

        while unvisited:
            found = False

            for edge in self.edges:
                if (int(edge.fro) == current) and (edge.to not in visited):
                    visited.append(edge.to)
                    unvisited.remove(int(edge.to))
                    current = edge.to
                    found = True
            
            if found == False:
                for edge in self.edges:
                    if int(edge.to) == current:
                        visited.append(int(edge.fro))
                        current = edge.fro
                        break
        
        
   
        # Returns the path with duplicates removed
        return list(dict.fromkeys(visited))

    def num_addresses(self):
        '''Find the total number of unique addresses on truck and returns it'''

        unique_addresses = []

        for p in self.cargo:
            if p.address_id not in unique_addresses:
                unique_addresses.append(p.address_id)

        return len(unique_addresses)

# delay_i = [1,2,4,6,7,17,22,24,25,26,28,29,31,32,33,40]
# must_sec = [3,8,10,13,14,15,16,18,19,20,30,34,36,37,38,39]
# third_i = [5,9,11,12,21,23,27,35]