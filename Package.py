from dataclasses import dataclass
from typing import List

@dataclass
class Package:
    '''
    Holds data on packages.  
    '''

    package_id: int
    address_id: int = None
    address: str = None
    deadline: str = None
    city: str = None
    state: str = None
    zip_code: str = None    
    weight: float = None
    status: str = 'At Hub'
    instructions: str = None

    # Needs finalization  (DELETE???)
    def distance_to(self, address_id):
        return self.distances[address_id]

    # Needs finalization (DELETE???)
    def __repr__(self):
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
        '''

    # Needs finalization
    def __str__(self):
        return f'ID = {self.package_id:>02}\t\tAddress = [{self.address_id:>02}] {self.address:>39} {self.city:>16},{self.state:<2} {self.zip_code:<15}Weight = {self.weight:<3}\t\tInstruction = {self.instructions:<60}\t\tStatus = {self.status}'

    # Needs finalization
    def __eq__(self, other):
        return self.package_id == other.package_id