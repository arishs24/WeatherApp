#-----------------------------------------------------------------------------
# Name:        Weather Whiz (assignment.py)
# Purpose:     A weather app with personalized units and daily updated news, along with weather forecast updated from online API
#			   and option to store favorite city, music to relax user, along with notifications for user ease.
#
# Author:      Arish Shahab
# Created:     25-05-2023
# Updated:     09-06-2023
#-----------------------------------------------------------------------------
#I think this project deserves a level 4+ because # I think this project deserves a level 4+ because I have completed all the level 3 requirements with complete efficiency, I have added additional features
# along with the level 3 requirements, and completed level 3+ requirements in different, creative ways, to ensure efficiency. Along with that, I made regular
# commits as much as I could, as I had to complete this assignment with medical issues, and I submitted it by a deadline agreed with by the teacher,
#
#Features Added: Personalized Units, real news data from BBC updated live, live updated weather data from API, option to favorite a city, personalized notifications
#                music, animated pictures, pictures to help with weather data, saves city when application closed, use of lists and classes
#   ...
#   ...
#   ...
#-----------------------------------------------------------------------------
import pygame
import requests
import pytz
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from rectangle_class import Rectangle
from plyer import notification

#*********SETUP**********
pygame.init()

#Initialized mixer for sounds
pygame.mixer.init()

#set up size of window
screen_width = 1280
screen_height = 720

#Loads music file for background music
pygame.mixer.music.load("bg.mp3")

#volume for background
pygame.mixer.music.set_volume(10)

#plays background music
pygame.mixer.music.play(-1)

#Made an account with openweathermap and got an API key to
#get live info for weather from openweather API, referenced later in code
api_key = 'e969794ec9987da732e8ae5af494d347'


#Sets the size and the program file name
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Weather Whizz")

#Loads all required images before referenced later, sets the size, and removes bg
background_image = pygame.image.load("background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

sun_image = pygame.image.load("sun.png").convert_alpha()
sun_image = pygame.transform.scale(sun_image, (200, 200))
cloud_image = pygame.image.load("cloud.png").convert_alpha()
cloud_image = pygame.transform.scale(cloud_image, (200, 200))
frost_image = pygame.image.load("frost.png").convert_alpha()
frost_image = pygame.transform.scale(frost_image, (200, 150))

whizz_image = pygame.image.load("whizz.png").convert_alpha()
whizz_image = pygame.transform.scale(whizz_image, (650, 150))

news_image = pygame.image.load("news.png").convert_alpha()
news_image = pygame.transform.scale(news_image, (650, 150))

#Initializes saved city to blank so it can have a value later on in the code
default_city = ""

# Load the player images for animation
# load the player images and create a list of images for animation. The images are loaded from files named "sunny1.png" through "sunny8.png" 
sunny_images = []
for i in range(1, 8):
    sunny_image = pygame.image.load(f"sunny{i}.png").convert_alpha()
    sunny_image = pygame.transform.scale(sunny_image, (200, 200))
    sunny_images.append(sunny_image) #append adds it to the list
    

# animation variables
animation_frame = 0  # Index of which image is currently displayed
animation_timer = 0  # Set to 0, increases as animation changes
animation_delay = 15  # this value controls animation speed

# Create a font object, initialize font
font = pygame.font.Font('Antonio-Regular.ttf', 38)
font1 = pygame.font.Font('Antonio-Regular.ttf', 18)
font2 = pygame.font.Font('ostrich-regular.ttf', 38)
font3 = pygame.font.Font('alert.ttf', 45)
font4 = pygame.font.Font('fun.ttf', 60)
font5 = pygame.font.Font('news.ttf', 45)

# Set the text content and color forthe title
text_content = "Weather Whizz"
text_color = (255, 255, 255)

# Render the text, initializes text
text = font.render(text_content, True, text_color)

# Set the position of the text
text_x = 550
text_y = 46


# File path for storing the default city
default_city_file = "default_city.txt"

# Variable to store the user's input text
saved_input_text = ""

# Function to save the default city to a file
def save_default_city(city):
    """
    Save the default city to a file.

    Parameters:
        city (string): The default city to be saved

    Returns:
        None
    """
    # Open the default city file in write mode
    with open(default_city_file, "w") as file:
        # Write the provided city to the file
        file.write(city)

# Function to load the default city from the file
def load_default_city():
    """
    Load the default city from a file

    Returns:
        string: The loaded default city.
    """
    try:
        # Open the default city file in read mode
        with open(default_city_file, "r") as file:
            # Read the content of the file and remove leading/trailing whitespace
            return file.read().strip()
    except FileNotFoundError:
        # If the file is not found, print an error message and return an empty string
        return ""

# Function to show a notification
def show_notification(title, message):
    """
    Show a notification with the provided title and message.

    Parameters:
        title (string): The title of the notification.
        message (string): The content/message of the notification.

    Returns:
        None
    """
    # Use the 'notification' module to display a notification
    notification.notify(
        # Set the title of the notification
        title=title,
        # Set the message/content of the notification
        message=message,
        # Specify the path to the application icon file to be displayed in the notification
        app_icon='favicon.ico',
        # Set the timeout duration for the notification (in seconds)
        timeout=10
    )
      


def draw_welcome():
    '''
     Description: Draws the welcome screen of the weather app.
 
     Parameters:
         None
 
     Return:
         None
    '''
    # Draw the background image
    screen.blit(background_image, (0, 0))
    
    # Draw the Weather Whizz logo
    screen.blit(whizz_image, (330, 50))
    
    # Draw the first box
    box1 = Rectangle(300, 570, 200, 100, (255, 0, 0))
    box1.draw(screen)
    
    # Draw the second box
    box2 = Rectangle(550, 570, 200, 100, (0, 255, 0))
    box2.draw(screen)
    
    # Draw the third box
    box3 = Rectangle(800, 570, 200, 100, (0, 0, 255))
    box3.draw(screen)
    

    # Render the text labels on the boxes
    label1_content = "Your Weather"
    label2_content = "News"
    label3_content = "Settings"

    label1 = font.render(label1_content, True, text_color)
    label2 = font.render(label2_content, True, text_color)
    label3 = font.render(label3_content, True, text_color)

    label1_x = box1.x + (box1.width - label1.get_width()) // 2
    label1_y = box1.y + (box1.height - label1.get_height()) // 2

    label2_x = box2.x + (box2.width - label2.get_width()) // 2
    label2_y = box2.y + (box2.height - label2.get_height()) // 2

    label3_x = box3.x + (box3.width - label3.get_width()) // 2
    label3_y = box3.y + (box3.height - label3.get_height()) // 2

    screen.blit(label1, (label1_x, label1_y))
    screen.blit(label2, (label2_x, label2_y))
    screen.blit(label3, (label3_x, label3_y))
    
    # Blit the player image, with the animation frame to animate sun
    screen.blit(sunny_images[animation_frame], (1050, 60))

def draw_settings():
    ''' 
    Description: Draws the settings screen of the weather app

    Parameters:
       None

    Return:
       None
    '''
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Define the settings options positions and dimensions
    box1_x = 300
    box1_y = screen_height - 150
    box1_width = 200
    box1_height = 100

    box2_x = 800
    box2_y = screen_height - 150
    box2_width = 200
    box2_height = 100

    # Draw the settings option boxes
    pygame.draw.rect(screen, (255, 255, 255), (box1_x, box1_y, box1_width, box1_height))
    pygame.draw.rect(screen, (255, 255, 255), (box2_x, box2_y, box2_width, box2_height))

    # Render the text labels on the boxes
    label1_content = "Fahrenheit"
    label2_content = "Celsius"

    label1 = font.render(label1_content, True, (0,0,0))
    label2 = font.render(label2_content, True, (0,0,0))

    label1_x = box1_x + (box1_width - label1.get_width()) // 2
    label1_y = box1_y + (box1_height - label1.get_height()) // 2

    label2_x = box2_x + (box2_width - label2.get_width()) // 2
    label2_y = box2_y + (box2_height - label2.get_height()) // 2

    screen.blit(label1, (label1_x, label1_y))
    screen.blit(label2, (label2_x, label2_y))
    
    # Render the screen title
    title_content = "Settings"
    title = font.render(title_content, True, text_color)

    title_x = screen_width // 2 - title.get_width() // 2
    title_y = 100

    screen.blit(title, (title_x, title_y))
    
    # Draw the back button to navigate through the screen
    back_image = pygame.image.load("backy2.png").convert_alpha()
    back_image = pygame.transform.scale(back_image, (200, 100))
    screen.blit(back_image, (31, 23))


def draw_news():
    ''' 
    Description: Draws the news screen of the weather app

    Parameters:
       None

    Return:
       None
    '''
    global news_text
    global news_x
    global news_y
    # Declare global variables for news text and position
    
    screen.blit(background_image, (0, 0))
    # Draw the background image on the screen at position (0, 0)
    
    # Define the URL of the webpage from which code fetches the news headlines
    url = 'https://www.bbc.com/news'

    # Send an HTTP request to the URL and get response
    response = requests.get(url)

    # Create a BeautifulSoup object to analyze data from the HTML content of the response
    # The 'BeautifulSoup' class is provided by the BeautifulSoup library and is used to analyze HTML documents
    #pass the HTML content of the response object to the BeautifulSoup constructor along with the parser provided by the library ('html.parser')
    # Now, it can navigate and extract data from the HTML structure of the webpage in a simple way
    soup = BeautifulSoup(response.text, 'html.parser') # Referenced from this website (https://beautiful-soup-4.readthedocs.io/en/latest/)

    # Getting all the <h3> elements with the CSS class 'gs-c-promo-heading__title', that represent the news headlines on the website
    headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')
    # Fetch news headlines from the website using BeautifulSoup
    #Referenced from this website (https://stackoverflow.com/questions/50590445/data-scraping-using-python-and-bs4)
    # and referneced from here (https://www.youtube.com/watch?v=MxseaVcUd1M&ab_channel=Iknowpython)
    
    # Render the "Today's News" text using the specified font and color
    news_text = font.render("Today's News", True, (0, 0, 0))
    
    # Draw the news image on the screen at position (350, 80)
    screen.blit(news_image, (350, 80))
    
    # Set the initial position for rendering headlines
    news_x = 500
    news_y = 150
    
    # Create a font object for rendering the headlines
    headline_font = pygame.font.Font('ostrich-regular.ttf', 35)
    
     # Set the initial position for rendering headlines
    screen_width, screen_height = screen.get_size()
    headline_x = 406
    headline_y = 259
   
    # Define the maximum number of headlines to display
    max_headlines = 5
    
    # Load and scale the back button image
    back_image = pygame.image.load("backy2.png").convert_alpha()
    back_image = pygame.transform.scale(back_image, (200, 100))
    
    # Draw the back button on the screen at position (31, 23)
    screen.blit(back_image, (31, 23))
    
    # Initialize variables for headline counting and duplicate checking, so won't show the same news twice
    headline_counter = 0
    rendered_headlines = set()
    
    for headline in headlines:
        # Break the loop if the maximum number of headlines is reached
        if headline_counter >= max_headlines:
            break
        
        # Extract and strip the text of the headline, removes white space, just extracts text
        headline_text = headline.text.strip()
        
        # If there is a duplicate, it skips
        if headline_text in rendered_headlines:
            continue
        
        # Render the headline text using the specified font and color
        headline_rendered = font4.render(headline_text, True, (0, 0, 0))
        
        # Calculate the centered coordinates for the headline
        headline_rect = headline_rendered.get_rect(center=(headline_x, headline_y))
        
        # Draw the headline on the screen at position (200, headline_y)
        screen.blit(headline_rendered, (200, headline_y))
        
        # Update the position for the next headline
        headline_y += 80
        
        # Increase the counter and add the headline to the set of rendered headlines
        headline_counter += 1
        rendered_headlines.add(headline_text)
        
# Initialize the input_text variable, creating an empty string, for the search box  
input_text = ""


def draw_weather():
    ''' 
    Description: Draws the weather screen of the weather app

    Parameters:
       None

    Return:
       None
    '''
    # Declare variables as a global variable to access them inside the function
    global save_button
    global save_button_x
    global save_button_y
    global search_button_y
    global search_box_height
    global search_button_x
    global search_button_width
    global saved_text
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the search box
    search_box_x = 400
    search_box_y = 50
    search_box_width = 500
    search_box_height = 50

    pygame.draw.rect(screen, (255, 255, 255), (search_box_x, search_box_y, search_box_width, search_box_height))
    
    # Render the search box label
    label_content = "Search: "
    label = font.render(label_content, True, text_color)
    label_x = search_box_x - label.get_width() - 10
    label_y = search_box_y + (search_box_height - label.get_height()) // 2
    screen.blit(label, (label_x, label_y))
    
    # Render the input text
    input_font = pygame.font.Font(None, 24)
    input_label = input_font.render(input_text, True, (0, 0, 0))
    input_x = search_box_x + 10
    input_y = search_box_y + (search_box_height - input_label.get_height()) // 2
    screen.blit(input_label, (input_x, input_y))
    
    # Render the search button
    search_button_x = search_box_x + search_box_width + 10
    search_button_y = search_box_y
    search_button_width = 100
    search_button_height = search_box_height
    
    pygame.draw.rect(screen, (0, 255, 0), (search_button_x, search_button_y, search_button_width, search_button_height))

    search_button_label = font.render("Search", True, (0, 0, 0))
    search_button_label_x = search_button_x + (search_button_width - search_button_label.get_width()) // 2
    search_button_label_y = search_button_y + (search_button_height - search_button_label.get_height()) // 2
    screen.blit(search_button_label, (search_button_label_x, search_button_label_y))
    
    
    # Render the save button
    save_button_x = search_button_x + search_button_width + 10
    save_button_y = search_button_y
    save_button_width = 180
    save_button_height = search_box_height
    
    if show_weather == True:
        pygame.draw.rect(screen, (255, 0, 0), (save_button_x, save_button_y, save_button_width, save_button_height))

    save_button_label = font1.render("Save as default location", True, (0, 0, 0))
    save_button_label_x = save_button_x + (save_button_width - save_button_label.get_width()) // 2
    save_button_label_y = save_button_y + (save_button_height - save_button_label.get_height()) // 2
    
    if show_weather == True:
        screen.blit(save_button_label, (save_button_label_x, save_button_label_y))
    
    # Creates a back button to navigate through the screen
    back_image = pygame.image.load("backy2.png").convert_alpha()
    back_image = pygame.transform.scale(back_image, (200, 100))
    screen.blit(back_image, (31, 23))
    
    



#define gamestates
welcome = 0
settings = 1
weather = 2
news = 3
game = 4

#sets the original gamestate
currentgame_state = welcome

#Sets initial value for booleans
show_celsius = True

check_weather = False

show_weather = False

show = False


def mouse_click(pos):
    ''' 
    Description: Draws the weather screen of the weather app

    Parameters:
       pos(tuple); gets x and y position of the mouse

    Return:
       None
    '''
    # Declare variables as a global variable to access them inside the function
    global currentgame_state
    global show_weather
    global temp_text
    global desc_text
    global temp_x
    global temp_y
    global desc_x
    global desc_y
    global input_text
    global time_text
    global time_x
    global time_y
    global humidity_text
    global humidity_x
    global humidity_y
    global pressure_text
    global pressure_x
    global pressure_y
    global wind_text
    global wind_x
    global wind_y
    global error_text
    global error_x
    global error_y
    global show_fail
    global weather_image
    global image_x
    global image_y
    global celc_text
    global celc_x
    global celc_y
    global fahr_text
    global fahr_x
    global fahr_y
    global celc_show
    global fahr_show
    global show_celsius
    global input_text
    global city_text
    global city_text_x
    global city_text_y
    global check_weather
    global save_default_city
    global show
    global saved_text
    global saved_input_text
    global default_city

    # Extracts x and y coords
    x = pos[0]
    y = pos[1]

    if currentgame_state == welcome:
        # Check if the click is within the weather button bounds
        if x < 300 + 200 and x > 300 and y < 570 + 100 and y > 570:
            currentgame_state = weather  # Set currentgame_state to 'weather'

    if currentgame_state == weather:
        # Check if the click is within the back button bounds
        if x < 31+200 and x > 31 and y < 23+100 and y > 23:
            currentgame_state = welcome  # Set currentgame_state to 'welcome'

    if currentgame_state == welcome:
        # Check if the click is within the settings button bounds
        if x < 800 + 200 and x > 800 and y < 570 + 100 and y > 570:
            currentgame_state = settings  # Set currentgame_state to 'settings'

    if currentgame_state == settings:
        # Check if the click is within the back button bounds
        if x < 31+200 and x > 31 and y < 23+100 and y > 23:
            currentgame_state = welcome  # Set currentgame_state to 'welcome'

    if currentgame_state == welcome:
        # Check if the click is within the news button bounds
        if x < 550 + 200 and x > 550 and y < 570 + 100 and y > 570:
            currentgame_state = news  # Set currentgame_state to 'news'

    if currentgame_state == news:
        # Check if the click is within the back button bounds
        if x < 31+200 and x > 31 and y < 23+100 and y > 23:
            currentgame_state = welcome  # Set currentgame_state to 'welcome'

    if currentgame_state == settings:
        # Check if the click is within the Fahrenheit button bounds
        if x < 300 + 200 and x > 300 and y < 570 + 100 and y > 570:
            show_celsius = False  # Set show_celsius to False (use Fahrenheit as default)
            fahr_text = font.render("Default Unit = F", True, (0, 0, 0))

    if currentgame_state == settings:
        # Check if the click is within the Celsius button bounds
        if x < 800 + 200 and x > 800 and y < 570 + 100 and y > 570:
            show_celsius = True  # Set show_celsius to True (use Celsius as default)
            celc_text = font.render("Default Unit = C", True, (0, 0, 0))

    if currentgame_state == weather and check_weather == True:
        # Check if the click is within the save button bounds
        if x < 1020 + 180 and x > 1020 and y < 50 + 50 and y > 50:
            show = True  # Set show to True (display "Saved!" message)
            saved_text = font4.render("Saved!", True, (0, 0, 0))
            save_default_city(saved_input_text)  # Call the save_default_city function with saved_input_text as parameter

               
    if currentgame_state == weather:
        check_weather = False
        show_fail = False
        if default_city or x < 910 + 100 and x > 910 and y < 50 + 50 and y > 50:
            check_weather = True
        if check_weather == True:
            #Sets the URL and city text based on input or saved city
            if input_text:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={input_text}&appid={api_key}'
                city_text = font3.render(input_text, True, (0, 0, 0))
            else:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={default_city}&appid={api_key}'
                city_text = font3.render(default_city, True, (0, 0, 0))
            city_text_x = 525
            city_text_y = 130
            #  Send an HTTP request to the URL and gets response
            response = requests.get(url)
            # 200 means it is successful and continue with the code
            if response.status_code == 200: #Referenced from this website, https://beapython.dev/2023/03/18/build-a-simple-weather-app-in-python-using-openweathermap-api/
                saved_input_text = input_text
                # Converts into json object, so it can be accessed in code 
                data = response.json() 
                # Extract temperature data from the JSON response
                temp = data['main']['temp']

                # Clear the input text for the search box
                input_text = ""

                # Extract humidity, pressure, wind speed, and weather description from the response
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                wind_speed = data['wind']['speed']
                desc = data['weather'][0]['description']
                
                
                # Retrieve the time zone for the given city
                timezone = data['timezone']
                
                # Adjust the current time based on the time zone
                city_time = datetime.utcnow() + timedelta(seconds=timezone) # Referenced from this website (
                #https://stackoverflow.com/questions/62623062/get-time-from-city-name-using-python)
                #https://www.youtube.com/watch?v=78ZKWdhX-Pw
                
                # Format the city time as a string
                time_str = city_time.strftime('%H:%M:%S')

                # Create text surfaces for temperature and description
                if show_celsius == True:
                    # Convert from Kelvin to C
                    temp = temp - 273
                    temp = round(temp, 2)
                    temp_text = font.render(f'Temperature: {temp} °C', True, (255, 255, 0))
                if show_celsius == False:
                    # Convert from kelvin to F
                    temp = 1.8 * (temp - 273) + 32
                    temp = round(temp, 2)
                    temp_text = font.render(f'Temperature: {temp} °F', True, (255, 255, 0))
                
                desc_text = font.render(f'Description: {desc}', True, (255, 255, 0))
                time_text = font4.render(f'Time: {time_str}', True, (255, 255, 255))
                
                # Create text surfaces for humidity, pressure, and wind speed
                humidity_text = font.render(f'Humidity: {humidity}%', True, (255, 255, 0))
                pressure_text = font.render(f'Pressure: {pressure} hPa', True, (255, 255, 0))
                wind_text = font.render(f'Wind Speed: {wind_speed} m/s', True, (255, 255, 0))
                           
                # Specify the positions for the text surfaces
                temp_x = 35
                temp_y = 228

                desc_x = 35
                desc_y = 468
                
                # Specify the position for the time text surface
                time_x = 35
                time_y = 168
                
                # Specify the positions for the text surfaces
                humidity_x = 35
                humidity_y = 288

                pressure_x = 35
                pressure_y = 348

                wind_x = 35
                wind_y = 408

                # Draw the text surfaces on the screen
                show_weather = True
                
                image_x = 500
                image_y = 300
        
                # Sends notification to display and displays image based on weather
                if temp > 15:
                    show_notification("Weather App", "Today's weather forecast: Warm, wear a t-shirt")
                    weather_image = sun_image
                elif temp >= 5 and temp <= 15:
                    show_notification("Weather App", "Today's weather forecast: A little chilly, wear a sweater")
                    weather_image = cloud_image
                else:
                    weather_image = frost_image
                    show_notification("Weather App", "Today's weather forecast: It's COLD, wear a JACKET!")
                    
                # If response is not 200 or not valid, or city name is not found from API website, gives an error
            else:
                show_fail = True
                show_weather = False
                input_text = ""
                error_text = font3.render('Error fetching weather data!', True, (255, 0, 0))
                error_x = 340
                error_y = 336
                
# Game loop
running = True
while running:
    # Load default city from saved data
    default_city = load_default_city()

    # Update animation frame
    animation_timer += 1
    if animation_timer >= animation_delay:
        animation_frame = (animation_frame + 1) % 4  # Wrap around at 4 frames
        animation_timer = 0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If quit event detected, exit the game loop
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse button is clicked, get the mouse position and handle the click
            pos = pygame.mouse.get_pos()
            mouse_click(pos)
        if event.type == pygame.KEYDOWN and currentgame_state == weather:
            # Key is pressed down and the game state is weather
            if event.key == pygame.K_RETURN:
                # Enter key is pressed, trigger weather checking
                check_weather = True
            elif event.key == pygame.K_BACKSPACE:
                # Backspace key is pressed, remove the last character from the input text
                input_text = input_text[:-1]
            else:
                # Any other key is pressed, append the unicode character to the input text
                input_text += event.unicode


    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the appropriate screen based on the game state
    if currentgame_state == welcome:
        draw_welcome()
    if currentgame_state == settings:
        draw_settings()
    if currentgame_state == weather:
        draw_weather()
    if currentgame_state == news:
        draw_news()

    # Display Celsius or Fahrenheit text based on settings
    if currentgame_state == settings and show_celsius == True:
        screen.blit(celc_text, (550, 500))
    if currentgame_state == settings and show_celsius == False:
        screen.blit(fahr_text, (550, 500))

    # Display weather information if enabled
    if currentgame_state == weather and show_weather == True:
        screen.blit(temp_text, (temp_x, temp_y))
        screen.blit(desc_text, (desc_x, desc_y))
        screen.blit(time_text, (time_x, time_y))
        screen.blit(humidity_text, (humidity_x, humidity_y))
        screen.blit(pressure_text, (pressure_x, pressure_y))
        screen.blit(wind_text, (wind_x, wind_y))
        screen.blit(weather_image, (image_x, image_y))
        screen.blit(city_text, (city_text_x, city_text_y))

    # Display error message if weather retrieval fails
    if currentgame_state == weather and show_fail == True and show_weather == False:
        screen.blit(error_text, (error_x, error_y))

    # Display "Saved!" message if weather is saved as default location
    if currentgame_state == weather and show == True:
        screen.blit(saved_text, (1040, 107))

          
    # Update the screen
    pygame.display.flip()

# Quit the game
pygame.quit()