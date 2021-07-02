import pandas as pd
import numpy as np
import re

'''
def splitCsvCols(df):
    df["c_wet_brake_wind_speed_range"] = df["c_wet_brake_wind_speed_range"].str.lower()
    print(df['c_wet_brake_wind_speed_range'].count)
    df = df[df["c_wet_brake_wind_speed_range"].notna()]
    print(df['c_wet_brake_wind_speed_range'].count)
    df = df[df['c_wet_brake_wind_speed_range'].str.contains(r'(min: )?(\d*\.?\d*)( (max:|to|til|\-) )(\d*\.?\d*)')]
    print(df['c_wet_brake_wind_speed_range'].count)
    temp = df['c_wet_brake_wind_speed_range'].str.extractall(r'(min: )?(\d*\.?\d*)( (max:|to|til|\-) )(\d*\.?\d*)')
    df['c_wet_brake_wind_speed_min'] = temp[1].values
    df['c_wet_brake_wind_speed_max'] = temp[4].values
    print(df['c_wet_brake_wind_speed_range'].count)
    df.to_csv("test.csv")
    '''

def cleanMost(df):
    # lowercase and drop null
    df["c_wet_brake_wind_speed_range"] = df["c_wet_brake_wind_speed_range"].str.lower()
    totalCount = len(df.index)
    df = df[df["c_wet_brake_wind_speed_range"].notna()]
    nonNullCount = len(df.index)

    # identify and extract ranges with 2 numbers, 'low', or 1 number with km/h
    df = df[df['c_wet_brake_wind_speed_range'].str.contains(r'(min: )?(\d*\.?\d*)( (max:|to|til|\-) )(\d*\.?\d*)|(low|no)|^(\d*\.?\d*)[ ]?km\/h')]
    temp = df['c_wet_brake_wind_speed_range'].str.extractall(r'(min: )?(\d*\.?\d*)( (max:|to|til|\-) )(\d*\.?\d*)|(low|no)|^(\d*\.?\d*)[ ]?km\/h')
    df.reset_index(drop=True, inplace=True)
    temp.reset_index(drop=True, inplace=True)

    # combine, conditionally set max and min, and drop columns as needed
    df = pd.concat([df, temp], axis = 1)
    conditions = [(df[1].notna()) & (df[4].notna()), (df[5] == 'low') | (df[5] == 'no'), (df[6].notna())]
    choices1 = [df[1], 0.0, df[6]]
    choices2 = [df[4], 0.0, df[6]]
    df['c_wet_brake_wind_speed_min'] = np.select(conditions, choices1)
    df['c_wet_brake_wind_speed_max'] = np.select(conditions, choices2)
    df = df.drop(columns=[0,1,2,3,4,5,6])
    finalCount = len(df.index)

    df.to_csv("cleaned_wind.csv")
    print("Percent of original data successfully cleaned: " + str(100 * finalCount / totalCount))
    print("Percent of non null data successfully cleaned: " + str(100 * finalCount / nonNullCount))


if __name__ == "__main__":
    df = pd.read_csv("Files/wetbrk_test_data_2020.csv")

    #splitCsvCols(df)
    cleanMost(df)

