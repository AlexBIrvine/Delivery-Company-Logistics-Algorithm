from Truck import Truck
from Hash_Table import HashTable
import datetime


receiveing = HashTable()
start_2 = datetime.datetime.combine(datetime.date.today(), datetime.time(8,0))
truck2 = Truck(receiveing.handload_truck_2(), start_2, 2, receiveing)



print(truck2)
truck2.run_deliveries()
print(truck2)

# start_1 = datetime.datetime.combine(datetime.date.today(), datetime.time(9,5))
# truck1 = Truck(receiveing.handload_truck_1(), start_1, 1, receiveing)
# print(truck1)
# truck1.run_deliveries()
# print(truck1)

# start_3 = datetime.datetime.combine(datetime.date.today(), truck2.time.time())
# truck3 = Truck(receiveing.handload_truck_3(), start_3, 3, receiveing)
# print(truck3)
# truck3.run_deliveries()
# print(truck3)

# print(receiveing)