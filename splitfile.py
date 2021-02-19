import datetime
import dateutil.parser
import json
import pytz
import re

fn = "D:\OneDrive\Documents\dayone\Journal.json"
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

        # Finish YAML
        newEntry.append( '---\n' )

        # Add body text if it exists, after some tidying upp
        try:
            newText = entry['text'].replace("\\", "")
            newText = newText.replace( "\u2028", "\n")
            newText = newText.replace( "\u1C6A", "\n\n")
            #newText = newText.replace( "![]dayone-moment://", "photos/")
            # Replace all photos
            #newText = re.search("(\!\[\]\(dayone-moment:\/\/)([A-F0-9]+)(\))", newText)
            newText = re.sub("(\!\[\]\(dayone-moment:\/\/)([A-F0-9]+)(\))", r'[[\2.jpeg]]', newText)
            newEntry.append( newText )
        except KeyError:
            pass

        # Let's add some tags at the bottom to finish up
        tags = ''
        if 'tags' in entry:
            for t in entry['tags']:
                tags = "%s #%s" % (tags, t.replace(' ', '-'))

        if entry['starred']:
            tags = "%s #starred" % tags 

        if tags != '':
            newEntry.append( "\n\n%s" % tags )


        fnNew = "D:\OneDrive\Documents\dayone\%s.md" % createDate.strftime( '%Y-%m-%d')
        with open(fnNew, 'w', encoding='utf-8') as f:
         for line in newEntry:
            f.write(line)

