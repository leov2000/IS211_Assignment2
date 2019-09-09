import argparse
import logging
import urllib.request as urllib
from datetime import datetime
import csv

def processData(csvContents):
    """
    A primary function that received the fetched csv data
    parses, formats and sanitizes according to spec.

    Parameters:
        csvContents(bytes): csv data fetched

    Returns:
      A dictionary of people with id's as the keys and a tuple
      with the person info as its value. 
    """

    csvPayLoad = csv.reader(csvContents.decode('utf-8').splitlines())
    csvResults = [row for idx, row in enumerate(csvPayLoad) if idx > 0]
    personDict = {
        pid: (name, parseDate(bday)) for idx, (pid,name,bday) in enumerate(csvResults) 
        if strDateParseChecker(bday, pid, idx + 2)
    }

    return personDict

def downloadData(url):
    """
    A primary function that fetches given the #url param
    or prints an error. 

    Parameters:
        url(string): uri string

    Returns:
        the .csv data.
    """

    csvData = urllib.urlopen(url)
    personData = processData(csvData.read())

    return personData
        
def displayPerson(id, personData):
    """
    A primary function used to get values from the #personData
    dict given an id. A fallback value is provided if the id
    isn't present in the dictionary.

    Parameters:
        id(int): int representing the person id.
        personData(dict[int, tuple[str, <date-obj>]]): the dictionary which
            houses the state of all people.

    Returns:
        A formatted string via the displayStrFmtr call or the fallback string.

    """

    person = personData.get(id, 'No user found with that id')

    return displayStrFmtr(id, person) if isinstance(person, tuple) else person

def displayStrFmtr(id, person):
    """
    A utilty function that's used to display the 
    name and bday of a user given an id via the
    CLI. 

    Parameters:
        id(int):                        int representing the person id.
        person(tuple[str, <date-obj>]): tuple that contains person info.

    Returns:
        A formatted string that includes the id and person info.
    """

    (name, bday) = person
    result = f"Person #<{id}> is <{name}> with a birthday of <{dateStrFmtr(bday)}>"

    return result 

def dateStrFmtr(dateObj):
    """
    A utility function that takes the #dateObj param
    and returns a formatted string of 'YYYY-MM-DD'

    Parameters:
        dateObj(<date-obj>): A date object.
    
    Returns:
        A formatted string.
    """

    return dateObj.strftime('%Y-%m-%d')

def parseDate(dateStr):
    """
    A utility function that parses the #dateStr param according to 
    format

    Parameters:
        dateStr(str): A string in a date format.
    
    Returns:
        A date object.
    """

    return datetime.strptime(dateStr, '%d/%m/%Y')

def strDateParseChecker(dateStr, personId, line):
    """
    An intermediary function that checks the #dateStr 
    param can be parsed, if parsed it returns a dateobj
    if it fails, log the #id and #line where the error
    occurred

    Parameters:
        dateStr(str) : A string in a date format. 
        personId(int): The person id int.
        line(int)    : int line where the person can be found.

    Returns | Logs:
        A date object only if its parsed correctly and None if 
        it isnt. If it fails to parse correctly an error is
        appended to the errors.log      
    """

    try:
        return parseDate(dateStr)
    except ValueError:
        logging.error(f'Error processing line #<{line}>, for ID #<{personId}>')
        return None

def safeIntChecker(intStr):
    """
    A utility function that checks if the string representation of an int inputted
    when the CLI starts can be successfuly cast as an int.
    
    Parameters:
        intStr(str): A string representing an Int.

    Returns:
        A tuple with a boolean as the first item and a value if its successfuly cast or
        None if it isnt.

    """
    
    try: 
        num = int(intStr)
        return (True, num)
    except ValueError:
        return (False, None)

def main():
    """
    The main function of this application.

    Parameters:
        url(str): A string representing a url
    
    Returns:
        No values are returned as a sideffect the CLI is bootstrapped using the url
        parameter. You're prompted to search for a user given number. if the string
        is > 0 and not one of the users assocaited with a date error you'll receive
        the users info if its <= 0 the app will exit.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(message)s')
    logging.getLogger('assignment2')

    if(args.url):
        try:
            personData = downloadData(args.url)
        except (ValueError, urllib.HTTPError):
            print(f'Something went wrong, you entered in <{args.url}>, please check your url param for errors')
            return SystemExit

        CLI = personData != None

        while CLI:
            keyed = input('Please Enter an ID For Lookup\n')
            (isInt, castNum) = safeIntChecker(keyed)

            if isInt and castNum > 0:
                personString = displayPerson(keyed, personData)
                print(personString)

            elif isInt and castNum <= 0:
                CLI = False

if __name__ == '__main__':
    main()
    