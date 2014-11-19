__author__ = 'Sterling Windmill'

import fileinput
import re
import calendar

# list of fields to write out to csv
fieldlist = ['date',
             'time',
             'tclient',
             'tqueue',
             'tconn',
             'tsession',
             'rcode',
             'event',
             'state']

# regex power!
# note that these field names don't map directly to output
# we're manipulating some of the data before writing it to csv
pattern = re.compile(r'(?P<srcip>[\d.]+):\d+ \['
                      '(?P<day>\d+)\/'
                      '(?P<month>[A-Z][a-z]{2})\/'
                      '(?P<year>\d+):'
                      '(?P<hour>\d+):'
                      '(?P<minute>\d+):'
                      '(?P<second>\d+).*?\].*?'
                      '(?P<tclient>\d+|-1)\/'
                      '(?P<tqueue>\d+|-1)\/'
                      '(?P<tconn>\d+|-1)\/'
                      '(?P<tserver>\d+|-1)\/'
                      '(?P<tsession>\d+|-1) '
                      '(?P<rcode>\d+|-1).*?'
                      '(?P<event>[CSPRIcs-])'
                      '(?P<state>[RQCHDLT-])'
                      '(?P<cookie1>[NIDVEO-])'
                      '(?P<cookie2>[NIUPRD-])')



# print header row
print ",".join(fieldlist)

# loop through input (stdin)
for line in fileinput.input():

    # perform regex
    match = re.search(pattern, line)

    # check for regex match
    if match:

        # store mapped groups as a Python dictionary
        data = match.groupdict()

        # manipulating raw data to format month as a number instead of three letter abbreviation
        data['month'] = str(list(calendar.month_abbr).index(data['month']))

        # building date from individual components
        data['date'] = data['month'] + '/' + data['day'] + '/' + data['year']

        # building time from individual components
        data['time'] = data['hour'] + ":" + data['minute'] + ":" + data['second']

        # create list containing real data
        datalist = [data[item] for item in fieldlist]

        print ",".join(datalist)
