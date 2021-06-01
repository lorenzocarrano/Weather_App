from tkinter import *
from API_key import *
from PIL import ImageTk, Image
import requests
import json
import matplotlib.pyplot as plt
from json_analysis import *
import numpy as np

root = Tk()
root.title("Meteo")
root.geometry("329x95")
root.configure(background="light blue")


def show_graphic(api, query):
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, api['cnt'], api['cnt']), collect_data(api, query))
    ax.set_title(query.get())
    plt.show()


def actual_forecast():
    try:
        api_request = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=" + city.get() + "&appid=5950c6d8f2501af205f9e8945a398a49")

    except Exception as e:
        api = "Error"
    else:
        api = api_request.json()

        Window1 = Toplevel()
        Window1.title(city.get() + ": Real-Time Weather")
        Window1.geometry("600x400")
        temperature_frame = LabelFrame(Window1, text="Temperature(°C)", font=("Helvetica", 10), padx=10, pady=10)
        temperature_frame.grid(row=2, column=0, padx=30, pady=10)
        main_informations_frame = LabelFrame(Window1, text="General", font=("Helvetica", 10))
        main_informations_frame.grid(row=2, column=1, padx=30, pady=10)

        state = Label(main_informations_frame, text=api["sys"]["country"])
        prov = Label(main_informations_frame, text=api["name"])
        wheater = Label(main_informations_frame, text=api["weather"][0]['description'])
        hum = Label(main_informations_frame, text="Humidity: " + str(api["main"]['humidity']))
        press = Label(main_informations_frame, text="Pressure: " + str(api["main"]['pressure']) + 'mbar')
        temp = Label(temperature_frame, text="Temperature: " + str(int(api["main"]["temp"]) - 273))
        temp_min = Label(temperature_frame, text="min: " + str(int(api["main"]["temp_min"]) - 273))
        temp_max = Label(temperature_frame, text="max: " + str(int(api["main"]["temp_max"]) - 273))
        temp_percepita = Label(temperature_frame, text="Percepita: " + str(int(api["main"]["feels_like"]) - 273))

        state.grid(row=0, column=0)
        prov.grid(row=0, column=1)
        wheater.grid(row=1, column=0)
        hum.grid(row=2, column=0)
        press.grid(row=2, column=1)
        temp.grid(row=2, column=0)
        temp_min.grid(row=2, column=0)
        temp_max.grid(row=2, column=1)
        temp_percepita.grid(row=3, column=0)


def next_five_days_forecast():
    try:
        api_request = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" + city.get() + "&appid=" + Key)
    except Exception as e:
        api = "Error"
    else:
        api = api_request.json()
        Window2 = Toplevel()
        Window2.title(city.get() + ": Next 5 days forecast")
        Window2.geometry("1300x600")

        frame_clmn = 0
        lbl_row = 0
        i = 0
        # el(api)
        while i < api["cnt"] - 1:

            actual_day, actual_month, actual_year = get_dmy(api, i)

            day_frame = LabelFrame(Window2, text=actual_day + "/" + actual_month + "/" + actual_year,
                                   font=("Helvetica", 10))
            day_frame.grid(row=0, column=frame_clmn)
            frame_clmn += 1
            while api["list"][i]["dt_txt"][8:10] == actual_day and i < api["cnt"]:
                lbl = Label(day_frame, text=get_time(api, i, mode='hm') + ": Temperatura°C: " + str(
                    round(api["list"][i]["main"]["feels_like"] - 273))
                                            + "; " + get_weather_description(api, i), font=("Helvetica", 12))
                lbl.grid(row=lbl_row)
                lbl_row += 1
                i += 1
                if i == api["cnt"]:
                    break
            lbl_row = 0

        query_options = [
            "Temperatura percepita",
            "Temperatura minima",
            "Temperatura massima",
            "Pressione",
            "Umidita'"
        ]
        query = StringVar()
        query.set(query_options[0])
        query_menu = OptionMenu(Window2, query, *query_options)
        query_menu.grid(row=lbl_row + 1, column=1)
        graphic_btn = Button(Window2, text="Show Graphic", command=lambda: show_graphic(api, query))
        graphic_btn.grid(row=lbl_row + 1, column=0)


city = Entry(root)
city.grid(row=0, column=0, padx=20, pady=10, columnspan=5)
actual_btn = Button(root, text="Real-Time forecast", padx=20, pady=10, command=actual_forecast)
actual_btn.grid(row=1, column=0)
next_days_btn = Button(text="Next 5 days forecast", padx=10, pady=10, command=next_five_days_forecast)
next_days_btn.grid(row=1, column=1)

root.mainloop()
