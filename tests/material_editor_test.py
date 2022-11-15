import unittest
from material_editor.materials import IsotropicMaterial

class Test_Material_Editor(unittest.TestCase):
    def test_create_new_material(self):
        isotropic1 = IsotropicMaterial("test_materials.txt")
        marcinek = IsotropicMaterial("test_materials.txt")
        isotropic1._new_material(name="test", mass_density="54", E=" 25", v=" 4", C11="5", C66="665125")
        isotropic1._new_material(name="test2", mass_density="56632", E=" 25", v=" 4", C11="5", C66="66225")
        isotropic1._new_material(name="test3", mass_density="5", E=" 25", v=" 4", C11="5", C66="662424")
        marcinek._new_material(name="test4", mass_density="10000", E=" 25", v=" 4", C11="5", C66="662424")

if __name__ == '__main__':
    unittest.main()
