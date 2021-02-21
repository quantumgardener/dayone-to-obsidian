# dayone-to-obsidian
Convert a DayOne JSON export into individual entries for Obsidian. Each entry is created as a separate page.

## Requirements
* Python 3
* pytk (pip install pytk

## Optional requirements
* Obsidian [Icons Plugin](https://github.com/visini/obsidian-icons-plugin) to display calendar marker at start of page heading

## Setup
1. Export your journal from DayOne in JSON format **DO NOT do this in your current vault. Create a new vault for the purpose of testing**
2. Expand that zip file
3. Adjust the *root* variable to point to the location where your zip file was expanded and Journal.json exists. You should also have a photos folder here if there were photos in your journal
4. If you **not** are using the [Icons Plugin](https://github.com/visini/obsidian-icons-plugin) to display calendar marker at start of page heading set *icons = False*
5. Run the script
6. Check results in Obsidian
7. If happy, move all the *journal* and *photos* folders to whatever vault you want them in.

## Features
* Processes all entries, including any blank ones you may have.
* Entries organised by year/month/day
* If multiple entries on a day, each additional entry is treated seperately
* Adds YAML metadata for whatever exists
   * minimum date and timezone
   * Location as text
   * GPS coordinates
   * Tags
   * Starred flag
* Every entry has the date inserted in the text for easier reading (with a calendar icon to help you quickly distinguish from other entries in your vault)
* If location is specified, it is given under the date, linked to Google Search
* Tags added at the bottom, each as a subtag of journal to distinguish from other tags in your vault

## A note on photos
For whatever reason, photo identifiers in the text of an entry within the JSON file are not saved with that identifier. Instead they are named with the MD5 digest of the file. We fix this by renaming all files to match the identifier in the text entry. This rename only occurs if required.

