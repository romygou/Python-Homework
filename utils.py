import urllib
import csv

def read_data(path):
    """
    Read downloaded data from a .csv file, and return a list of tuples. Each tuple represents a link between states.
    Args:
        path: string (Path of the file in which data is present)
    Returns:
        data: list of tuples which represents the data
    """
    with open(path, "r") as f:
        reader = csv.reader(f)
        return [(row[0], row[1]) for row in list(reader)]

def describe(data, n):
    """
    Print a string describing the nth element of the loaded dataset, with capitalization.
    Args:
        data: list of tuples
        n: integer
    Returns:
        None (The function prints the string and does not return anything)
    """
    capitalize_data = [(i[0].capitalize(), i[1].capitalize()) for i in data] #capitalize each word in the tuple
    txt = "Element {nrow} of the Hamilton data set is {data1}. This means that {data2} mentions {data3} in a song."
    print(txt.format(nrow = n, data1 = data[n], data2 = capitalize_data[n][0], data3 = capitalize_data[n][1]))


def data_to_dictionary(data):
    """
    Convert data (represented as a list of 2-tuples) into a dictionary keyed by first entry of the tuple. The corresponding value
    is the list of all second entries corresponding to the first entry, with repeats.
    Args:
        data: list of tuples
    Returns:
        dictionary: which is created in this function
    """
    dictionary = {} #initialize dictionary
    for i in range(len(data)): #iterate through data
        if data[i][0] in dictionary:
            dictionary[data[i][0]].append(data[i][1]) #if mentioner is already in dictionary, append mentioned to the end
        else:
            dictionary[data[i][0]] = [data[i][1]] #if mentioner is not in dictionary, create a list containing mentioned
    return dictionary
    