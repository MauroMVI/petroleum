import requests
import zipfile
import io
import csv
import shutil
from datetime import datetime



def download_zip(url, filename):
    """
    This function downloads the zipfile from the SIH url, and extracts the 
    file of interest on the SAME directory where the code is.
    Using the 'with' statement closes the file after using it, saving memory.
    """

    # Using requests gets the zip file from the url, I do not really know what
    # stream=True do.
    with requests.get(url, stream=True) as r:
        # Prints code. If 200, it is ok.
        print(f"Status code: {r.status_code}")
        # Converts content of req. into bytes.
        with io.BytesIO(r.content) as bf:
            # Converts bytes to ZipFile obj. don't really know if previous step
            # is required.
            with zipfile.ZipFile(bf) as zf:
                # Extracts file to working directory
                zf.extract(filename)

def get_strdate():
    """
    This function gets the today's date and creates a str obj. to manipulate.
    Then, it removes all '-' and returns it to use on other functions.
    """

    #Gets only date part of today's date and creates a str.
    date = str(datetime.now().date())
    # Removes '-' from string.
    date = date.replace('-','')
    # Returns desired string.
    return date

def data_paths(date, filename):
    """
    This function prepares the paths and new name of the file, 
    with the format I desire. In this case, date_filename.csv. 
    Date comes from get_strdate() function.
    """
    # Standard name of the file, the SIH always put it like this.
    path_src = filename
    # Path destination, this part also sets new name of file.
    path_destination = '/home/mmvi/mexico/petroleum'
    path_destination += f'/data/{date}_POZOSCOMPILADO.csv'
    # Returns path_src: original path of file, as it's in the same working 
    # directory it does not needs the full path.
    # Returns path_destination: Full path to data directory, where I want the
    # files to be stored. Sets the new name for move_data() function.
    return path_src, path_destination


def move_data(path_src, path_destination):
    """
    This function moves the file to the path I want, and renames it.
    path_src and path_destination come from data_paths function.
    """
    # This function will rename the file as well.
    shutil.move(path_src, path_destination)

def prep_data_for_pd(path_destination, encoding="ISO-8859-1"):
    """
    This function gets the number of rows to skip to reach the column headers of
    the data and upper case the headers. Original csv file contains useless info
    for pandas and difficults the creation of a DataFrame. For this csv,
    encoding="ISO-8859-1" is default as the first rows 
    """
    # Assigns the full path of csv file to filename variable.
    filename = f'{path_destination}'
    # Initializes variables that will help create DataFrame.
    row_index = 0
    skiprows = [0]
    # Opens file using with statement to lower memory usage.
    with open(filename, encoding=encoding) as f:
        #Assigns the iterator obj. to reader.
        reader = csv.reader(f)
        # Moves through each line of the reader variable.
        for line in reader:
            # This header will always be present on the csv as it shows historic
            # data.
            if 'Fecha' in line:
                # Assigns the list of header to header_lower.
                header_lower = line
                break
            else:
                # While we reach the headers, this get the indexes for each line
                # to be skipped in order to create the correct DataFrame.
                row_index += 1
                skiprows.append(row_index)
                continue
        # Makes all headers to uppercase for aesthetics purposes.
        header_rows = [element.upper() for element in header_lower]
    # Returns the headers of DataFrame in uppercase and number of rows to skip.
    return header_rows, skiprows

def download_data(url, filename):
    """
    This function calls all the other functions needed to download the data,
    save it at desired location and rename the file.
    """
    date = get_strdate()
    path_src, path_destination = data_paths(date, filename)
    download_zip(url, filename)
    shutil.move(path_src, path_destination)

url = 'https://sih.hidrocarburos.gob.mx/downloads/PRODUCCION_POZOS.zip'
filename = 'POZOS_COMPILADO.csv'
download_data(url, filename)
# header_rows, skiprows = prep_data_for_pd(path_destination)
# print(header_rows)
# print(skiprows)