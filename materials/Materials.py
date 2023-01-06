"""
=========================================================================
Tool for dispersion calculation

Created by Bartlomiej Jargut
https://github.com/dee7ine

Lamb wave class implemented by Francisco Rotea
https://github.com/franciscorotea
-------------------------------------------------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

=========================================================================
"""


from __future__ import annotations

import os
from dataclasses import dataclass
from Exceptions import NoMaterialFound, ErrorParsingMaterial, ErrorCreatingMaterial


@dataclass
class IsotropicMaterial:

    # _frequency = 1000.00

    _filename: str = f'{os.getcwd()}\\material_data.txt'

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

        # parsed_list, material_names_list = self.parse_materials()

        self._parsed_material_data, self._material_names_list = self.parse_materials()
        self._index = self._find_material(material=self._name)

        self._name: str = self._parsed_material_data[self._index][0]
        self._density = float(self._parsed_material_data[self._index][1])
        self._E = float(self._parsed_material_data[self._index][2])
        self._v = float(self._parsed_material_data[self._index][3])
        self._C11 = float(self._parsed_material_data[self._index][4])
        self._C66 = float(self._parsed_material_data[self._index][5])

        print(f"Name: {self._name},"
              f" mass-density: {self._density},"
              f" E: {self._E},"
              f" v: {self._v},"
              f" C11: {self._C11},"
              f" C66: {self._C66}")

    @classmethod
    def fix_file_path(cls: IsotropicMaterial, filepath: str) -> None:
        """
        Method setting data file path
        :param filepath:

        :return:
        """
        cls._filename = filepath

    @classmethod
    def parse_materials(cls: IsotropicMaterial) -> tuple[list[list[str]], list[str]]:
        """
        File parsing method - parses file contents into
        list of names and list of data

        :return:
        """
        with open(cls._filename, 'r') as material_data:
            try:
                material_data_list = material_data.readlines()
                parsed_material_data = [line.split(' ') for line in material_data_list]

                material_names_list = []
                for i in range(0, len(parsed_material_data)):
                    material_names_list.append(parsed_material_data[i][0])

                material_data.close()

                return parsed_material_data, material_names_list

            except Exception:
                raise ErrorParsingMaterial

    @classmethod
    def new_material(cls: IsotropicMaterial, name: str, density: str, e: str, v: str, c11: str, c66: str) -> None:
        """
        Create new material with given parameters

        :param name: Name
        :param density: Density
        :param e: Young's Modulus
        :param v: Poisson's ratio
        :param c11: Engineering constant c11
        :param c66: Engineering constant c66

        :return:
        """
        with open(cls._filename, 'a+') as material_data:
            try:
                new_material_data = []
                new_material_data.extend([name, density, e, v, c11, c66])

                print(new_material_data)

                material_data.writelines("\n")

                # conversion of Young's modulus to GPa

                if '.' in e:
                    material_data.writelines(f"{name} {density} {e.replace('.', '', 1)}00000000 {v} {c11} {c66}")
                else:
                    material_data.writelines(f"{name} {density} {e}000000000 {v} {c11} {c66}")

                material_data.close()
            except Exception:
                raise ErrorCreatingMaterial

    def _find_material(self, material: str) -> int:
        """
        Function that finds material of given name

        :param material: name of the material

        :return:
        """

        parsed_list, material_names_list = self.parse_materials()

        for index, name in enumerate(material_names_list):
            # print(name)
            if material in name:
                return index
                # print(index)
        raise NoMaterialFound("No material found. You can create your own material in material editor!")

    def _validate_data_file(self) -> bool:
        """
        Method validating data file

        :return:
        """

        valid: bool = True

        for index, line in enumerate(self._parsed_material_data):
            if len(line) == 6:
                ...

        return valid

    @property
    def name(self) -> str:
        return self._name

    @property
    def density(self) -> float:
        return self._density

    @property
    def e(self) -> float:
        return self._E

    @property
    def v(self) -> float:
        return self._v

    @property
    def c11(self) -> float:
        return self._C11

    @property
    def c66(self) -> float:
        return self._C66


def main() -> None:

    """
    don't run
    only for testing purposes
    :return:
    """

    Lead = IsotropicMaterial(material='Platinum')
    # print(getattr(material._name))
    print(Lead.name)


if __name__ == "__main__":

    main()
