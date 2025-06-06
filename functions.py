import pandas as pd
import numpy as np
min_data_year = 1880
max_data_year = 2025
data = pd.read_csv("SSANameData.txt")
def name_counts_years(name, sex, year, min_y = min_data_year, max_y = max_data_year, function = np.equal):
    current_data = data[function(name, data['name'])]
    length = len(current_data)
    current_data = current_data[current_data['sex'] == sex]
    length = len(current_data)
    current_data.loc['total'] = current_data.sum(numeric_only=True)
    current_data.loc['num_names'] = (current_data.iloc[0:length] != 0).sum(axis=0)

    year_columns = [str(y) for y in range(min_y, max_y)]
    name_counts = current_data.loc['total', year_columns].tolist()
    # name_counts = current_data[year_columns]
    num_names = current_data.loc['num_names',  (str(min_y)):(str(max_y - 1))].tolist()
    # num_names = (current_data[year_columns] != 0).sum()
    return name_counts, num_names