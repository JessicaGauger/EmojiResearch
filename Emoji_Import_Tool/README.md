# Emoji Import Tool

This tool was built for a practicum in order to import and store basic emoji information. 
It contains functionality for:

* Creating a MySql database
* Scraping emoji data through the use of Emojipedia
* Storing emoji names, unicode, and a single platform image url 

## Database Setup

This project relies on MySQL as the database server. To begin, use the script in the Database 
Setup folder. This will drop the database if it exists and re-create it with new tables. 

```
> .\Database Setup\EmojiDatabaseSetup.sql
```

Additional tables are included in this script which are used in other parts of the practicum
project. 

### Local Config

After the database is set, create a local configuration file with credential details called
local_config.py with the following dictionary (and supply credentials)

```
db_config = {
   'user': '',
   'host': 'localhost',
   'password': '',
   'database': 'covid_emoji_proj'
}
```

## To Run
After the database and local_config are created, the tool is ready to be run. 
There are two methods available to populate data:
* Method 1: Persist By Scraping With Unicode Versions
  - This method relies on keeping the emoji versions up to date in the emoji_data file.
  Those versions are used to scrape emoji per unicode release.  
    * ```Update ./emoji_data.py```
    * ```Run ./method1.py```
* Method 2: Persist By Scraping With Emojipedia.all()
  - This method relies on certain pages on the emojipedia.org website to be up. If those pages
  are down, this method will not work.
    * ```Run ./method2.py```

## SQL Output
While the python scripts use MySql connectors to persist the data, each method also outputs
the sql used into the Output folder. This allows for quickly populating the tables without
re-running the python. 
```
Method 1 Output: ./Output/method1_insert_emoji.sql
Method 2 Output: ./Output/method2_insert_emoji.sql
```
