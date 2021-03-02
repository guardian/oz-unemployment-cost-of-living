import pandas as pd 
import os
from yachtCharter import yachtCharter

## GET INDEXED FIGURE FOR UNEMPLOYMENT BENEFITS

data_path = os.path.dirname(__file__)
ub_data = f'{data_path}/data/unemploymentsicknessandbenefits.xlsx'

ub_df = pd.read_excel(ub_data)
ub_df = ub_df[['Date of effect', '21 years']]
ub_df = ub_df.dropna()

ub_df['Date of effect'] = pd.to_datetime(ub_df['Date of effect'])

ub_hundert = ub_df.loc[ub_df['Date of effect'] == '20/9/2011']['21 years'].values

ub_df['ub_index'] = (ub_df['21 years']/ub_hundert)*100

ub_df = ub_df[['Date of effect', "ub_index"]]

# ub_df = ub_df.rename(columns={'Date of effect':"Date", "ub_index": "value", "21 years": "Weekly UB"})
ub_df = ub_df.rename(columns={'Date of effect':"Date", "ub_index": "UB Index for singles over 21"})

ub_df['UB Index for singles over 21'] = pd.to_numeric(ub_df['UB Index for singles over 21'])

# ub_df['variable'] = "UB Index for singles over 21"
### GET SELECT CPI NUMBERS

index_cv = f'{data_path}/data/CPI_All_Time_Series/640105.xls'
in_df = pd.read_excel(index_cv, sheet_name="Data1")

nammo = [('Unnamed: 0', "Date"), ("Index Numbers ;  Rents ;  Australia ;", "Rent"), ("Index Numbers ;  Milk ;  Australia ;", "Milk"), 
("Index Numbers ;  Fruit ;  Australia ;", "Fruit"), ("Index Numbers ;  Vegetables ;  Australia ;", "Vegetables"),
("Index Numbers ;  Snacks and confectionery ;  Australia ;", "Snacks"), ("Index Numbers ;  Garments ;  Australia ;", "Garments")]

speci = [x[0] for x in nammo]
short_names = [x[1] for x in nammo]

in_df = in_df[speci ]

in_df = in_df[9:]

for thing in nammo:
    in_df.rename(columns={thing[0]:thing[1]}, inplace=True)

in_df["Date"] = pd.to_datetime(in_df['Date'])

ub_pivot = pd.melt(ub_df, id_vars="Date", value_vars="UB Index for singles over 21")

in_pivot = pd.melt(in_df, id_vars = "Date", value_vars = short_names[1:])



combined = pd.concat([ub_pivot, in_pivot])

import datetime 
cutoff_date = datetime.date(1985, 1, 1)
combined = combined.loc[combined['Date'] > datetime.datetime.combine(cutoff_date, datetime.datetime.min.time())]

pivoted = combined.pivot(index="Date", columns="variable", values="value").reset_index()
pivoted['Date'] = pivoted['Date'].dt.strftime('%Y-%m-%d')

def makeTestingLine(df):
	
    template = [
            {
                "title": "Growth in Jobseeker/unemployment benefit compared to selected CPI items",
                "subtitle": "Unemployment benefits have been indexed at 100 in 2011",
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
                "margin-right": "10"
            }
        ]
    key = []
    periods = []
    labels = []

    df.fillna("", inplace=True)
    chartData = df.to_dict('records')

    yachtCharter(template=template, data=chartData, chartId=[{"type":"linechart"}], labels=labels,
    options=[{"colorScheme":"guardian", "lineLabelling":"TRUE"}], chartName="ub-selected_cpi")

makeTestingLine(pivoted)


