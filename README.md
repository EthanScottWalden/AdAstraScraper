# AdAstra Scraper

This program was created from **Feburary to April 2025** for the Empty Room Junior Design project. 

This is a Python web scraper for CBU IT's classroom schedule page. It uses Selenium to navigate and interact with complex, dynamic web pages on the site and parses information about the times classrooms are available on particular days with Beautiful Soup 4. The program outputs the collected information into a JSON file for easy input into the mobile app's Firebase storage.

To see the Empty Room mobile app and the commit history of the AdAstra Scraper, see the latest version of Empty Room here: https://github.com/NoahTheLee/EGR302_Empty_Room/tree/testing

# How to run

**This program has required arguments.** To run this, execute this in the console:

`python adastra_scraper.py <username> <password>`

where <username> and <password> are the credientials you want to try to use to log in to ad astra.

# Dependencies

The following packages are required: **beautifulsoup4, selenium, portion**
