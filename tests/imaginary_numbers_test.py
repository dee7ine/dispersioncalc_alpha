import unittest
from material_editor.imaginary_numbers import ImaginaryNumber

im1 = ImaginaryNumber(real_part=5, imaginary_part=4, name = "Marcin")
im2 = ImaginaryNumber(real_part=10, imaginary_part=15)
im3 = ImaginaryNumber(real_part=10, imaginary_part=0)
im4 = ImaginaryNumber(real_part=0, imaginary_part=10)
im5 = ImaginaryNumber(real_part=-3, imaginary_part=-60)

sum1 = im1 + im2
sum2 = im1 + im5

diff1 = im1 - im2

class TestStringMethodsForImaginaryNumbers(unittest.TestCase):
    def test_print(self):
        self.assertEqual(im1.print_self(), '5+4i')
        self.assertEqual(im2.print_self(), '10+15i')
        self.assertEqual(im3.print_self(), '10')
        self.assertEqual(im4.print_self(), '0+10i')
        self.assertEqual(im5.print_self(), '-3-60i')

    def test_sum(self):
        self.assertEqual(sum1, '15+19i')
        self.assertEqual(sum2, '2-56i')

    def test_diff(self):
        self.assertEqual(diff1, '-5-11i')

    def test_attribute(self):
        self.assertEqual(getattr(im1, 'name'), {'name': 'Marcin'})

if __name__ == '__main__':
    unittest.main()
