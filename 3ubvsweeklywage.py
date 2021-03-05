import pandas as pd 
from yachtCharter import yachtCharter
import os

data_path = os.path.dirname(__file__)


## UNEMPLOYMENT BENEFIT

ub_data = f'{data_path}/data/unemploymentsicknessandbenefits.xlsx'

ub_df = pd.read_excel(ub_data)
ub_df = ub_df[['Date of effect', '21 years']]
ub_df = ub_df.dropna()

ub_df['Date of effect'] = pd.to_datetime(ub_df['Date of effect'])

ub_hundert = ub_df.loc[ub_df['Date of effect'] == '20/9/2011']['21 years'].values

ub_df['ub_index'] = (ub_df['21 years']/ub_hundert)*100

# ub_df = ub_df[['Date of effect', "ub_index"]]

# ub_df = ub_df.rename(columns={'Date of effect':"Date", "ub_index": "value", "21 years": "Weekly UB"})
ub_df = ub_df.rename(columns={'Date of effect':"Date", "21 years": "value"})

ub_df["variable"] = "Jobseeker"

ub_df['value'] = pd.to_numeric(ub_df['value'])

ub_df = ub_df[['Date', 'value', 'variable']]

## WEEKLY EARNINGS

ww_data = f'{data_path}/data/6302003.xls'
ww_df = pd.read_excel(ww_data, sheet_name=1)

ww_df = ww_df[['Unnamed: 0', "Earnings; Persons; Full Time; Adult; Ordinary time earnings ;"]]
ww_df = ww_df[9:]

ww_df = ww_df.rename(columns={'Unnamed: 0': "Date", "Earnings; Persons; Full Time; Adult; Ordinary time earnings ;": "value"})
ww_df["variable"] = "Weekly earnings"

ww_df['value'] = pd.to_numeric(ww_df['value'])

combined = pd.concat([ub_df, ww_df])

import datetime 
cutoff_date = datetime.date(1995, 1, 1)
# cutoff_date = cutoff_date.strftime()
combined = combined.loc[combined['Date'] > datetime.datetime.combine(cutoff_date, datetime.datetime.min.time())]

pivoted = combined.pivot(index="Date", columns="variable", values="value").reset_index()
pivoted['Date'] = pivoted['Date'].dt.strftime('%Y-%m-%d')
print(pivoted)

def makeTestingLine(df):
	
    template = [
            {
                "title": "How jobseeker compares to weekly earnings over time",
                "subtitle": "Australian average weekly earnings and jobseeker for singles over 21",
                "footnote": "",
                "source": "Australian Bureau of Statistics, Department of Social Services",
                "dateFormat": "%Y-%m-%d",
                "yScaleType":"",
                "xAxisLabel": "Date",
                "yAxisLabel": "AUD$ per week",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10",
                "breaks": "no"
            }
        ]
    key = []
    periods = []
    labels = []

    df.fillna("", inplace=True)
    chartData = df.to_dict('records')

    yachtCharter(template=template, data=chartData, chartId=[{"type":"linechart"}], labels=labels,
    options=[{"colorScheme":"guardian", "lineLabelling":"TRUE"}], chartName="ub-vs-weekly")

makeTestingLine(pivoted)