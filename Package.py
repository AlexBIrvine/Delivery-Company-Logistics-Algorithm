from dataclasses import dataclass
from typing import List

@dataclass
class Package:
    '''
    Holds data on packages.  
    '''

    package_id: int
    address_id: int = None
    site_name: str = None
    address: str = None
    deadline: str = None
    city: str = None
    zip_code: str = None    
    weight: float = None
    status: str = 'At Hub'
    instructions: str = None
    distances: List[float] = None

    def distance_to(self, address_id):
        return self.distances[address_id]

    def __str__(self):
        return f'''
        ID = {self.package_id}
        A_ID = {self.address_id}
        address = {self.address}
        deadline = {self.deadline}
        city = {self.city}
        zip code = {self.zip_code}
        weight = {self.weight}
        status = {self.status}
        instructions = {self.instructions}
        distances = {self.distances}
        '''

    def __eq__(self, other):
        return self.package_id == other.package_id