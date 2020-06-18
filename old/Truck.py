from dataclasses import dataclass
from typing import List


@dataclass
class Truck:
    '''
    Docstring
    '''

    onboard_packages: List[Package] = []
    current_location: int = 0

    def load(self, package):
        self.onboard_packages.append(package)

    def deliver(self, id):
        return True


    def __repr__(self):
        return_str = ''

        for packages in self.onboard_packages:
            return_str += str(packages)

        return return_str