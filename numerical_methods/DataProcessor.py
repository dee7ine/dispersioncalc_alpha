import pandas as pd


class DataProcessor:
    """
    Class for handling numerical
    data returned by dispersion curve
    calculation
    """

    _filepath: str

    @classmethod
    def set_file_path(cls, filepath) -> None:
        cls._filepath = filepath

    def result_to_df(self, result: dict, filename: str) -> pd.DataFrame:
        """
        Converts result dict into Pandas dataframe
        and saves it into .xlsx file

        :param result:
        :param filename:
        :return:
        """

        result = list(result.values())

        main_df = pd.DataFrame()

        for index, _ in enumerate(result):
            temp_df_x = pd.DataFrame(result[index][0], columns=['x'])
            temp_df_y = pd.DataFrame(result[index][1], columns=['y'])
            temp_df = pd.concat([temp_df_x, temp_df_y], axis=1)
            main_df = pd.concat([main_df, temp_df], axis=1)
            # print(pd.DataFrame(values_list[index][0]))
            # x_list.append(pd.DataFrame(values_list[index][0], columns=['x']))
            # y_list.append(pd.DataFrame(values_list[index][1], columns=['y']))

        main_df.to_excel((f'{self._filepath}{filename}.xlsx'), sheet_name='Phase velocity')
        return main_df
