from dataclasses import dataclass
from decorators import timeit
from material_editor.imaginary_numbers import ImaginaryNumber

class Material_File_Parser:
    material_list : list
    material_names_list : list

    def __init__(self):
        pass


@dataclass
class IsotropicMaterial:

    _filename: str

    _name: str
    _mass_density: float

    _longitudinal_velocity = 6142.03
    _shear_velocity = 3093.85
    _frequency = 1000

    """
    Engineering constants and
    stiffness components
    """

    _E = ImaginaryNumber(0, 0)
    _v = ImaginaryNumber(0, 0)

    _C11 = ImaginaryNumber(0, 0)
    _C66 = ImaginaryNumber(0, 0)

    """
    DO NOT DELETE THIS COMMENT
    
    Fix setting real and imaginary attributes of E, v and 
    stiffness coefficients
    """

    def __init__(self, filename: str) -> None:

        #self._new_material(name = "test", mass_density = "5", E = " 25", v = " 4", C11 = "5", C66 = "66")
        self._filename = filename
        parsed_list, material_names_list = self._parse_materials()

        self._name = parsed_list[0][0]
        self._mass_density = float(parsed_list[0][1])
        self._E = float(parsed_list[0][2])
        self._v = float(parsed_list[0][3])
        self._C11 = float(parsed_list[0][4])
        self._C66 = float(parsed_list[0][5])

        print(material_names_list)
        print(f"Name: {self._name},"
              f" mass-density: {self._mass_density},"
              f" E: {self._E},"
              f" v: {self._v},"
              f" C11: {self._C11},"
              f" C66: {self._C66}")

    def _parse_materials(self):
        with open(self._filename, 'r') as material_data:
            material_data_list = material_data.readlines()
            parsed_material_data = [line.split(' ') for line in material_data_list]

            material_names_list = []
            for i in range(0, len(parsed_material_data)):
                material_names_list.append(parsed_material_data[i][0])

            material_data.close()
            return parsed_material_data, material_names_list

    def _new_material(self, name: str, mass_density: str, E: str, v: str, C11: str, C66: str):
        with open(self._filename, 'a+') as material_data:

            new_material_data = []
            new_material_data.extend([name, mass_density, E, v, C11, C66])

            print(new_material_data)

            material_data.writelines("\n")
            material_data.writelines(f"{name} {mass_density} {E} {v} {C11} {C66}")

            material_data.close()

@timeit
def main():
    material = IsotropicMaterial()

if __name__ == "__main__":
    main()