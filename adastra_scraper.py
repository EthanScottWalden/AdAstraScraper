# This program has required arguments. To run this, type this in the console:
# python adastra_scraper.py <username> <password>
# where <username> and <password> are the credientials you want to try to use to log in to ad astra.

import json
import argparse
import math
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from time import sleep
import portion as P

# classes that will be ignored when scraping and removed from existing class info if they are present
blacklist = {
    "ABPK B8 - Virtual Reality Studio",
    "AMOD Lancer Team Room",
    "AQUA POOL",
    "ARPT OFFC - Instructor Office",
    "BBSB 100 - Lobby",
    "BBSB 101 - Elevator",
    "BBSB 102 - Hallway",
    "BBSB 103 - Kitchenette",
    "BBSB 105 - Women's Softball Restroom",
    "BBSB 105S - Women's Shower",
    "BBSB 106 - Mud Room",
    "BBSB 107 - Physical Therapy",
    "BBSB 108 - Laundry Room",
    "BBSB 109 - Rolling Storage",
    "BBSB 110 - Kitchenette",
    "BBSB 111 - Baseball Locker Room",
    "BBSB 112 - Baseball Restroom",
    "BBSB 112S - Shower",
    "BBSB 113 - Baseball Foyer",
    "BBSB 114 - Physical Therapy",
    "BBSB 115 - Concessions",
    "BBSB 116 - Electrical Room",
    "BBSB 117 - Fire",
    "BBSB 118 - Stair",
    "BBSB 200 - Lobby",
    "BBSB 201 - Elevator",
    "BBSB 202 - All Gender Restroom",
    "BBSB 203 - Work Room",
    "BBSB 204 - Softball Coach Female Locker Room",
    "BBSB 204S - Softball Coach Female Shower",
    "BBSB 205 - Softball Coach Male Locker Room",
    "BBSB 205R - Softball Coach Male Restroom",
    "BBSB 205S - Softball Coach Male Shower",
    "BBSB 206 - Softball Balcony",
    "BBSB 207 - Softball Assistant Coach Office 4",
    "BBSB 208 - Softball Assistant Coach Office 3",
    "BBSB 209 - Softball Head Coach",
    "BBSB 210 - Softball Assistant Coach Office 1",
    "BBSB 211 - Softball Assistant Coach Office 2",
    "BBSB 212A - Softball Open Office Area",
    "BBSB 212B - Softball Open Office Area",
    "BBSB 213 - Kitchenette",
    "BBSB 214 - Conference Room",
    "BBSB 215 - Baseball Open Office Area",
    "BBSB 216 - Baseball Assistant Coach Office 4",
    "BBSB 217 - Baseball Assistant Coach Office 3",
    "BBSB 218 - Baseball Head Coach",
    "BBSB 219 - Baseball Balcony",
    "BBSB 220 - Stair",
    "BBSB 221 - Baseball Assistant Coach Office 2",
    "BBSB 222 - Baseball Assistant Coach Office 1",
    "BBSB 223 - Janitor",
    "BBSB 224 - Baseball Coach Locker Room",
    "BBSB 224R - Baseball Coach Restroom",
    "BBSB 224S - Baseball Coach Shower",
    "BBSB 225 - Work Room",
    "BBSB 226 - IT Room",
    "BBSB 227 - Baseball Hall",
    "BBSB 228 - Elevator Equipment",
    "BBSB 234 - Softball Hallway",
    "ECTR 1 - Visiting Team Locker Room",
    "ECTR 2 - Visiting Team Locker Room",
    "ECTR 3 - Visiting Team Locker Room",
    "ECTR 4 - Visiting Team Locker Room",
    "ECTR A207 - Meeting Room",
    "ECTR B204 - Meeting Room",
    "ECTR Bowl - Events Center Bowl",
    "ECTR C119 - Green Room",
    "ECTR Concessions East - Events Center Concessions East Area",
    "ECTR Concessions West - Events Center Concessions West Area",
    "ECTR Concourse - Events Center Concourse Level",
    "ECTR Foyer - Events Center Foyer",
    "ECTR Loading Dock - Events Center Loading Dock",
    "ECTR Plaza - Events Center Plaza",
    "GRND ADC Breezeway Booth 1 - ADC Breezeway 1",
    "GRND ADC Breezeway Booth 2 - ADC Breezeway 2",
    "GRND Atrium",
    "GRND Basin",
    "GRND Basketball Court",
    "GRND Basketball Court - Colony",
    "GRND Brisco's Lawn",
    "GRND BUSB Booth",
    "GRND Colony Lawn",
    "GRND Colony Pool",
    "GRND Cottage Lawn",
    "GRND CX Booth 1",
    "GRND CX Booth 2",
    "GRND CX Booth 3",
    "GRND Do not schedule",
    "GRND East S.E. Smith Courtyard",
    "GRND Ellis Great Commission Plaza",
    "GRND Flag Plaza",
    "GRND Fortuna Circle",
    "GRND Front Lawn",
    "GRND Global Village Lawn",
    "GRND Gym Lawn",
    "GRND Harden Square",
    "GRND Hawthorn House Lawn",
    "GRND HSCC Courtyard",
    "GRND HSCC Lawn",
    "GRND James East Lawn",
    "GRND Lancer Arms Lawn",
    "GRND Mission Hall Lawn",
    "GRND S.E. Smith Courtyard",
    "GRND Sand Volleyball Court",
    "GRND Simmons Lawn",
    "GRND Smith Lawn",
    "GRND Soccer Field",
    "GRND South Colony Lawn",
    "GRND Stamps Courtyard Lawn",
    "GRND Stamps Courtyard Seal",
    "GRND Stamps Seal Booths 1",
    "GRND Stamps Seal Booths 2",
    "GRND Stamps Seal Booths 3",
    "GRND Stamps Seal Booths 4",
    "GRND Stamps Step Booths 1",
    "GRND Stamps Step Booths 2",
    "GRND Stamps Step Booths 3",
    "GRND Tower Hall Lawn",
    "GRND Wallace Lawn",
    "GRND Wanda's Patio",
    "GRND Yeager Loading Zone",
    "HMUS 132 - Music Conference Room",
    "HSCC A006 - Conference Room",
    "HSCC G127 - Strength and Conditioning lab",
    "HSCC N271 - - Interior Design Studio",
    "HSCC P280 - Interior Design Studio",
    "INST OFFC - Instructor Office",
    "JAME 048 - Computer Lab-Journalism",
    "JAME 052 - Educational Effectiveness",
    "JAME 060 - Newsroom for Lancer Media Group",
    "JAME 107A - Staples Room",
    "JAME 123A - Behavioral Science Seminar Room",
    "JAME 125 - Beh Science Conf Room",
    "JAME 181 - Conference Room",
    "JAME 450 - Lab-Graphic Design",
    "JAME Garage 1 - Garage",
    "JAME Garage 2 - Garage",
    "JAME Garage 3 - Garage",
    "JAME Garage 4 - Garage",
    "JAME Garage 5 - Garage",
    "JAME Garage 6 - Garage",
    "JAME Garage 7 - Garage",
    "JAME Garage 8 - Garage",
    "JAME Garage 9 - Garage",
    "KINE 106 - Volleyball Team Room - Women",
    "KINE 121 - Volleyball Team Room - Men",
    "LAPC LAPC - Lancer Athletic Performance Center",
    "LAPN CL Lounge - Community Life Lounge",
    "LAPN Courtyard - Lancer Plaza Courtyard",
    "LARM 039 - Conference Room",
    "LOAC BASE - Sports-Field",
    "LOAC SOCC - Sports-Field",
    "LOAC SOCC PRAC - Sports-Field",
    "LOAC SOFT - Sports-Field",
    "MGCR LBY1 - First Floor Lobby",
    "NURS 002 - Nursing Conference Room",
    "NURS 105 - Nursing High Fidelity Skills Lab",
    "NURS 107 - Nursing High Fidelity Skills Lab",
    "NURS 108 - Nursing Skills Lab",
    "NURS 122 - Nursing Skills Lab",
    "NURS 132 - Nursing Flex Classroom",
    "NURS 134 - Lab-Nursing Skills",
    "NURS 139 - Nursing Debrief",
    "NURS 178 - Nursing Waiting Room Sim Clinic",
    "NURS 181 - Nursing Debrief/Conf/Exam Room",
    "NURS 211 - Nursing Skills Lab",
    "NURS 232 - Nursing Flex Classroom",
    "NURS 234 - Nursing Flex Classroom",
    "NURS 236 - Nursing Simulation Lab",
    "NURS 251 - Conference",
    "OTHR OFF 1 - Off Campus 1",
    "OTHR OFF 2 - Off Campus 2",
    "OTHR OFF 3 - Off Campus 3",
    "OTHR OTHR - Other - Non-CBU Campus Location",
    "PBLD 101 - Student Lounge",
    "PBLD 103 - Center for Entrepreneurship",
    "PBLD 105 - Park Building Terrace",
    "PBLD 114 - Innovators Hallway",
    "PBLD 128 - Grand Foyer",
    "PBLD 132 - Innovators Auditorium AB",
    "PBLD 132A - Innovators Auditorium A",
    "PBLD 132B - Innovators Auditorium B",
    "PBLD 209 - Capital Markets Trading Room",
    "PBLD 210 - Second Floor Lobby",
    "PBLD 212 - Business Conference Room",
    "PBLD Breezeway - PBLD Breezeway",
    "PBLD Hallway - Innovators Side B Hallway",
    "PBLD Lobby  - Innovators Side A Lobby",
    "PBLD Patio - Innovators Patio",
    "POIN Pool - Point Pool",
    "RCTR 105 - Racquetball Room 105",
    "RCTR 106 - Racquetball Room 106",
    "RCTR 107 - Racquetball Room 107",
    "RCTR Basketball Gymnasium",
    "RCTR CHER - Cheer Room",
    "RCTR GX1 - Group Exercise 1",
    "RCTR GX2 - Cycling Room",
    "RCTR GX3 - Group Exercise 3",
    "RCTR North Basketball Court",
    "RCTR Rooftop Field",
    "RCTR South Basketball Court",
    "SIMM LBY1 - First Floor Lobby",
    "SMIT LBY1 - First Floor Lobby",
    "TEGR 102 - Center for Innovation",
    "TEGR 317 - Dean's Planning Room",
    "TEGR 365 - Dean's Conference Room",
    "TEGR 369 - Conference Room",
    "TOWR LBY1 - First Floor Lobby",
    "TPLZ 125A - Storage",
    "TPLZ 125B - Storage",
    "TPLZ 140 - Office",
    "TPLZ 150 - Office",
    "UP300 300 - UP Shack",
    "VAND 110 - GYM",
    "VAND 220 - Classroom",
    "VAND Locker Room",
    "VAND Patio",
    "WALT 100 - Wallace Theater",
    "WALT Patio - Wallace Theatre - Patio",
    "YCTR ADC - Alumni Dining Commons",
    "YCTR B129 - Admissions Conference Room",
    "YCTR B140 - Admissions Conference Room 2",
    "YCTR B223 - Tillery Reading Clinic",
    "YCTR C210 - Provost Conference Room",
    "YCTR C222 - Executive Conference Room",
    "YCTR D113 - University Registrar Conference Room",
    "YCTR D223 - Copenbarger Dining Room",
    "YCTR D223A - LG Copenbarger Dining Room (Large Side)",
    "YCTR D223B - SM Copenbarger Dining Room (Small Side)"
}

num_classes = 423 # the number of classrooms we need to scrape, including the blacklisted classes. This is a constant because the number of rooms does not change

# attempts to login to ad astra with the given username and password. 
# returns boolean: True if successful, False if not
def login(username, password, driver):
    # navigate to the login page
    driver.get("https://www.aaiscloud.com/CABaptistU/logon.aspx?nosso=")

    # username field
    username_field = driver.find_element(By.ID, 'userNameField-inputEl')
    replace_content_of_element(driver, username_field, username)
    # username_field.send_keys(username)

    # password field
    password_field = driver.find_element(By.ID, 'textfield-1030-inputEl')
    replace_content_of_element(driver, password_field, password)
    # password_field.send_keys(password)

    # login button
    login_button = driver.find_element(By.ID, 'logonButton')

    # click on login button
    login_button.click()

    # wait until the home page is loaded
    WebDriverWait(driver, 3).until(EC.url_matches("https://www.aaiscloud.com/CABaptistU/Default.aspx"))
    # driver.get("https://www.aaiscloud.com/CABaptistU/Default.aspx")

    return driver.find_elements(By.ID, 'button-1022-btnInnerEl') != [] # returns True if we can access the calendars

# Navigates driver to Full_ Grid and does some setup to make our lives easier
def setup_calendar(driver):
    # navigate to the calendar page
    driver.get("https://www.aaiscloud.com/CABaptistU/Calendars/DailyGridCalendar.aspx")
    sleep(0.2) # waiting for the page to load

    # Once we get here, we need to switch to the correct calendar. 
    # By default it does not tell us anything about what times each class will be occupied. We need to switch to "Full_ Grid."

    # Clicks on the calendar selection dropdown arrow to show the options
    calendar_selection_dropdown_arrow = driver.find_element(By.ID, 'DailyGridCalendarForm_CalendarComboCtrl-trigger-picker')
    calendar_selection_dropdown_arrow.click()

    # Waits for the dropdown to open
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'DailyGridCalendarForm_CalendarComboCtrl-picker-listEl')))
    WebDriverWait(driver, 2).until(lambda driver: driver.find_element(By.ID, 'DailyGridCalendarForm_CalendarComboCtrl-picker-listEl').get_attribute('aria-hidden') == 'false')
    WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#DailyGridCalendarForm_CalendarComboCtrl-picker-listEl > li:nth-child(2)')))

    js_css_click(driver, '#DailyGridCalendarForm_CalendarComboCtrl-picker-listEl > li:nth-child(2)') # clicks on the "Full Grid" option

    # Waits for dropdown to close
    WebDriverWait(driver, 1).until(lambda driver: driver.find_element(By.ID, 'DailyGridCalendarForm_CalendarComboCtrl-picker-listEl').get_attribute('aria-hidden') == 'true')

    # opens the calendar configuration options
    calendar_configuration = driver.find_element(By.ID, 'button-1036')
    calendar_configuration.click()

    # defining input fields for start and end time, and the ok button
    start_time = driver.find_element(By.ID, 'undefinedcalendarConfigDlg_CalendarStartTime-inputEl')
    end_time = driver.find_element(By.ID, 'undefinedcalendarConfigDlg_CalendarEndTime-inputEl')
    ok_button = driver.find_element(By.ID, 'undefinedcalendarConfigDlg_OKBtn')

    # setting the start and end times to 12:00 AM and 11:59 PM respectively
    replace_content_of_element(driver, start_time, "12:00 AM")
    replace_content_of_element(driver, end_time, "11:59 PM")

    # confirm changes
    ok_button.click()

    # at this point we have done all of the setup we need to do to scrape the calendar. Now it's time for the funny

# replaces the content of given input element with the given new content
def replace_content_of_element(driver, elem, new_content):
    driver.execute_script(f"arguments[0].value = '{new_content}'", elem)

# clicks with javascript by id because stale element exceptions are annoying
def js_id_click(driver, id):
    # get element by id click
    driver.execute_script("document.getElementById(arguments[0]).click()", id)

# clicks with javascript because stale element exceptions are annoying
def js_css_click(driver, css_selector):
    # get element by css selector click
    driver.execute_script("document.querySelector(arguments[0]).click()", css_selector)

# the html on ad astra does not ever contain the information for every class. the classes that are loaded depend on the position of the vertical scrollbar.
# this generator obtains multiple html soups, each of which contains the information for a different set of classes.
def get_html_soups(driver, num_extra_soups, scroller):
    html = driver.page_source
    yield BeautifulSoup(html, 'html.parser')

    for i in range(1, num_extra_soups + 1):
        # set the scroll position to scroll_step * i.
        # ideally this will make it so that the scrollbar moves down in terms of percentage of the scroller height instead of pixels because the scroller height is not constant.
        scroll_height = driver.execute_script("return arguments[0].scrollHeight", scroller) * 1.02 # the height of the scroller in pixels, artificially increased by 2% to ensure we get all the data
        scroll_step = math.ceil(scroll_height / num_extra_soups) # the amount to scroll the scroller down by each time
        driver.execute_script(f"arguments[0].scrollTop = {scroll_step * i}", scroller) # scroll down by scroll_step pixels

        html = driver.page_source
        yield BeautifulSoup(html, 'html.parser')
        # sleep(0.1)

# scraping the classroom data from the html soups
def get_classroom_data(soups, previous_classroom_data):
    classroom_data = dict() if previous_classroom_data is None else previous_classroom_data # dictionary mapping classroom names to their unavailable times

    for date, value in soups.items():
        current_soup = value[0] # the soup we are currently scraping; the data we want is spread out across each one.
        current_soup_index = 0 # the index of the next soup we will scrape

        # this is being used to help us find out whether a class actually didn't show up in our html or if we just skipped over it.
        # this equals -1 as long as we are not looking for a class that caused us to skip to the next soup,
        # and is set to the index of the soup that we skipped over while we are.
        first_index_where_class_not_found = -1 

        try:
            # looping until we have addressed all classes
            for i in range(num_classes):
                # obtaining the classroom name, as a SELENIUM ELEMENT, NOT AS A STRING!
                current_class = current_soup.select_one(f'table[data-recordindex="{i}"] .x-grid-cell-first div') # the element containing the classroom name

                # if we get here the class is not in the blacklist. so we need to get its information for the current date
                # checking to see if the class is in the current frame
                
                while current_class is None: # if the classroom name is not in the current soup, we need to move to the next soup
                    # this variable equals -1 while we are not looking for a class that caused us to skip to the next soup.
                    # if this conditional is true, that means that this is the first instance of a miss.
                    if first_index_where_class_not_found == -1: 
                        first_index_where_class_not_found = current_soup_index # setting the index of the first class not found to the current soup index 
                    elif current_soup_index == first_index_where_class_not_found: # this conditional is true if we have gone through all the soups and not found the class we're looking for.
                        raise RuntimeError()
                
                    current_soup_index += 1

                    # the test see if we've gone through every soup and failed to find the class we're looking for.
                    # if this errors this doesn't mean we've failed. it means we'll start again at the beginning 
                    # until we find what we needed, or get back to where the problem started (in which case we will error)
                    if current_soup_index == len(value): # if we have gone through all the soups and not found the class, we need to go back tot he first one
                        current_soup_index = 0

                    current_soup = value[current_soup_index]
                        
                    print(f"looking for {i + 1} moving to index {current_soup_index}, first fail index {first_index_where_class_not_found}")
                    current_class = current_soup.select_one(f'table[data-recordindex="{i}"] .x-grid-cell-first div') # the element containing the classroom name

                classroom_name = current_class.text.strip() # the name of the classroom
                if classroom_name in blacklist:
                        print(f'{date} | {i + 1} of {num_classes} | {classroom_name}: skipped')
                else:
                    first_index_where_class_not_found = -1 # resetting the index of the first class not found, because we found it
                    classroom_timeframes = get_timeframes_of_class_by_current_id(i, current_soup) # the timeframes the classroom is occupied
                    classroom_data[classroom_name] = dict() if classroom_name not in classroom_data else classroom_data[classroom_name] # if the classroom is not already a key in classroom_data, we need to add it
                    classroom_data[classroom_name][date] = classroom_timeframes # adding the timeframes to the classroom data for this classroom on this particular date
                    print(f'{date} | {i + 1} of {num_classes} | {classroom_name}: {classroom_data[classroom_name][date]}')
        # when we fail to find a class in the current soup, we will delete the information for the current value of "date" from the classroom data.
        # the purpose of this is so that we can keep the data that we successfully scraped and only have to rescrape the data for the date that caused the error.
        except RuntimeError: 
            print(f"Failed to find class {i + 1} in soups.")

            for class_name, dates in classroom_data.items(): # iterating over the keys in the classroom data dictionary
                if date in dates:
                    print(f"Removing {date} from {class_name}")
                    del classroom_data[class_name][date] # removing all data corresponding to the value of "date"

            continue
    return classroom_data

   
def get_timeframes_of_class_by_current_id(id, current_soup):
    # converts a pixel interval to a string representing a timeframe
    def px_interval_to_time_string(interval):
        time_string = f"{px_to_time(interval.lower)} - {px_to_time(interval.upper)}"
        return time_string
    
    # converts a pixel length to a time
    def px_to_time(px):
        time = px / 70
        hours = math.floor(time) # we're treating this as hours elapsed since midnight. will be converted to 12-hour time below
        remainder = time - hours # remainder of time, will be converted to minutes below

        ret_minutes = math.floor(remainder * 60 / 5 + 0.5) * 5 # converting the remainder to minutes, in increments of 5 minutes

        if ret_minutes < 10: # if the minutes are less than 10, we need to add a 0 to the beginning
            ret_minutes = f"0{ret_minutes}"
        elif ret_minutes == 60: # if the minutes are 60 because of silly inconsistencies, we need to increment the hours and set the minutes to 0
            ret_minutes = "00"
            hours += 1
        
        ret_hour = None # the hour of the 12-hour time we will return
        am_pm = None # will be AM or PM, to be returned with the rest of the time

        # computing the hour and AM/PM portion of the 12-hour time
        match(hours):
            case 0 | 24:
                ret_hour = 12
                am_pm = "AM"
            case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11:
                ret_hour = hours
                am_pm = "AM"
            case 12:
                ret_hour = 12
                am_pm = "PM"
            case 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23:
                ret_hour = hours - 12
                am_pm = "PM"
        
        return f"{ret_hour}:{ret_minutes} {am_pm}"
        
    
    classroom_timeline = current_soup.select_one(f'table[id^="RoomDayGridId-timelineview-record-"][data-recordindex="{id}"]') # the element containing the event timeline graphics
    timeslot_styles = map(lambda timeslot: timeslot['style'], classroom_timeline.select('.x-grid-cell-inner > div:not(:last-child)')) # css styles of each timeslot in the timeline
    
    style_px_interval = P.closed(0, 24 * 70 + 1) # the time intervals that the classroom is occupied in pixels
    time_strings = []

    if timeslot_styles:
        for style in timeslot_styles:
            left_px = int(re.search(r'(?<=left:)(\d+)(?=px;)', style).group(0)) # the css left px property of the timeslot
            width_px = int(re.search(r'(?<=width:)(\d+)(?=px;)', style).group(0)) # the css width px property of the timeslot

            style_px_interval = style_px_interval - P.closed(left_px, left_px + width_px + 1) # union of the current interval and the new interval

        for subinterval in style_px_interval:
            time_strings.append(px_interval_to_time_string(subinterval)) # converting each interval to a time string
    return time_strings

if __name__ == '__main__':
    # Setting up argument parser for username and password, which will be used to attempt to login to ad astra
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='Username for Ad Astra')
    parser.add_argument('password', help='Password for Ad Astra')
    args = parser.parse_args()

    driver = webdriver.Edge()
    driver.implicitly_wait(3) # will wait at most 3 seconds for elements to exist before erroring. This is to prevent the program from running too fast and breaking

    # attempting login. If successful, we shall commence the funny
    if login(args.username, args.password, driver):
        soups = {}
        class_info = None
        
        # this variable is set to true whenever we obtain new data or remove old information. when it becomes true
        must_update_json = False 

        # getting the previous class info from the json file if it exists, so we can know what kind of info to be removed/added and what is already there.
        try:
            with open("class_info.json", "r") as f:
                class_info = json.load(f)
        except FileNotFoundError:
            pass

    # if (args.rescrape == "true"):
        # setting up the calendar before the funny
        setup_calendar(driver)
        
        # beginning the funny.
        # the soups dict will be mapped by date to the html soups we obtain from the calendar for that date.
        # right now we are getting TWO WEEKS worth of calendar data.
        scroller = driver.find_element(By.ID, 'ext-element-46') # the element that we use to scroll the calendar

        # getting current date in MM/DD format 
        current_date = datetime.today()
        current_date_formatted = f"{current_date.month}/{current_date.day}"

        num_extra_soups = 60 # the number of extra soups besides the first we will get for each date.
        
        if class_info is None: # if we don't have any previous class info, we need to get all the soups for today and the next 13 days
            must_update_json = True

            # adding new soups to the soups dict
            soups[current_date_formatted] = [soup for soup in get_html_soups(driver, num_extra_soups, scroller)] # getting the soups for the first date, today.
            
            for i in range(1, 14): # getting the rest of the 2 weeks worth of calendar data
                driver.execute_script(f"arguments[0].scrollTop = 0", scroller) # scrolling back to the top of the page
                current_date += timedelta(days=1) # incrementing the date by 1 day
                current_date_formatted = f"{current_date.month}/{current_date.day}" # formatted date for the soups dict
                current_date_formatted_with_year = f"{current_date.month}/{current_date.day}/{current_date.year}" # formatted date with year for the 

                date_input = driver.find_element(By.ID, 'RoomDayGridId_StartDateFilter-inputEl') # the input element where we specify the date
                replace_content_of_element(driver, date_input, current_date_formatted_with_year) # inputting new date
                sleep(0.1)

                # pressing enter to apply the date change... yes, twice.
                date_input.send_keys(Keys.ENTER)
                date_input.send_keys(Keys.ENTER) 

                # adding new soups to the soups dict
                soups[current_date_formatted] = [soup for soup in get_html_soups(driver, num_extra_soups, scroller)]
        else: # otherwise we only need to remove the info that isn't relevant anymore and scrape the stuff we need that isn't already 
            # removing the classes that are blacklisted from the class info dictionary
            for blacklisted_class in blacklist:
                if blacklisted_class in class_info:
                    must_update_json = True
                    print(f"Removing {blacklisted_class} from json file")
                    del class_info[blacklisted_class] 

            abpk_a19 = class_info.get("ABPK A19 - Lab-Engineering") # the ABPK A19 class info from the json file.

            next_fourteen_days = [current_date + timedelta(days=i) for i in range(14)] # today and the next 13 days from today
            next_fourteen_days_formatted = [f"{date.month}/{date.day}" for date in next_fourteen_days] # the next 14 days formatted for the soups dict

            # iterating over the keys in the abpk_a19 dictionary, which are the dates from the previous json file.
            # deleting the keys that are not in the next fourteen days formatted list, which happen to be the dates we don't need anymore.
            abpk_a19_keys = list(abpk_a19.keys()) # the keys in the abpk_a19 dictionary, which are the dates from the previous json file.

            for key in abpk_a19_keys:
                if key not in next_fourteen_days_formatted:
                    print(f"Removing {key} from json file")
                    for class_name, dates in class_info.items():
                        if key in dates:
                            must_update_json = True
                            del class_info[class_name][key]

            unaddressed_dates = [date for date in next_fourteen_days if f"{date.month}/{date.day}" not in abpk_a19_keys] # the dates that are in the next fourteen days but not in the abpk_a19 dictionary
            if len(unaddressed_dates) != 0: # if there are any unaddressed dates, we need to scrape them
                must_update_json = True
                unaddressed_dates_formatted = [date for date in next_fourteen_days_formatted if date not in abpk_a19_keys] # the dates that are in the next fourteen days formatted list but not in the abpk_a19 dictionary
                
                current_date = unaddressed_dates[0] # the first date we are looking at
                current_date_formatted = unaddressed_dates_formatted[0] # the first date in the unaddressed dates list
                current_date_formatted_with_year = f"{current_date.month}/{current_date.day}/{current_date.year}" # formatted date with year
                
                date_input = driver.find_element(By.ID, 'RoomDayGridId_StartDateFilter-inputEl') # the input element where we specify the date
                replace_content_of_element(driver, date_input, current_date_formatted_with_year) # inputting new date
                sleep(0.1)

                # pressing enter to apply the date change... yes, twice.
                date_input.send_keys(Keys.ENTER)
                date_input.send_keys(Keys.ENTER) 
                
                soups[current_date_formatted] = [soup for soup in get_html_soups(driver, num_extra_soups, scroller)] # getting the soups for the first date, today.
                
                for i in range(1, len(unaddressed_dates)): # getting the rest of the 2 weeks worth of calendar data
                    driver.execute_script(f"arguments[0].scrollTop = 0", scroller) # scrolling back to the top of the page
                    current_date = unaddressed_dates[i] # the current date we are looking at
                    current_date_formatted = unaddressed_dates_formatted[i] # the current date formatted for the soups dict
                    current_date_formatted_with_year = f"{current_date.month}/{current_date.day}/{current_date.year}" # formatted date with year

                    date_input = driver.find_element(By.ID, 'RoomDayGridId_StartDateFilter-inputEl') # the input element where we specify the date
                    replace_content_of_element(driver, date_input, current_date_formatted_with_year) # inputting new date
                    sleep(0.1)

                    # pressing enter to apply the date change... yes, twice.
                    date_input.send_keys(Keys.ENTER)
                    date_input.send_keys(Keys.ENTER) 

                    # adding new soups to the soups dict
                    soups[current_date_formatted] = [soup for soup in get_html_soups(driver, num_extra_soups, scroller)]
            else: # if there are no unaddressed dates, we don't need to do anything really and we can just end the program here
                print("Class info is already up to date.")

        
        driver.quit() # we don't need the driver anymore

        if must_update_json: # if we need to update the json file, we need to get the classroom data from the soups, if there is any new information
            class_info = get_classroom_data(soups, class_info) # scraping the classroom data from the soups

            # outputting the classroom data to a json file
            with open("class_info.json", "w") as f:
                json.dump(class_info, f)
        
    else: # if login failed
        print("Login failed. Please check your username and password.")
        driver.quit()