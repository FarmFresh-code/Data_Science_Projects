#   File: Neil_Opitz_DSC510_Week_12_Assignment.py
#   Final Project
#   Name: Neil Opitz
#   Date: 11/15/2019
#   Course: DSC 510 - Introduction To Programming
#   Description: The program asks the user if they would like to enter either a zip code or city location to get a weather conditions for that location.
#   Usage: The program determines if a zipcode or city name will be entered by the user, then validates the user entry.  The program uses a GET request
#   to obtain the forecast for the location from the server. The server returns json data containing several weather forecast variables.  
#   The program parses the data, stores only the required weather data in a response.json() variable, and prints the forecast data to the user.  
#   The program prompts the user for another forecast and implements error checking with a sentinel value for their response.

import requests
import json

unit = 'imperial'
url = "http://api.openweathermap.org/data/2.5/forecast?"
my_api = "8cdfe197cb57f8740647af0de77362ce"

# function for determining if user inputted 5 digit zip code
def properFormatZip(zip_prompt):
    five_digits = False
    zipnum = 0
    for z in zip_prompt:        
        if z.isdigit():
            zipnum += 1
    if zipnum == 5:
        five_digits = True            
    return five_digits

# function for determining if user included numbers in city name
def properFormatCity(city_prompt):
    number_flag = False
    for c in city_prompt:
        if c.isdigit():
            number_flag = True
    return number_flag

# function to ask user to choose a city or zip code entry or to opt out of program
def promptZipOrCity(decision):
    while decision != sentinel_value:  
        decision = input('\nPress any key and Enter to view the forecast for a city or US zip code.  If you wish to exit the program enter \'No\' : ')

        if decision == sentinel_value:
            exitProgram()
            break
             
        location_prompt = (input('\nEnter a 1 to input a US zip code or enter a 2 in input a city: '))  
           
        if len(location_prompt) > 0:
            try:
                location_prompt = location_prompt.lstrip()
                if location_prompt == '1':
                    zipcodeWeather(url, my_api)

                elif location_prompt == '2':
                    cityWeather()

                else:
                    print('\nYou did not enter a \'1\' or a \'2\'.')
               
            except ValueError:
                print ('\nYou did not enter a \'1\' or a \'2\'.')

# function that checks if zip code is valid
def validateZip(zip_prompt_string):
    url_zipcode = url + "appid=" + my_api + "&q=" + zip_prompt_string  + ',US' + '&mode=json&units=' + unit
    # GET request to website
    response = requests.get(url_zipcode)                        
    # status code check
    if response.status_code == 200:
        print('\nWe found a forecast for your city!')
        valid_zipcode = True

    elif response.status_code == 404:
        print('\nNo forecast found for your city.')
        valid_zipcode = False

    return valid_zipcode
    
# function for entering zip code
def zipcodeWeather(url, my_api):
    city_temp_list = []
    city_sky_list = []
    j=0
    while j==0:
        print('\nYou will need to enter a properly formatted US zip code, which is a 5 digit number such as \'68104\'.\n')
        zip_prompt = (input('Input a properly formatted US zip code and press enter: '))
        zip_prompt_string = str(zip_prompt)
        zip_prompt_string = zip_prompt_string.lstrip()
                         
        if len(zip_prompt) > 0:
            validate_zip = False

            # Try / Except to test for integer input
            try:
                zipcode = int(zip_prompt)
                
                proper_format_zipcode = properFormatZip(zip_prompt_string)
                
                if proper_format_zipcode:
                    validate_zip = validateZip(zip_prompt_string)
                                                
                try:
                    if validate_zip:
                        j=1
                        print('\nYou entered a valid US zip code: ',zip_prompt_string)
                        
                        # request validated zip code forecast data
                        url_zipcode = url + "appid=" + my_api + "&q=" + zip_prompt_string  + ',US' + '&mode=json&units=' + unit
                        response = requests.get(url_zipcode)
                        # save data as json dictionary data
                        dict = response.json()
                        select_data = dict['list']
                                                
                        get_weather = weatherData(select_data, city_temp_list, city_sky_list)

                except ValueError:
                    print ("\nThe zip code you entered does not exist.")

            except ValueError:
                print ("\nYou did not enter a properly formatted zip code.")


        elif len(zip_prompt) == 0:
            print("\nYou did not enter a zip code.")

    forecast = printForecast(city_temp_list, city_sky_list)

    return city_temp_list, city_sky_list
               

# function that checks if a city name is valid
def validateCity(city):
    url_city = url + "appid=" + my_api + "&q=" + city + ',US' + '&mode=json&units=' + unit
    # GET request to website
    response = requests.get(url_city)                        
    # status code check
    if response.status_code == 200:
        print('\nWe found a forecast for your city!')
        valid_city_name = True

    elif response.status_code == 404:
        print('\nNo forecast found for your city.')
        valid_city_name = False

    return valid_city_name

# function for entering city
def cityWeather():
    city_temp_list = []
    city_sky_list = []
    i=0
    while i==0:
        print('\nYou will need to enter a properly formatted city name, such as \'Detroit\'.')
        city_prompt = input('\nInput a properly formatted city name and press enter:')
        city_prompt = city_prompt.lstrip()
           
        if len(city_prompt) > 0:
            city_name_validation = False
               
            try:
                   
                proper_format_city_prompt = properFormatCity(city_prompt)
                if proper_format_city_prompt:
                    print('\nYou included a number in the city name.')
                    
                elif proper_format_city_prompt == False:  # entered city name does not contain any numbers
                    
                    city = city_prompt.title()

                    # check to see if city is an actual city name
                    city_name_validation = validateCity(city)

                try:
                    if city_name_validation:
                        i=1
                        print('\nYou entered a valid US city name: ',city)

                        # request validated city forecast data
                        url_city = url + "appid=" + my_api + "&q=" + city + ',US' + '&mode=json&units=' + unit
                        response = requests.get(url_city)
                        # save data as json dictionary data
                        dict = response.json()
                        select_data = dict['list']
                                                
                        get_weather = weatherData(select_data, city_temp_list, city_sky_list)

                except ValueError:
                    print ("\nThe city you entered does not exist.")

            except ValueError:
                print ("\nYou did not enter a properly formatted city name.")


        elif len(city_prompt) == 0:
            print("\nYou did not enter a city name.")

    forecast = printForecast(city_temp_list, city_sky_list)

    return city_temp_list, city_sky_list


# function that aggregates the parsed weather data into lists
def weatherData(select_data, city_temp_list, city_sky_list):
    day1_temp_list = []
    day2_temp_list = []
    day3_temp_list = []
    day4_temp_list = []
    day5_temp_list = []
    
    j = 0

    # parse 3 hour temperature data into daily lists               
    for box in select_data:
        if j < 8:
            day1_temp_list.append(box['main']['temp_min'])
            day1_temp_list.append(box['main']['temp_max'])
        if j >= 8 and j < 16:
            day2_temp_list.append(box['main']['temp_min'])
            day2_temp_list.append(box['main']['temp_max'])
        if j >= 16 and j < 24:
            day3_temp_list.append(box['main']['temp_min'])
            day3_temp_list.append(box['main']['temp_max'])
        if j >= 24 and j < 32:
            day4_temp_list.append(box['main']['temp_min'])
            day4_temp_list.append(box['main']['temp_max'])
        if j >= 32:
            day5_temp_list.append(box['main']['temp_min'])
            day5_temp_list.append(box['main']['temp_max'])
        j+=1

    # extract min and max daily temperatures and append to list
    city_temp_list.append(min(day1_temp_list))
    city_temp_list.append(max(day1_temp_list))
    city_temp_list.append(min(day2_temp_list))
    city_temp_list.append(max(day2_temp_list))
    city_temp_list.append(min(day3_temp_list))
    city_temp_list.append(max(day3_temp_list))
    city_temp_list.append(min(day4_temp_list))
    city_temp_list.append(max(day4_temp_list))
    city_temp_list.append(min(day5_temp_list))
    city_temp_list.append(max(day5_temp_list))

    s = 0
    # parce sky type at noon each day and append to list
    for box in select_data:                       
        for sky in box['weather']:
            # select the sky type at noon
            if s == 3 or s == 11 or s == 19 or s== 27 or s==35:
                city_sky_list.append(sky['main'])
            s+=1

    return city_temp_list, city_sky_list            

# function that prints forecast
def printForecast(city_temp_list, city_sky_list):

    print('   Day {}:   Low Temperature: {}   High Temperature: {}   Skies: {}'.format(1,int(city_temp_list[0]), int(city_temp_list[1]), city_sky_list[0]))
    print('   Day {}:   Low Temperature: {}   High Temperature: {}   Skies: {}'.format(2,int(city_temp_list[2]), int(city_temp_list[3]), city_sky_list[1]))    
    print('   Day {}:   Low Temperature: {}   High Temperature: {}   Skies: {}'.format(3,int(city_temp_list[4]), int(city_temp_list[5]), city_sky_list[2]))
    print('   Day {}:   Low Temperature: {}   High Temperature: {}   Skies: {}'.format(4,int(city_temp_list[6]), int(city_temp_list[7]), city_sky_list[3]))
    print('   Day {}:   Low Temperature: {}   High Temperature: {}   Skies: {}'.format(5,int(city_temp_list[8]), int(city_temp_list[9]), city_sky_list[4]))
   
# program exit function
def exitProgram():
    print('\nThank you for visiting this program.  We hope you enjoyed your experience.')
    print('\nGood bye.')

sentinel_value = 'No'
decision = '1'

print('Welcome to the Weather Forecast program!')

promptZipOrCity(decision)
