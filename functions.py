import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
default_color = 'xkcd:periwinkle'
min_data_year = 1880
max_data_year = 2025
data = pd.read_csv("SSANameData.txt")
generation_starts = {'Missionary' : 1880, 'Lost' : 1883, 'Greatest' : 1901, 'Silent' : 1928, 'Boomers' : 1946, 'Gen X' : 1965, 'Milennial' : 1981,
                     'Gen X' : 1997, 'Gen Alpha' : 2010, 'Gen Beta' : 2025}
def name_counts_years(name, sex, min_y = min_data_year, max_y = max_data_year, function = np.equal):
    """Finds the total count and unique number of names that are equal to (or other function) the given name
    with the associated sex. The min_y and max_y (non-inclusive) change the range of years
    """
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

def name_input(input_type = "name"):
    """Asks the user for the name and associated sex
    """
    name = input(f"Enter the {input_type}: ").lower()
    sex = ""
    while sex != 'f' and sex != 'm':
        sex = input("Enter M for Male and F for Female: ").lower()
    return name, sex

def single_line_name_input():
    """Gets the general input for graphing a name as a single line for simplicity
    """
    line = input("Enter name, sex, single year, min year, max_year sparated by comma, no spaces: ")
    return line

def year_input():
    """Asks the user for the year range otherwise uses the default min and max
    """
    enter_years = input("Enter y to set min/max years and q for default: ").lower()
    min_y = 0
    max_y = 0
    if enter_years == "y":
        while min_y < min_data_year or max_y > max_data_year:
            print(f"the data ranges from {min_data_year} to {max_data_year - 1}")
            min_y = int(input("Enter the minimum year: "))
            max_y = int(input("Enter the maximum year: "))
        max_y += 1
    else:
        min_y = min_data_year
        max_y = max_data_year
    return min_y, max_y

def single_year_input(min_y = min_data_year, max_y = (max_data_year - 1), type = "count"):
    """Asks the user for a single year within the range of years given
    """
    year = 0
    while year < min_y or year > max_y:
        print(f"the data ranges from {min_y} to {max_y}")
        try:
            year = int(input(f"Enter a specific year to see the {type}"))
        except ValueError:
            print("please enter a number")
    return year

def gens_years_input(generation_starts):
    """Asks the user for year input by either using generation definitions or specific years
    """
    choice = input("Enter 'g' to use one generation, 'y' to use years, 'a' to use all names: ").lower()
    if choice == 'g':
        print(f"The generations are: Missionary (0) 1880-1882, Lost (1) 1883-1900, Greatest (2) 1901-1927, Silent (3) "+
                "1928-1945, \nBoomer (4) 1946-1964, X (5) 1965-1980, Millennial (6) 1981-1996, Z (7) 1997-2009, Alpha (8) 2010-2024")
        choice = int(input("Enter the number corresponding with the desired generation: "))
        min_y = generation_starts[list(generation_starts.keys())[choice]]
        max_y = generation_starts[list(generation_starts.keys())[choice + 1]]
    elif choice == 'y':
        min_y, max_y = fun.year_input()
    else:
        min_y = min_data_year
        max_y = max_data_year
    return min_y, max_y


def multiple_inputs():
    """Asks the user for multiple names and their associated sexes.
    Then gets year range and single year and returns a list of names, list of sexes, and the years
    """
    stop = False
    name_list = []
    sex_list = []
    while stop == False:
        name, sex, cont = input("Enter name, sex, continue (c or q) sparated by comma, no spaces: ").lower().split(',')
        name_list.append(name)
        sex_list.append(sex)
        stop = (cont == 'q')
    min_y, max_y = year_input()
    year = single_year_input(min_y, max_y)
    return name_list, sex_list, year, min_y, max_y

def first_nonzero(name_list, min_y = min_data_year):
    """Returns the first year in a list of counts of a name where the value is > 0
    """
    name_list = np.array(name_list)
    i = np.nonzero(name_list)
    return i[0][0] + min_y

def last_nonzero(name_list, min_y = min_data_year):
    """Returns the last year in a list of counts of a name where the value is > 0
    """
    name_list = np.array(name_list)
    i = np.nonzero(name_list)
    return i[0][-1] + min_y

def peak_year(name_list, min_y = min_data_year):
    """Returns the year in a list of counts of a name where the count was the highest
    """
    max_value = max(name_list)
    max_index = name_list.index(max_value) + min_y
    return max_index, int(max_value)

def calculate_percent_change(name_counts):
    """Calculates the percent change in the count of a name over the entire list of name counts
    """
    initial = name_counts[0]
    initial = initial if initial > 0 else 1
    final = name_counts[-1]
    final = final if final > 0 else 1
    return (final - initial) / initial * 100, int(initial), int(final)

def calculate_percent_diff(v1, v2):
    """Calculates the percent difference in the values of two numbers
    On a scale of 0-200 (200 meaning very different) until I figure out what I did wrong
    """
    if v1 == 0 or v2 == 0:
        return 200
    return abs(v1 - v2) / ((v1 + v2) / 2) * 100

def get_rank(name, sex, year):
    """Returns the rank of a name with its associated sex in the given year where 1 means it
    was the most popular name that year. -1 means it was not in the dataset for that year
    """
    current_data = pd.read_csv("names/yob" + str(year) + ".txt", names = ['Name', 'Sex', 'Count'])
    current_data = current_data[current_data['Sex'] == sex.upper()]
    name_list = current_data['Name'].apply(lambda x : x.lower()).tolist()
    if name in name_list:
        return name_list.index(name) + 1
    else:
        return -1
    
def make_graph(title, x, y, year, label, color = default_color, show = True, x_label = 'year', y_label = 'count'):
    """Creates a line graph with the given label and formats it
    """
    plt.plot(x, y, color = color, label = label)
    format_graph(title, year, show, x_label, y_label)

def format_graph(title, year, show = True, x_label = 'year', y_label = 'count'):
    """Formats the graph to have labels, legend, grid, and if show is True, then a line to mark the specified year
    """
    if show == True:
        plt.axvline(x = year, label = year, color = 'xkcd:grey', linestyle = '--')
    plt.xlabel(y_label)
    plt.ylabel(x_label)
    plt.legend()
    plt.title(title)
    plt.grid(True)

def top_names(sex, min_y = min_data_year, max_y = max_data_year):
    """Sums up the year counts for each year in the range and sorts the names from most to least popular
    """
    if sex == 'f' or sex == 'm':
        top = data[data['sex'] == sex]
    else:
        top = data
    names = top['name']
    sexes = top['sex']
    year_columns = [str(y) for y in range(min_y, max_y)]
    top = top.loc[:, year_columns]
    top['total'] = top.sum(axis = 1)
    top = top.drop(year_columns, axis = 1)
    top.index = names
    top['sex'] = list(sexes)
    top = top.sort_values(by = 'total', ascending = False)
    return top

def narrow_top_popularity(top):
    """To be used with the dataframe returned by top_names method to find names in a certain section of the popularity
    """
    print("The popularity options are: extremely popular (1), very popular (2), common (3), uncommon(4), \n\trare (5), ultra rare (6), ignore (7)")
    choice = int(input("Enter the number for the popularity: "))
    popularities = {'0' : 0, 'e' : 0.01, 'v' : 0.025, 'c' : 0.075, 'u' : 0.2, 'r' : 0.5, 'b' : 1,}
    top = top[top['total'] > 0]
    top = top.sort_values(by = 'total', ascending = False)
    if choice != 7:
        top_percent = popularities[list(popularities.keys())[choice - 1]]
        bottom_percent = popularities[list(popularities.keys())[choice]]
        top_index = int(len(top)*top_percent)
        if choice == 6:
            bottom_index = len(top)
        else:
            bottom_index = int(len(top)*bottom_percent)
        top = top.iloc[top_index:bottom_index]
    return top

def biggest_rank_jump(name, sex, min_y = min_data_year, max_y = max_data_year):
    """Finds the largest number of ranks the name jumped in a single year over the range
    """
    ranks = []
    for i in range(min_y, max_y):
        ranks.append(get_rank(name, sex, i))
    biggest_jump = 0
    first_year = 0
    second_year = 0
    rank_1 = 0
    rank_2 = 0
    for i in range(1, len(ranks)):
        if abs(ranks[i] - ranks[i-1]) > biggest_jump and ranks[i] != -1 and ranks[i-1] != -1:
            biggest_jump = (ranks[i] - ranks[i-1]) * -1
            first_year = i - 1
            second_year = i
            rank_1 = ranks[i-1]
            rank_2 = ranks[i]
    first_year += min_y
    second_year += min_y
    return biggest_jump, first_year, second_year, rank_1, rank_2
    