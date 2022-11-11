from dataclasses import dataclass
from decorators import timeit
from imaginary_numbers import ImaginaryNumber

@dataclass
class IsotropicMaterial:
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

    def __init__(self) -> None:
        parsed_list, material_names_list = self._parse_materials()
        self._name = parsed_list[0][0]
        self._mass_density = float(parsed_list[0][1])
        self._E = float(parsed_list[0][2])
        self._v = float(parsed_list[0][3])
        self._C11 = float(parsed_list[0][4])
        self._C66 = float(parsed_list[0][5])

        #print(type(self._v))
        print(material_names_list)
        print(f"Name: {self._name}, mass-density: {self._mass_density}, E: {self._E}, v: {self._v}, C11: {self._C11}, C66: {self._C66}")

    def _parse_materials(self):
        with open("material_data.txt") as material_data:
            material_data_list = material_data.readlines()
            parsed_material_data = [line.split(' ') for line in material_data_list]

            material_names_list = []
            for i in range(0, len(parsed_material_data)):
                material_names_list.append(parsed_material_data[i][0])

            #print(parsed_material_data)
            #print(material_names_list)
            material_data.close()
            return parsed_material_data, material_names_list

@timeit
def main():
    material = IsotropicMaterial()

if __name__ == "__main__":
    main()