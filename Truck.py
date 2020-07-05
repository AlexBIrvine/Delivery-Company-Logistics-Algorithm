from Package import Package
from Hash_Table import HashTable
from decimal import Decimal
import datetime

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


    def __init__(self, payload, start_time, truck_num, warehouse):
        '''Initializes truck with payload list of packages'''   
        self.warehouse = warehouse
        self.address_book = self.warehouse.graph
        self.time = start_time
        self.cargo = payload
        self.number = truck_num
        self.edges = []
        self.millage = 0.0
        self.current_location = 0
        self.miles_to_next = 0.0

        # Runs the sort_package method to order packages by delivery order, 
        # 
        self.sort_packages()
        self.find_miles_to_next()


    def find_miles_to_next(self):
        '''
        Finds the miles to the next package and updates miles_to_next.
        '''
        self.miles_to_next += round(float(self.address_book[int(self.current_location)][int(self.cargo[0].address_id)]), 1)


    # Rewritten, now clean up
    def deliver_package(self, package):
        '''
        Delivers package passed in as argument.  
        This will get the miles between truck's current address and the packages address, 
        update the total miles driven for the tuck, 
        update the time of the truck, 
        update the current location of the tuck, 
        and set the status of the package with details of delivery.  
        '''

        # miles_driven = round(float(self.address_book[int(self.current_location)][int(package.address_id)]), 1)
        # self.millage += round(miles_driven,1)
        # self.update_time(miles_driven)
        self.find_miles_to_next()
        self.current_location = package.address_id
        status = f'DELIVERED at {self.time.time()} on truck #{self.number}'
        self.warehouse.update_package(package, status)

    def deliver_next(self):
        '''
        Delivers the next package cargo.  
        If no package is left in cargo and truck is not at the hub, returns to hub.  
        '''

        if len(self.cargo) > 0:
            self.deliver_package(self.cargo.pop(0))
        elif len(self.cargo) == 0 and self.current_location != 0:
            self.millage += round(float(self.address_book[int(self.current_location)][0]), 1)
            self.current_location = 0

    def tick(self):
        '''
        Moves the truck 0.1 miles and delivers a package if at location
        '''

        if round(self.millage, 1) == round(self.miles_to_next, 1):
            self.deliver_next()
        else:
            self.millage += round(0.1, 1)
            self.update_time(0.1)


    # NOW BROKEN -- Need to fix, issue lies in updating miles to next
    def run_deliveries(self):
        '''delivers all packages'''
        while len(self.cargo) > 0:
            self.tick()
        

    # Rewritten, now clean up
    def sort_packages(self):
        '''
        Sorts packages in cargo in order of the shortest path.  
        '''

        self.find_minimum_spanning_tree()
        path = self.get_dfs_path()
        deliveries = []

        for address in path:
            deliveries.extend(self.get_packages_from_address(address))

        self.cargo = deliveries

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

    def update_time(self, miles):
        '''
        Updates current time of truck based on miles driven. 
        All trucks within this project drive at a constant 18 MPH, 
        or 200 seconds per mile. 
        '''

        SECONDS_PER_MILE = 200
        driven = datetime.timedelta(0, SECONDS_PER_MILE * miles)
        self.time += driven

    def __repr__(self):
        '''
        Returns a string for the status of the truck.  
        Includes total packages on truck, millage & time.
        '''
        return f'Truck #{self.number}\nPackage count =\t{len(self.cargo)}\nMilliage =\t{round(self.millage, 1)}\nMiles to next = {round(self.miles_to_next, 1)}\nTime =\t\t{self.time.time()}\n'
