query_vocabulary = {
        "Temperatura percepita": "feels_like",
        "Temperatura minima": "temp_min",
        "Temperatura massima": "temp_max",
        "Pressione": "pressure",
        "Umidita'": "humidity"
    }

def get_dmy(api, i):
    actual_day = api["list"][i]["dt_txt"][8:10]
    actual_month = api["list"][i]["dt_txt"][5:7]
    actual_year = api["list"][i]["dt_txt"][0:4]
    return actual_day, actual_month, actual_year


def get_time(api, i, mode='hms'):
    if mode == 'hms':
        return api["list"][i]["dt_txt"][11:]
    elif mode == 'hm':
        return api["list"][i]["dt_txt"][11:16]
    elif mode == 'h':
        return api["list"][i]["dt_txt"][11:13]
    elif mode == 'm':
        return api["list"][i]["dt_txt"][14:16]
    elif mode == 's':
        return api["list"][i]["dt_txt"][17:]


def get_weather_description(api, i):
    return api["list"][i]["weather"][0]["description"]


def collect_data(api, query):
    v = []
    for i in range(api["cnt"]):
        v.append(round(api["list"][i]["main"][query_vocabulary[query.get()]] - 273))

    return v


