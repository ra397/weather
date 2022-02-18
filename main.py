from tkinter import *
import requests


def main():
    window = Tk(className='Weather App')  # main window
    window.geometry('250x250')  # sets window size

    title = Label(text="Enter name of city:")  # title
    title.pack(ipadx=500, ipady=10)  # add title to top

    entry_box = Entry(justify=CENTER)  # creates a textbox that takes input
    entry_box.pack()

    # outputs
    city_label = Label(window, text='')
    weather_label = Label(window, text='')
    description_label = Label(window, text='')

    def submit():
        # print current day information below enter button
        string = entry_box.get()
        if get_coordinates(string) == -1:
            # outputs
            city_label.configure(text='City not found, check spelling')
        else:
            coordinates = get_coordinates(string)
            city_label.configure(text=coordinates[2] + ', ' + coordinates[3])
            degree_f = get_info(coordinates[0], coordinates[1], 0)
            weather_label.configure(text=str(round(degree_f[0])) + "° F")
            description_label.configure(text=degree_f[1].capitalize())

        city_label.pack()
        weather_label.pack()
        description_label.pack()

    entry_button = Button(text='Enter', command=submit)
    entry_button.pack()

    window.mainloop()


# gets weather information based coordinates, day is a number denoting day (0 is today, 1 is tomorrow)
def get_info(lon, lat, day):
    key = '659f52603f1d61f0fa69fca33ef77167'
    base_url = "http://api.openweathermap.org/data/2.5/onecall?"
    complete_url = base_url + "lat=" + lat + "&lon=" + lon + "&exclude=minutely,hourly,alerts,current" \
                   + "&appid=" + key + "&units=imperial"
    response = requests.get(complete_url)
    if response.status_code == 404:
        return -1
    fahrenheit = response.json().get('daily')[day].get('temp').get('day')
    description = response.json().get('daily')[day].get('weather')[0].get('description')
    return fahrenheit, description


# returns the coordinates of a city based off city name
def get_coordinates(city_name):
    key = '659f52603f1d61f0fa69fca33ef77167'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + key + "&q=" + city_name
    response = requests.get(complete_url)
    if response.status_code == 404:
        return -1
    lon = response.json().get('coord').get('lon')
    lat = response.json().get('coord').get('lat')
    city = response.json().get('name')
    country = response.json().get('sys').get('country')
    return str(lon), str(lat), city, country


if __name__ == "__main__":
    main()
