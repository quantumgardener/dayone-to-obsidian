import datetime
import dateutil.parser
import json
import pytz    # pip install pytz
import re
import os
import sys
import shutil
import time

# Set this as the location where your Journal.json file is located
root = r"D:\OneDrive\Documents\dayone" 
journalFolder = os.path.join(root, "journal") #name of folder where journal entries will end up
fn = os.path.join( root, "Journal.json" )

# Clean out existing journal folder, otherwise each run creates new files
if os.path.isdir(journalFolder):
    print ("Deleting existing folder: %s" % journalFolder)
    shutil.rmtree(journalFolder)

time.sleep(2)  # Give time for folder deletion to complete. Only a problem if you have the folder open when trying to run the script
if not os.path.isdir(journalFolder):
    print( "Creating journal folder: %s" % journalFolder)
    os.mkdir(journalFolder)

print( "Begin processing entries")
count = 0
with open(fn, encoding='utf-8') as json_file:
    data = json.load(json_file)
    for entry in data['entries']:
        newEntry = []

        # Start YAML
        newEntry.append( '---\n' )

        # Add raw create datetime adjusted for timezone and identify timezone
        createDate = dateutil.parser.isoparse(entry['creationDate'])
        newEntry.append( 'Creation Date: %s\n' % createDate.astimezone(pytz.timezone(entry['timeZone'])) )
        newEntry.append( 'Timezone: %s\n' % entry['timeZone'] ) 

        # Add location
        location = ''
        for locale in ['placeName', 'localityName', 'administrativeArea', 'country']:
            try:
                location = "%s, %s" % (location, entry['location'][locale] )
            except KeyError:
                pass
        newEntry.append( 'Location: %s\n' % location[2:]) # Remove leading ", "

        # Add GPS, not all entries have this
        try:
            newEntry.append( 'GPS: %s, %s\n' % ( entry['location']['latitude'], entry['location']['longitude'] ) )
        except KeyError:
            pass

        # Add any tags to YAML. They are also added separately at end of entry to tie in as Obisidan tags
        # Tags in YAML are not recognised by Obsidian
        if 'tags' in entry:
            newEntry.append( "Tags: %s\n" % ", ".join(entry['tags']))

        if entry['starred']:
            newEntry.append( "Starred: True\n" )


        # Finish YAML
        newEntry.append( '---\n' )

        # Add a page header
        if sys.platform == "win32":
            newEntry.append( '## %s\n' % createDate.astimezone(pytz.timezone(entry['timeZone'])).strftime( "%A, %#d %B %Y at %#I:%M %p"))
        else:
            newEntry.append( '## %s\n' % createDate.strftime( "%A, %-d %B %Y"))  #untested

        # Add body text if it exists (can have the odd blank entry), after some tidying up
        try:
            newText = entry['text'].replace("\\", "")
            newText = newText.replace( "\u2028", "\n")
            newText = newText.replace( "\u1C6A", "\n\n")

            if 'photos' in entry:
                # Correct photo links. First we need to rename them. The filename is the md5 code, not the identifier
                # subsequently used in the text. Then we can amend the text to match. Will only to rename on first run
                # through as then, they are all renamed.
                # Assuming all jpeg extensions.

                for p in entry['photos']:
                    pfn = os.path.join( root, 'photos', '%s.jpeg' % p['md5'] )
                    if os.path.isfile( pfn ):
                        newfn = os.path.join( root, 'photos', '%s.jpeg' % p['identifier'] )
                        print ( 'Renaming %s to %s' % (pfn, newfn ))
                        os.rename( pfn, newfn )

                # Now to replace the text to point to the file in obsidian
                newText = re.sub(r"(\!\[\]\(dayone-moment:\/\/)([A-F0-9]+)(\))", r'![[\2.jpeg]]', newText)

            newEntry.append( newText )
        except KeyError:
            pass

        # Let's add some tags at the bottom to finish up
        tags = '#journal/entry\n'
        if 'tags' in entry:
            for t in entry['tags']:
                tags = "%s#journal/%s\n" % (tags, t.replace(' ', '-'))

        if entry['starred']:
            tags = "%s#journal/starred\n" % tags 

        newEntry.append( "\n\n%s" % tags )

        # Save entries organised by year, year-month, year-month-day.md
        yearDir = os.path.join( journalFolder, str(createDate.year) )
        monthDir = os.path.join( yearDir, createDate.strftime( '%Y-%m'))

        if not os.path.isdir(yearDir):
            os.mkdir(yearDir)
        
        if not os.path.isdir(monthDir):
            os.mkdir(monthDir)
        
        # Target filename to save to. Will be modified if already exists
        fnNew = os.path.join( monthDir, "%s.md" % createDate.strftime( '%Y-%m-%d'))
        
        # Here is where we handle multiple entries on the same day. Each goes to it's own file
        if os.path.isfile( fnNew):
            # File exists, need to find the next in sequence and append alpha character marker
            index = 97 #ASCII a
            fnNew = os.path.join( monthDir, "%s%s.md" % (createDate.strftime( '%Y-%m-%d'), chr(index)))
            while os.path.isfile(fnNew):
                index += 1
                fnNew = os.path.join( monthDir, "%s%s.md" % (createDate.strftime( '%Y-%m-%d'), chr(index)))


        with open(fnNew, 'w', encoding='utf-8') as f:
         for line in newEntry:
            f.write(line)

        count += 1

print ("Complete: %d entries processed." % count)

