import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
default_color = 'xkcd:periwinkle'
min_data_year = 1880
max_data_year = 2026

def read_years(min_y, max_y):
    global min_data_year, max_data_year
    min_data_year = min_y
    max_data_year = max_y


def read_data(file_path):
    year_list_f = []
    year_list_m = []
    for i in range(min_data_year,max_data_year):
        file_name = file_path + "/yob" + str(i) + ".txt"
        df_f = pd.read_csv(file_name, delimiter = ",", names = ['Name', 'Sex', 'Count'])
        df_f['Name'] = df_f['Name'].apply(lambda x : x.lower())
        df_m = df_f[~df_f.Sex.str.contains('F')]
        df_f = df_f[~df_f.Sex.str.contains('M')]
        df_m = df_m.reset_index(drop = True)
        year_list_f.append(df_f)
        year_list_m.append(df_m)
    return year_list_f, year_list_m

def init(min_y, max_y, data_path="names"):
    global year_list_f, year_list_m
    read_years(min_y, max_y)
    year_list_f, year_list_m = read_data(data_path)

def get_year_list(sex):
    """Returns the appropriate list given the sex"""
    sex = sex.lower()
    return year_list_f if sex == 'f' else year_list_m

def get_year_list_one(sex, year):
    """Returns the appropriate dataframe given the sex and year"""
    l = year_list_f if sex == 'f' else year_list_m
    return l[year - min_data_year]

def name_counts_years(name, sex, min_y = min_data_year, max_y = max_data_year, function = "equal"):
    """Finds the total count and unique number of names that are equal to (or other function) the given name
    with the associated sex. The min_y and max_y (non-inclusive) change the range of years
    """
    name = name.lower()
    sex = sex.lower()
    year_list = get_year_list(sex)
    name_counts = []
    num_names = []
    for i in range(min_y, max_y):
        current_sum = 0
        current_df = year_list[i - min_data_year]
        if function == 'equal':
            current_df = current_df[current_df['Name'] == name]
        elif function == 'start':
            current_df = current_df[current_df['Name'].str.startswith(name)]
        elif function == 'end':
            current_df = current_df[current_df['Name'].str.endswith(name)]
        else:
            print("function not supported")
            return [], []
        current_sum = current_df['Count'].sum()
        name_counts.append(current_sum)
        num_names.append(len(current_df))
    return name_counts, num_names

def name_counts_simple(name, sex, min_y = min_data_year, max_y = max_data_year, function = "equal"):
    """Similar as name_counts_years but returns only the sum and the total names as integers instead of list"""
    year_list = get_year_list(sex)
    name_counts = 0
    num_names = 0
    for i in range(min_y, max_y):
        current_df = year_list[i - min_data_year]
        if function == 'equal':
            current_df = current_df[current_df['Name'] == name]
        elif function == 'start':
            current_df = current_df[current_df['Name'].str.startswith(name)]
        elif function == 'end':
            current_df = current_df[current_df['Name'].str.endswith(name)]
        else:
            print("function not supported")
            return -1, -1
        name_counts += current_df['Count'].sum()
        num_names += len(current_df)
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
                "1928-1945, \nBoomers (4) 1946-1964, X (5) 1965-1980, Millennial (6) 1981-1996, Z (7) 1997-2009, Alpha (8) 2010-2024")
        choice = int(input("Enter the number corresponding with the desired generation: "))
        # choice = input("Enter the exact name for the generation")
        years = generation_starts[list(generation_starts.keys())[choice]]
        min_y = years[0]
        max_y = years[1]
    elif choice == 'y':
        min_y, max_y = year_input()
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
    i = np.nonzero(name_list)[0]
    if i.size == 0:
        return max_data_year
    return i[0] + min_y

def last_nonzero(name_list, min_y = min_data_year):
    """Returns the last year in a list of counts of a name where the value is > 0
    """
    name_list = np.array(name_list)
    i = np.nonzero(name_list)[0]
    if i.size == 0:
        return max_data_year
    return i[-1] + min_y

def peak_year(name_list, min_y = min_data_year):
    """Returns the year in a list of counts of a name where the count was the highest
    """
    filtered = [x for x in name_list if x is not None]
    if len(filtered) > 0:
        max_value = max(filtered)
        max_index = name_list.index(max_value) + min_y
        return max_index, int(max_value)
    else:
        return -1, 0

def valley_year(name_list, min_y = min_data_year):
    """Returns the year in a list of counts of a name where the count was the lowest
    """
    filtered = [x for x in name_list if x is not None]
    if len(filtered) > 0:
        min_value = min(filtered)
        min_index = name_list.index(min_value) + min_y
        return min_index, int(min_value)
    else:
        return -1, 0

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
    year_list = get_year_list_one(sex, year)
    year_as_list = year_list['Name'].to_list()
    if name in year_as_list:
        return year_as_list.index(name) + 1
    else:
        return -1

def get_count(name, sex, year):
    """Returns the count of a name with its associated sex in the given year. 
    0 means it was not in the dataset for that year
    """
    year_data = get_year_list_one(sex, year)
    year_data = year_data[year_data["Name"] == name]
    return year_data["Count"].sum()

def get_name_from_rank(rank, sex, year):
    """Returns the name at the given rank for the associated sex, along with its count"""
    year_list = get_year_list_one(sex, year)
    name_row = year_list.iloc[rank - 1]
    return name_row["Name"], name_row["Count"]
    
def name_ranks_years(name, sex, min_y = min_data_year, max_y = max_data_year):
    ranks = []
    for i in range(min_y, max_y):
        r = get_rank(name, sex, i)
        r = r if r >= 0 else None
        ranks.append(r)
    return ranks
    
def make_graph(title, x, y, year, label, color = default_color, show = True, x_label = 'count', y_label = 'year'):
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

def top_names(sex, top_names = 10, min_y = min_data_year, max_y = max_data_year):
    """Sums up the year counts for each year in the range and sorts the names from most to least popular
    Set top_names to -1 to return all names
    """
    year_list = get_year_list(sex)
    df_all = pd.DataFrame(columns = year_list[0].columns)
    for i in range(min_y, max_y):
        df_all = pd.concat([df_all, year_list[i - min_data_year]])
    df_all['Count'] = df_all.groupby(['Name'])['Count'].transform('sum')
    df_all = df_all.drop_duplicates(keep = 'first')
    df_all = df_all.sort_values('Count', ascending = False)
    df_all = df_all.reset_index(drop = True)
    if top_names == -1:
        return df_all
    else:
        return df_all.iloc[0:top_names]

def narrow_top_popularity(top):
    """To be used with the dataframe returned by top_names method to find names in a certain section of the popularity
    """
    print("The popularity options are: extremely popular (1), very popular (2), common (3), uncommon(4), \n\trare (5), ultra rare (6), ignore (7)")
    choice = int(input("Enter the number for the popularity: "))
    popularities = {'0' : 0, 'e' : 0.01, 'v' : 0.025, 'c' : 0.075, 'u' : 0.2, 'r' : 0.5, 'b' : 1,}
    top = top[top['Count'] > 0]
    top = top.sort_values(by = 'Count', ascending = False)
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

def names_with_string(string, sex, min_y = min_data_year, max_y = max_data_year, function = 'start'):
    """Give a string to start, end, or be contained in a name and get a dataframe of the total sum of that name
    and the number of years it appeared in"""
    year_list = get_year_list(sex)
    data_names = pd.DataFrame(columns=['Name', 'Sex', 'Count', 'Years'])
    for i in range(min_y, max_y):
        current_df = year_list[i - min_data_year].copy()
        if function == 'start':
            current_df = current_df[current_df['Name'].str.startswith(string)]
        elif function == 'end':
            current_df = current_df[current_df['Name'].str.endswith(string)]
        else:
            print("function not supported")
        current_df['Years'] = 1
        data_names = pd.concat([data_names, current_df], axis=0)
    final_names = data_names.groupby('Name', as_index=False).agg({'Count' : 'sum', 'Years' : 'count'}).reset_index()
    return final_names.drop('index', axis = 1)

def biggest_rank_jump(name, sex, min_rank = 1000, min_jump = 100, min_y = min_data_year, max_y = max_data_year):
    """Finds the largest rank jumps of a name as long as start or end rank is >= min rank and number of ranks
    moved is >= min_jump"""
    year_list = get_year_list(sex)
    ranks = []
    for i in range(1880, 2025):
        ranks.append(get_rank(name, sex, i))
    jumps = pd.DataFrame(columns = ["Name", "Ranks", "y1", "y2", "r1", "r2"])
    for i in range(1, len(ranks)):
        num_ranks = abs(ranks[i] - ranks[i - 1])
        r1 = ranks[i - 1]
        r2 = ranks[i]
        if (r1 <= min_rank or r2 <= min_rank) and (r1 != -1 and r2 != -1) and num_ranks >= min_jump:
            jumps.loc[len(jumps)] = (name, num_ranks, i - 1 + min_data_year, i + min_data_year, r1, r2)
    return jumps

def unique_names_one(sex, min_y = max_data_year, max_y = max_data_year):
    """Returns all of the names and number of names that only appear for the given sex and do not appear in both lists"""
    year_list = get_year_list(sex)
    unique = set()
    for i in range(min_y,max_y):
        y = year_list[i - min_data_year]
        for n in y['Name']:
            unique.add(n)
    num_names = len(unique)
    return unique, num_names

def unique_names_total_solo(min_y = max_data_year, max_y = max_data_year):
    """Returns all of the unique names in the data set when unique male and female names have 
    not already been found with unique_name_one"""
    f_list, _ = unique_names_one("f", min_y, max_y)
    m_list, _ = unique_names_one("m", min_y, max_y)
    total = f_list.union(m_list)
    return total, len(total)

def unique_names_total(f_list, m_list):
    """Returns all of the unique names in the data set when unique male and female names have 
    already been found with unique_name_one"""
    total = f_list.union(m_list)
    return total, len(total)

def unisex_names_solo(min_y = max_data_year, max_y = max_data_year):
    """Returns all names appearing in both male and female lists when unique male and female names have
    not already been found with unique_name_one"""
    f_list, _ = unique_names_one("f", min_y, max_y)
    m_list, _ = unique_names_one("m", min_y, max_y)
    unisex = f_list.intersection(m_list)
    return unisex, len(unisex)

def unisex_names(f_list, m_list):
    """Returns all names appearing in both male and female lists when unique male and female names have
    already been found with unique_name_one"""
    unisex = f_list.intersection(m_list)
    return unisex, len(unisex)

def sum_name_list(names, sex, min_y = min_data_year, max_y = max_data_year):
    """Takes a list of just names and a sex (b for both) and creates a dataframe of the name, sex,
    and total count over the range of years"""
    result = pd.DataFrame(columns = ["Name", "Sex", "Count"])
    if sex != "b":
        for n in names:
            s = name_counts_simple(n, sex, min_y, max_y)
            result.loc[len(result)] = (n, sex, s)
    elif sex == "b":
        for n in names:
            sm = name_counts_simple(n, "m", min_y, max_y)
            result.loc[len(result)] = (n, sex, sm)
            sf = name_counts_simple(n, "f", min_y, max_y)
            result.loc[len(result)] = (n, sex, sf)
    return result