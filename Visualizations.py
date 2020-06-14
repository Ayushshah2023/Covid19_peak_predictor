import pandas as pd
import io
import requests
import pylab
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import plotly.graph_objects as go


def writeCategorical(df):
    with open('categorical.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['country', 'date', 'total','new'])
        cols = list(df.columns.values)
        for index, row in df.iterrows():
            counter = 0
            for val in row:
                newdate = datetime.strptime(df.columns[counter],
                                            '%m/%d/%y').strftime('%y-%m-%d')
                if(counter > 0 and counter+1 <= len(row)):
                    val2 = val - row[counter-1]
                else:
                    val2 = val
                filewriter.writerow([index, newdate, val,val2])
                counter += 1
    start_plot(cols[0], cols[len(cols) - 1])


def start_plot(start_date, end_date):
    dataset = pd.read_csv("categorical.csv")
    dates = pd.date_range(start_date, end_date).strftime('%y-%m-%d').tolist()
    countries = []
    for country in dataset["country"]:
        if country not in countries:
            countries.append(country)
    fig_dict = {"data": [], "layout": {}, "frames": []}

    fig_dict["layout"]["yaxis"] = {
        "range": [0, 20000],
        "title": "New Cases Each Week"
    }
    fig_dict["layout"]["xaxis"] = {
        "title": "Confirmed Cases",
        "range": [0, 200000]
    }
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["sliders"] = {
        "args": ["transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }],
        "initialValue": dates[0],
        "plotlycommand": "animate",
        "values": dates,
        "visible": True
    }
    

    fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }]



    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Date:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    date = '20-01-22'
    for country in countries:
        dataset_by_date = dataset[dataset["date"] == date]
        dataset_by_date_and_cont = dataset_by_date[
            dataset_by_date["country"] == country]

        data_dict = {
            "x": list(dataset_by_date_and_cont["total"]),
            "y": list(dataset_by_date_and_cont["new"]),
            "type":"scatter",
            "mode": "markers",
            "marker": {
             "size": 12
            },
            "fill": 'toself',
            "line": {"simplify": False},
            "name": country
        }
        fig_dict["data"].append(data_dict)

    for date in dates:
        frame = {"data": [], "name": str(date)}
        for country in countries:
            dataset_by_year = dataset[dataset["date"] == date]
            dataset_by_year_and_cont = dataset_by_year[
                dataset_by_year["country"] == country]

            data_dict = {
                "x": list(dataset_by_year_and_cont["total"]),
                "y": list(dataset_by_year_and_cont["new"]),
                "type":"scatter",
                "mode": "markers",
                "marker": {
                    "size": 12
                },
                "fill": 'toself',
                "line": {"simplify": False},
                "name": country
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [date],
            {"frame": {"duration": 300, "redraw": True},
            "mode": "immediate",
            "transition": {"duration": 300}}
        ],
            "label": date,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)

    fig.show()


def main():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    s = requests.get(url).content
    c = pd.read_csv(io.StringIO(s.decode('utf-8')))
    c.head()
    c.drop(columns=['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
    c = c.rename(columns={"Country/Region": "Country"})
    c = c.groupby(["Country"]).sum()
    writeCategorical(c)


if __name__ == "__main__":
    main()
