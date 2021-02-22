# dayone-to-obsidian
Convert a [Day One](https://dayoneapp.com/) JSON export into individual entries for [Obsidian](https://obsidian.md). Each entry is created as a separate page. It was created for my own use and is unlikely to be modified now that it has served it's purpose.

## Requirements
* Python 3
* pytk (pip install pytk

## Optional requirements
* Obsidian [Icons Plugin](https://github.com/visini/obsidian-icons-plugin) to display calendar marker at start of page heading

## Setup

**DO NOT do this in your current vault. Create a new vault for the purpose of testing. You are responsible for ensuring against data loss**
**This script deletes folders if run a second time**
**This script renames files**
1. Export your journal from [Day One in JSON format](https://help.dayoneapp.com/en/articles/440668-exporting-entries) 
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
   * Tags (show in metadata dropdown)
   * Starred flag
* Every entry has the date inserted in the text for easier reading (with a calendar icon to help you quickly distinguish from other entries in your vault)
* If location is specified, it is given under the date, linked to Google Search
* Tags can be prefixed (default = journal) to show as subtags in Obsidian separate from other note tags
* Optional via uncommenting code. Tags added at the bottom
