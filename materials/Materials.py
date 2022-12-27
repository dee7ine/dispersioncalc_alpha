import os

from dataclasses import dataclass
from Exceptions import NoMaterialFound


@dataclass
class IsotropicMaterial:

    # _frequency = 1000.00

    _filename: str = f'{os.getcwd()}\\materials\\material_data.txt'

    def __init__(self, material: str) -> None:

        """
        Material handling class

        --------------

        Fixed attributes:
        _filename -> default filepath for material data; can be chosen in UI file dialog

        Attributes:
        _name: str -> name of the material on the list
        _index: int -> index of the material on the list
        _density: float or int -> mass density of the material
        _E: float or int -> Young's Modulus of the material
        _v: float or int -> Poisson's ratio of the material
        _C11: float or int -> stiffness component C11
        _C66: float or int -> stiffness component C66


        """

        self._name = material

        parsed_list, material_names_list = self.parse_materials()

        self._material_names_list = material_names_list
        self._index = self._find_material(mat=self._name)

        self._name: str = parsed_list[self._index][0]
        self._density = float(parsed_list[self._index][1])
        self._E = float(parsed_list[self._index][2])
        self._v = float(parsed_list[self._index][3])
        self._C11 = float(parsed_list[self._index][4])
        self._C66 = float(parsed_list[self._index][5])

        print(f"Name: {self._name},"
              f" mass-density: {self._density},"
              f" E: {self._E},"
              f" v: {self._v},"
              f" C11: {self._C11},"
              f" C66: {self._C66}")

    @classmethod
    def fix_file_path(cls, filepath: str) -> None:
        cls._filename = filepath

    @classmethod
    def parse_materials(cls):
        with open(cls._filename, 'r') as material_data:
            material_data_list = material_data.readlines()
            parsed_material_data = [line.split(' ') for line in material_data_list]

            material_names_list = []
            for i in range(0, len(parsed_material_data)):
                material_names_list.append(parsed_material_data[i][0])

            material_data.close()
            return parsed_material_data, material_names_list

    @classmethod
    def new_material(cls, name: str, mass_density: str, e: str, v: str, c11: str, c66: str):
        with open(cls._filename, 'a+') as material_data:

            new_material_data = []
            new_material_data.extend([name, mass_density, e, v, c11, c66])

            print(new_material_data)

            material_data.writelines("\n")
            material_data.writelines(f"{name} {mass_density} {e} {v} {c11} {c66}")

            material_data.close()

    def _find_material(self, mat: str):
        parsed_list, material_names_list = self.parse_materials()

        for index, name in enumerate(material_names_list):
            # print(name)
            if mat in name:
                return index
                # print(index)
        raise NoMaterialFound("No material found. You can create your own material in material editor!")

    @property
    def name(self):
        return self._name

    @property
    def density(self):
        return self._density

    @property
    def e(self):
        return self._E

    @property
    def v(self):
        return self._v

    @property
    def c11(self):
        return self._C11

    @property
    def c66(self):
        return self._C66


def main():

    """
    don't run
    only for testing purposes
    :return:
    """

    Lead = IsotropicMaterial(material='Platinum')
    # print(getattr(material._name))
    print(Lead.__getattribute__(Lead._name))


if __name__ == "__main__":

    ...
