'''

This works with groups of whiskies.

v2
generate_group_whisky_df now uses the WhiskyGroup class.

'''
import pandas as pd
import matplotlib.pyplot as plt
from WhiskyGroupClass import WhiskyGroup
from os import path, getcwd, listdir, mkdir
from whisky_excel_IO_v2 import SAVE_PATH_HISTORICAL

'''
FUTURE IMPROVEMENTS:
    Instead of replacing NaN with the previous price, make the price linearly change to meet the next price.
'''
def generate_group_whisky_df(distillery, barrel_code):
    # This will make a DF containing the prices against dates for all whiskies of a particular brand and barrel code.
    # E.G: For Auchroisk HHR we get a DF containing the dates/prices of Auchroisk HHR with all the different bond dates.
    whisky_group = WhiskyGroup(distillery, barrel_code)
    df_list = whisky_group.get_group_dfs("historic")
    final_df = df_list[0].set_index("Date")
    for df in df_list[1:]:
        # Starting with the second element in the list, since we have already set final_df to be the first element.
        final_df = pd.merge(final_df, df.set_index("Date"), left_index=True, right_index=True, how="outer")
    final_df.fillna(method="ffill", inplace=True)  # When a price/date pair is missing for a column, use the last price
    return final_df


def control_function():
    print("Choose between: ")
    print("\t \'1\' - Export charts for all whisky groups.")
    print("\t \'2\' show chart for a particular whisky group.")
    user_input = input("Choice: ")
    if user_input == '1':
        print("\nThis script will export a chart for every whisky group.")
        export_all_whisky_group_charts()
        input("Charts exported.\nPress any key to exit.")
    elif user_input == '2':
        print("\nThis script will generate a chart for all whiskies belonging to a group. E.G: Auchroisk HHR")
        __distillery = input("Please enter the distillery: ")
        __barrel_code = input("Please enter the barrel code: ")
        generate_group_chart(__distillery, __barrel_code)
        plt.show()


def export_all_whisky_group_charts():
    distillery_list = listdir(SAVE_PATH_HISTORICAL)
    for distillery in distillery_list:
        for barrel_code in listdir(path.join(SAVE_PATH_HISTORICAL, distillery)):
            generate_group_chart(distillery, barrel_code)

            save_path = path.join(getcwd(), "Charts")
            if "Charts" not in listdir(getcwd()):
                mkdir(save_path)

            whisky_group = distillery.capitalize() + ' ' + barrel_code.upper()
            plt.savefig(path.join(save_path, whisky_group + ".png"), bbox_inches="tight")
            plt.close()


def generate_group_chart(distillery, barrel_code):
    df = generate_group_whisky_df(distillery, barrel_code)
    df.to_excel("output.xlsx", "sheet1")
    whisky_group = distillery.capitalize() + ' ' + barrel_code.upper()
    df.plot(title=whisky_group, figsize=(16, 9))

control_function()