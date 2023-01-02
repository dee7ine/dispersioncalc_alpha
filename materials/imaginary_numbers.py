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


from Decorators import timeit, log
class ImaginaryNumber:

    name: str = "Default"
    real_part: int
    imaginary_part: int
    rep_str: str

    @timeit
    @log
    def __init__(self, real_part: int, imaginary_part: int, **kwargs) -> None:
        """

        :param real_part:
        :param imaginary_part:
        :param kwargs:
        """
        self.name = kwargs
        self.real_part = real_part
        self.imaginary_part = imaginary_part

    def __add__(self, other) -> str:
        """
        :param other:
        :return:
        """
        real_sum =  self.real_part + other.real_part
        im_sum = self.imaginary_part + other.imaginary_part

        if im_sum < 0:
            return f"{real_sum}{im_sum}i"
        elif im_sum == 0:
            return f"{real_sum}"
        else: return f"{real_sum}+{im_sum}i"

    def __sub__(self, other) -> str:
        """
        :param other:
        :return:
        """
        real_difference = self.real_part - other.real_part
        im_difference = self.imaginary_part - other.imaginary_part

        if im_difference < 0:
            return f"{real_difference}{im_difference}i"
        elif im_difference == 0:
            return f"{real_difference}"
        else: return f"{real_difference}+{im_difference}i"

    def print_self(self):
        """
        :return:
        """
        if self.imaginary_part < 0:
            self.rep_str = f"{self.real_part}{self.imaginary_part}i"
        elif self.imaginary_part == 0:
            self.rep_str = f"{self.real_part}"
        else:
            self.rep_str = f"{self.real_part}+{self.imaginary_part}i"

        return self.rep_str

    def get_value(self):
        pass



