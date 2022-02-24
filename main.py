from tkinter import *
import calendar
from tkinter import ttk
import ttkthemes
import requests
import datetime
from numpy.core.defchararray import capitalize


def main():
    window = ttkthemes.ThemedTk()
    window.set_theme('arc')
    window.geometry('720x450')  # sets window size

    title = ttk.Label(window, text='Weather App', padding=5)
    title.config(font=25)
    title.place(x=360, y=15, anchor=CENTER)
    specification = ttk.Label(window, text="Enter name of city:")  # title
    specification.place(x=360, y=40, anchor=CENTER)

    entry_box = ttk.Entry(justify=CENTER)  # creates a textbox that takes input
    entry_box.place(x=360, y=65, anchor=CENTER)

    cityLabel = ttk.Label(window)
    descLabel = ttk.Label(window)
    errorLabel = ttk.Label(window)

    def enter():
        if entry_box.get() == '':
            return
        if current_weather(entry_box.get()) == -1:
            errorLabel.config(text="Error, check spelling")
            errorLabel.place(x=360, y=120, anchor=CENTER)
            return
        # retrieve data to be displayed
        errorLabel.config(text='')
        live_info = current_weather(entry_box.get())
        forecast_info = []
        for i in range(8):
            forecast_info.append(forecast(live_info[0], live_info[1], i))

        var = IntVar()

        def display_result():
            cityLabel.config(text=live_info[2] + ', ' + live_info[3], font=40)
            cityLabel.place(x=360, y=185, anchor=CENTER)
            if var.get() == 0:  # display today's information
                weatherLabel = ttk.Label(window, text=str(round(live_info[4])) + '° F')
                weatherLabel.config(font=40)
                weatherLabel.place(x=360, y=225, anchor=CENTER)
            else:
                weatherLabel = ttk.Label(window, text=str(forecast_info[var.get()][1]) + '° F')
                weatherLabel.config(font=40)
                weatherLabel.place(x=360, y=225, anchor=CENTER)
            descLabel.config(font=40, text=forecast_info[var.get()][2])
            descLabel.place(x=360, y=265, anchor=CENTER)

        # create radio buttons
        for i in range(8):
            if i == 0:
                rb = ttk.Radiobutton(window, text='Today', variable=var, value=i, width=90, command=display_result)
                rb.invoke()
                rb.place(x=0, y=400, anchor=W)
            else:
                rb = ttk.Radiobutton(window, text=forecast_info[i][0], variable=var, value=i, width=90,
                                     command=display_result)
                rb.place(x=(90 * i), y=400, anchor=W)

    entry_button = ttk.Button(text='Enter', command=enter)
    entry_button.place(x=360, y=95, anchor=CENTER)

    window.mainloop()


# gets weather information based coordinates, day is a number denoting day (0-7, 0 is today, 7 is a week from today)
def forecast(lon, lat, day):
    # request api and store in response object
    key = '659f52603f1d61f0fa69fca33ef77167'
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts' \
          '&appid={key}&units=imperial'.format(
        lat=lat, lon=lon, key=key)
    response = requests.get(url)
    if response.status_code == 404:
        return -1
    # retrieve needed data
    day_in_week = calendar.day_name[
        datetime.datetime.fromtimestamp(int(response.json().get('daily')[day].get('dt'))).weekday()]
    weather = round(response.json().get('daily')[day].get('temp').get('day'))
    description = capitalize(response.json().get('daily')[day].get('weather')[0].get('description'))
    return day_in_week, weather, description


# returns the coordinates of a city based off city name
def current_weather(city_name):
    key = '659f52603f1d61f0fa69fca33ef77167'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + key + "&q=" + city_name + "&units=imperial"
    response = requests.get(complete_url)
    if response.status_code == 404:
        return -1
    lon = response.json().get('coord').get('lon')
    lat = response.json().get('coord').get('lat')
    city = response.json().get('name')
    country = response.json().get('sys').get('country')
    live_weather = response.json().get('main').get('temp')
    return str(lon), str(lat), city, country, live_weather


if __name__ == "__main__":
    main()
