import tkinter as tk                # Needs to be pip installed and imported before running
from PIL import ImageTk, Image      #
from tkinter import font            #
import requests                     #
from io import BytesIO              #
                         

# Here is the url's that this application use to get information.

main_api = 'https://restcountries.eu/rest/v2/name/'
flag_api = 'https://www.countryflags.io/'

# Size of the canvas

HEIGHT = 600
WIDTH = 700

# This is the main function, that makes the whole program to work. It's called when the 'button' is pressed. 

def capital_city(entry):
    url = main_api + entry  # This gets the user input and inserts it into the url.
    json_data = requests.get(url).json() # This is the request part, where this program calls the API for information.
    response = json_data # Response from json_data.
    
    label['text'] = format_response(response) # This sets the label 'text' sections content, which in this case is defined in subfunction called 'response()'.
    flag = image(entry) # Sets content(image) of the flag, defined in subfunction called 'image()'. 
    panel.image = flag # This is only for reference to python, so it won't delete the flag image.
    panel['image'] = flag # This tells panel to use flag as an image.

# This is first subfunction, that sets the content that we get from the countries.

def format_response(response):
    try: # Try to get the information asked from the API.
        name = (response[0]['name']) # Name of the country (Info got from the API set in the capital_city(entry)).
        capital = (response[0]['capital']) # Capital city of the country (Info got from the API set in the capital_city(entry)).
        currency_name = (response[0]['currencies'][0]['name']) # Currency (name) of the country (Info got from the API set in the capital_city(entry)).
        currency_symbol = (response[0]['currencies'][0]['symbol']) # Currency (symbol) of the country (Info got from the API set in the capital_city(entry)).
        borders = (response[0]['borders']) # Border countries of the country (Info got from the API set in the capital_city(entry)).
        borderlist = [] # Made lists to handle data got from 'borders', so it's easier to handle.
        borderlist2 = [] #
        borderlist3 = [] #
        population = (response[0]['population']) # Population of the country (Info got from the API set in the capital_city(entry)).
        
        # For loop, for getting every border country from the 'borders', then appending each one to the borderlist.
        
        for x in borders:
            borderlist.append(x)
        
        # Setting some rules, how the information is shown.
        # Basically just split borderlists, if there is more than 8 border countries, so It's been shown beautifully.

        if 11 > len(borderlist) >= 9:
            length = str(len(borderlist))
            borderlist2 = borderlist[:5].copy()
            borderlist3 = borderlist[5:].copy()
            borderlist2 = ', '.join(map(str, borderlist2)) # This edits the output, to show without brackets.
            borderlist3 = ', '.join(map(str, borderlist3)) #
           #label['font'] = ('Courier', 11)     <---- Uncommand if you are using smaller HEIGHT and WIDTH for the canvas. You can also set your own font type and resize text.

        if 13 > len(borderlist) > 11:
            length = str(len(borderlist))
            borderlist2 = borderlist[:6].copy()
            borderlist3 = borderlist[6:].copy()
            borderlist2 = ', '.join(map(str, borderlist2)) #
            borderlist3 = ', '.join(map(str, borderlist3)) #
            #label['font'] = ('Courier', 11)      <---- Uncommand if you are using smaller HEIGHT and WIDTH for the canvas. You can also set your own font type and resize text.
           
        if 20 > len(borderlist) > 13:
            length = str(len(borderlist))
            borderlist2 = borderlist[:7].copy()
            borderlist3 = borderlist[7:].copy()
            borderlist2 = ', '.join(map(str, borderlist2)) #
            borderlist3 = ', '.join(map(str, borderlist3)) #
            #label['font'] = ('Courier', 11)    <---- Uncommand if you are using smaller HEIGHT and WIDTH for the canvas. You can also set your own font type and resize text.
                   
        if len(borderlist) <= 8:
            length = str(len(borderlist))
            borderlist2 = borderlist[:8].copy()
            borderlist2 = ', '.join(map(str, borderlist)) #
            borderlist3 = '' # If borderlist length is less or exactly 8, leave the borderlist3 empty.
            
        full_string = 'Country: %s \nCapital: %s \nPopulation: %s \nCurrency: %s( %s )  \nBorders: %s\n%s\n%s' % (name, capital, population, currency_name, currency_symbol, length, borderlist2, borderlist3)
        
    except: # If there was a miss spelling or country was not found, text result is telling that to the user.
        full_string = 'There was a porblem \n requesting your country info, \nplease check spelling.'
 
    return full_string # At the end returns full_string, that is used as a content of the labels text section.

# This is second subfunction that is used to get flag image.

def image(entry):
    try: # Try to get the flag image.
        url = main_api + entry # This gets the user input and inserts it into the url.
        json_data = requests.get(url).json() # This is the request part, where this program calls the API for information.
        response = json_data # Response from json_data.
        countryCode = (response[0]['alpha2Code']) # Country code of the country, that is used in the flag apis url. (Info got from the API set in the capital_city(entry)).

        url2 = flag_api + countryCode + '/flat/64.png' # This gets the Country code and inserts it into the url.
        response2 = requests.get(url2) # This is the request part, where this program calls the API for information.
        raw_img_data = response2.content # Raw content from response2.
        img_data = Image.open(BytesIO(raw_img_data)) # Open the content using BytesIO, so it's written in memory buffer.
        img = ImageTk.PhotoImage(img_data) # Using the BytesIO data to get the image. 

        
    except: # If there is some errors or flag is not existing, it returns empty image.
        img = '' 

        
    return img # Returns the flag image.
    

# Creating basic tkiner root canvas, that is filled with background image, frame, entry label, button, lower frame, label and panel.

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = ImageTk.PhotoImage(Image.open('images/earth.jpg')) # Replace 'earth.jpg' with your own picture or other image path and you get your own background image.
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#8c8c8c', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=('Courier', 12), bg='#000000', fg='white')
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text='Get info', font=('Courier', 12), bg='#8c8c8c', command=lambda: capital_city(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = tk.Frame(root, bg='#8c8c8c', bd=10)
lower_frame.place(relx=0.5,rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font=('Courier', 13), bg='#000000', fg='white', width = 200, relief = 'solid', justify = 'center') # You can change font type and resize text with changing the values of 'font'.
label.place(relwidth=1, relheight=1)

panel = tk.Label(lower_frame, bg = '#000000', height = 100)
panel.pack(side="bottom",expand="no")


root.mainloop()       
    



