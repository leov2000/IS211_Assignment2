import argparse
import logging
import urllib.request as urllib
from datetime import datetime
import csv

def processData(csvContents):
    csvPayLoad = csv.reader(csvContents.decode('utf-8').splitlines())
    csvResults = [row for idx, row in enumerate(csvPayLoad) if idx > 0]
    personDict = {
        pid: (name, parseDate(bday)) for idx, (pid,name,bday) in enumerate(csvResults) 
        if strDateParseChecker(bday, pid, idx + 2)
    }

    return personDict

def downloadData(url):
    csvData = urllib.urlopen(url)
    personData = processData(csvData.read())

    return personData
        
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
    