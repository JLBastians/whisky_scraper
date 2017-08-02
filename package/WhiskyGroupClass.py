import pandas as pd
from os import listdir, path, getcwd
from whisky_excel_IO import SAVE_PATH_CURRENT, SAVE_PATH_HISTORICAL


class WhiskyGroup:
    # A class that groups whiskies together by their distillery and barrel code. E.G: Starlaw HHR
    def __init__(self, distillery, barrel_code):
        self.distillery = distillery
        self.barrel_code = barrel_code

        self.current_distillery_directory = path.join(SAVE_PATH_CURRENT, self.distillery)
        self.current_group_directory = path.join(self.current_distillery_directory, self.barrel_code)
        self.historic_distillery_directory = path.join(SAVE_PATH_HISTORICAL, self.distillery)
        self.historic_group_directory = path.join(self.historic_distillery_directory, self.barrel_code)

    def get_group_dfs(self, dataset):
        # This returns a dict containing the df for each whisky in the group, keyed by its fill period.
        if dataset == "current":
            working_directory = self.current_group_directory
        elif dataset == "historic":
            working_directory = self.historic_group_directory
        else:
            return 0

        whisky_list = listdir(working_directory)
        df_list_of_tuples = []
        for whisky_file_name in whisky_list:
            whisky_file = path.join(working_directory, whisky_file_name)
            df = pd.read_excel(whisky_file)  # Ideally we would specify the sheetname, but the historic data has no sheet name. Could fix.
            whisky_id_fill_period = self.get_file_name_components(whisky_file_name)["fill_period"]
            df_tuple = (whisky_id_fill_period, df)
            df_list_of_tuples.append(df_tuple)
        return df_list_of_tuples

    def get_file_name_components(self, file_name):
        # This decomposes the file name and organizes the name of distillery, bond period and barrel code into a dict.
        file_name = file_name.replace('_', " ")
        file_name = file_name.split()
        return {"distillery": file_name[0], "fill_period": file_name[1], "barrel_code": file_name[2]}
