# -*- coding: utf-8 -*-

from yachtCharter import yachtCharter
import pandas as pd
import numpy as np
import requests
import simplejson as json


#%%


url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
print("Getting", url)
r = requests.get(url)
with open("data.csv", 'w') as f:
	f.write(r.text)		

#%%

df = pd.read_csv("data.csv")
df = df.set_index('date')

#%%
includes = ["Australia", "United States","United Kingdom","Italy","Spain", "Germany", "China", "Japan","Sweden", "South Korea", "Singapore","Vietnam"]

selected = df[df['location'].isin(includes)]

countries_new = selected[['location', 'new_cases_smoothed']].reset_index()

countries_new['new_cases_smoothed'] = countries_new['new_cases_smoothed'].round(1)
#%%

countries_new = countries_new.rename(columns={"date":"Date","location":"Country"})

#%%

def makeDailyCountryChart(df):
	
# 	lastUpdatedInt = df.date.iloc[-1]

	template = [
			{
				"title": "New Covid-19 cases per day for selected countries",
				"subtitle": "Showing the seven day rolling average of new confirmed cases. Each chart is scaled individually by default, to allow comparison of the shape of the epidemic curves",
				"footnote": "",
				"source": " | Source: <a href='https://ourworldindata.org/coronavirus' target='_blank'>ECDC data compiled by Our World in Data</a>",
				"dateFormat": "%Y-%m-%d",
				"xAxisLabel": "",
				"yAxisLabel": "Cumulative cases",
				"timeInterval":"day",
				"tooltip":"<strong>Date: </strong>{{#nicedate}}Date{{/nicedate}}<br/><strong>Cases: </strong>{{new_cases_smoothed}}",
				"periodDateFormat":"",
				"margin-left": "50",
				"margin-top": "5",
				"margin-bottom": "20",
				"margin-right": "25",
				"xAxisDateFormat": "%b %d"
			}
		]
	key = []
	periods = []
	options = [{"scaleBy":"individual", "chartType":"line"}]
	labels = []
	chartId = [{"type":"smallmultiples"}]
	df.fillna('', inplace=True)
	chartData = df.to_dict('records')

	yachtCharter(template=template, options=options, data=chartData, chartId=chartId, chartName="country-sm-covid-cases-2020")

makeDailyCountryChart(countries_new)

#%%

# includes2 = ["Australia","United Kingdom","Italy","Germany","Sweden", "France"]
# selected2 = df[df['location'].isin(includes2)]

# countries_new2 = selected2[['location', 'new_cases_smoothed_per_million']].reset_index()



# countries_new2['new_cases_smoothed_per_million'] = countries_new2['new_cases_smoothed_per_million'].round(1)

# countries_new2_pvt = countries_new2.pivot(index='date', columns='location', values='new_cases_smoothed_per_million')
# countries_new2_pvt = countries_new2_pvt.rename(columns={"date":"Date"})

#%%
def makeLineChart(df):

	template = [
			{
				"title": "New Covid-19 cases per day, per million people, for selected countries",
				"subtitle": "Showing the seven day rolling average of new confirmed cases per million people",
				"footnote": "",
				"source": "<a href='https://ourworldindata.org/coronavirus' target='_blank'>ECDC data compiled by Our World in Data</a>",
				"dateFormat": "%Y-%m-%d",
				"yScaleType":"",
				"xAxisLabel": "",
				"yAxisLabel": "",
				"minY": "",
				"maxY": "",
				"periodDateFormat":"",
				"margin-left": "50",
				"margin-top": "30",
				"margin-bottom": "20",
				"margin-right": "100"
			}
		]
	key = []
	periods = []
	labels = []
	chartId = [{"type":"linechart"}]
	df.fillna('', inplace=True)
	df = df.reset_index()
	chartData = df.to_dict('records')

	yachtCharter(template=template, data=chartData, chartId=[{"type":"linechart"}], chartName="clklklklk-covid-2020")

# makeLineChart(countries_new2_pvt["2020-03-01":])
