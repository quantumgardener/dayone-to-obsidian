from itertools import groupby, chain
import datetime
from dateutil import parser
import codecs

filename='journal.md'



# From https://stackoverflow.com/questions/35773600/how-to-split-file-into-chunks-by-string-delimiter-in-python
def getEntries(filename):
    with open(filename,'r', encoding="utf-8") as f:
        grps = groupby(f, key=lambda x: x.startswith("\tDate:")) # Used Date: as indicator of a new file
        for k, v in grps:
            if k:
                yield chain([next(v)], (next(grps)[1]))  # all lines up to next #TYPE

i = 1

for entry in getEntries(filename):
    # control variables
    endYAML = 2 # Point at which we insert the YAML end ---. Start at 2 which is after the first --- is inserted and the date which we always know we have. Other metadata will extend this
    reflections = False

    e = list(entry)
    e[0] = e[0].replace("\tDate:","Date: ") # Tidy up the date line for YAML
    dateWritten = e[0][6:]
    if e[1].find("\tLocation:\t") >= 0:
        e[1] = e[1].replace("\tLocation:\t","Location: ")
        endYAML += 1
    i+=1
    if i>300:
        break

    # Modify any special text lines
    b = [x for x, value in enumerate(e) if value[:4] == "Refl" ]
    if not len(b) == 0:
        print (e[b[0]])
        e[b[0]] = "\n*%s*\n" % e[b[0]][:-1]
        reflections = True


    # set up for output - wrap YAML then get filename from date
    e.insert(0, "---\n")
    e.insert(endYAML, "---\n")
    if reflections:
        e.append( "#reflections ")
    try:
        fn = parser.parse(dateWritten).date()
    except UnknownTimezoneWarning:
        pass
    
    with open('%s.md' % fn, 'w', encoding='utf-8') as f:
        for line in e:
            f.write(line)
            