class Node:
    '''
    Contains address_id, distance from hub & previous path info.  
    Helper class for DistanceGraph
    '''

    def __init__(self, id):
        self.id = id
        self.total_distance = float('inf')
        self.prev_address = id
