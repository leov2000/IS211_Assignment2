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
    print(type(csvContents), 'CSVCONTENTS')
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

    Returns | Prints:
        the .csv data or prints an error if an Exception occurs.
    """
    try:
        csvData = urllib.urlopen(url)
        personData = processData(csvData.read())

        return personData
    except (ValueError):
        print('Something went wrong')
        
def displayPerson(id, personData):
    person = personData.get(id, 'No user found with that id')

    return displayStrFmtr(id, person) if isinstance(person, tuple) else person

def displayStrFmtr(id, person):
    (name, bday) = person
    result = f"Person #<{id}> is <{name}> with a birthday of <{dateStrFmtr(bday)}>"

    return result 

def dateStrFmtr(dateObj):
    return dateObj.strftime('%Y-%m-%d')

def parseDate(dateStr):
    return datetime.strptime(dateStr, '%d/%m/%Y')

def strDateParseChecker(dateStr, personId, line):
    try:
        return parseDate(dateStr)
    except ValueError:
        logging.error(f'Error processing line #<{line}>, for ID #<{personId}>')
        return None

def safeIntChecker(intStr):
    try: 
        num = int(intStr)
        return (True, num)
    except ValueError:
        return (False, None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(message)s')
    logging.getLogger('assignment2')

    if(args.url):
        personData = downloadData(args.url)
        CLI = True

        while CLI:
            keyed = input('Please Enter a Integer UserId\n')
            (isInt, castNum) = safeIntChecker(keyed)

            if isInt and castNum > 0:
                personString = displayPerson(keyed, personData)
                print(personString)

            elif isInt and castNum <= 0:
                CLI = False

if __name__ == '__main__':
    main()
    