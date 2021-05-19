import asyncio
import datetime
import numpy as np
import aiohttp
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


links = ["https://api.apify.com/v2/key-value-stores/yaPbKe9e5Et61bl7W/records/LATEST?disableRedirect=true", "https://api.apify.com/v2/datasets/suHgi59tSfu02VsRO/items?limit=16&desc=true"]
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for l in links:
            task = asyncio.ensure_future(get_data(l, session))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    return data

async def get_data(link, session):
    async with session.get(link) as response:
        result_data = await response.json()
        return result_data

data = asyncio.get_event_loop().run_until_complete(main())

result = data[0]
date = result['lastUpdatedAtApify']
newdate = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")    
result['lastUpdatedAtApify'] = str(newdate)

newresult = data[1]
newresult.reverse()
def map_func(dictionary):
    dictionary["date"] = str(datetime.datetime.strptime(dictionary['lastUpdatedAtApify'], "%Y-%m-%dT%H:%M:%S.000Z").date())
    return dictionary
newresult = list(map(map_func, newresult))
infections = list(np.diff(list(map(lambda x: x['infected'], newresult))))
infections.insert(0,0)
counter = 0
for d in newresult:
    d["communityCases"] = infections[counter]
    counter += 1

latest = result
historical = newresult
external_stylesheets = [
{
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
### CSS inline styling ###
bodyMain = {
    "backgroundImage" : "url(./assets/covid.jpg)",
    "backgroundSize" : "cover",
    "backgroundRepeat" : "no-repeat",
    "margin" : "-8px",
    "height" : "100vh",
    "overflowX" : "hidden",
}

sectionMain = {
    "width" : "100vw",
    "textAlign" : "center",
    "position" : "relative",
    "top" : "30vh",
    "left" : "0vw",
}

textStyleMain = {
    "fontSize" : "3vw",
    "color" : "White",
}

DescStyleMain = {
    "fontSize" : "2vw",
    "color" : "White",
}

hrStyle = {
    "borderColor" : "White",
    "width" : "16vw",
}

aStyleMain = {
    "display" : "inline",
    "position" : "relative",
    "top" : "55vh",
    "left" : "44vw",
    "fontSize" : "2vw",
    "color" : "White",
    "width" : "16vw",
    "height" : "16vh"
}

graphStylesOdd = {
    "height" : "50vh",
    "width" : "70vw",
    "marginLeft": "30vw",
    "backgroundColor":"#d5d8dd"
}

textStyleGraphsOdd = {
    "height": "50vh",
    "width":"30vw",
    "color" : "White",
    "textAlign" : "center",
    "backgroundColor":"#264f5c",
    "float":"left",
    "fontSize": "2.5vw"
}

graphStylesEven = {
    "height" : "50vh",
    "width" : "70vw",
    "backgroundColor":"#e2dcd1",
    "float":"left"
}

textStyleGraphsEven = {
    "height": "50vh",
    "width":"30vw",
    "color" : "White",
    "textAlign" : "center",
    "backgroundColor":"#006f7a",
    "fontSize": "2.5vw",
    "marginLeft":"70vw"
}

### Main Graphs ###
df = pd.DataFrame(historical)
infectionRate = px.line(
    data_frame=df[1:],
    x="date",
    y="communityCases",
    labels={"date":"Date", "communityCases":"Number of New Cases"},
)

infectionRate.update_layout({
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_size' : 20,
    'xaxis' : {
        'tickformat':'%d %B'
    }
})

activeCases = px.line(
    data_frame=df,
    x='date',
    y='activeCases',
    labels={"date":"Date", "activeCases":"Number of active Cases"}
)

activeCases.update_layout({
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_size' : 20,
    'xaxis' : {
        'tickformat':'%d %B'
    }
})

activeCasesBreakdown = px.bar(
    data_frame=df,
    x="date",
    y=["inCommunityFacilites", "stableHospitalized", "criticalHospitalized"],
    labels={"date":"Date", "value":"Number of cases"},
    barmode='group'
)

activeCasesBreakdown.update_layout({
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_size' : 20,
    'xaxis' : {
        'tickformat':'%d %B',
    }
})

labels = ['Discharged', 'Active Cases', 'Deceased']
values = [latest['discharged'], latest['activeCases'], latest['deceased']]
casesBreakdown = go.Figure(data=[go.Pie(labels=labels, values=values)])

casesBreakdown.update_layout({
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_size' : 20,
})

### Main HTML ###
app.layout = html.Div(children=[
    html.Div(children=[
        html.Section(children=[
            html.Hr(style=hrStyle), 
            html.B("COV-INFO", style=textStyleMain), 
            html.Hr(style=hrStyle), 
            html.P("A COMPREHENSIVE VISUAL ON THE COVID-19 SITUATION IN SINGAPORE", style=DescStyleMain),
            html.P(f"LAST UPDATED: {latest['lastUpdatedAtApify']}", style=DescStyleMain)
            ], style=sectionMain),
        html.Div(html.A("Learn More", href="#daily-covid-cases", style={"textDecoration" : "none", "color" : "white"}, id="aMain"), style=aStyleMain)
    ], style=bodyMain),
    html.Div(children=[
        html.Section(children=[
            html.Span(children=["Infected", html.Br(), html.Br(), html.Span(f"{latest['infected']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["Discharged", html.Br(), html.Br(), html.Span(f"{latest['discharged']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["Quarantined", html.Br(), html.Br(), html.Span(f"{latest['inCommunityFacilites']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["Hospitalised (Stable)", html.Br(), html.Br(), html.Span(f"{latest['stableHospitalized']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["Hospitalised (Critical)", html.Br(), html.Br(), html.Span(f"{latest['criticalHospitalized']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["Active Cases", html.Br(), html.Br(), html.Span(f"{latest['activeCases']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["Deceased", html.Br(), html.Br(), html.Span(f"{latest['deceased']}", className="resultOverallStats")], className="overallStats"),
            html.Span(children=["New Cases", html.Br(), html.Br(), html.Span(f"{historical[-1]['communityCases']}", className="resultOverallStats")], className="overallStats")
        ], style={"display" : "flex", "justifyContent" : "center", "alignItems" : "center", "flexWrap" : "wrap", "height" : "100vh", "width":"100vw"}),
    ], style={"height" : "100vh", "margin" : "8px -8px -8px -8px", "backgroundColor" : "#21b2a6", "overflowX" : "hidden",}, id="daily-covid-cases"),
    html.Div(children=[
        html.Div(children=[
            html.P("New Cases", style={"marginTop":"18vh", "marginBottom":"0", }),
            html.P("This chart shows the number of new infections", style={"fontSize": "1.5vw"}),
        ], style=textStyleGraphsOdd),
        dcc.Graph(figure=infectionRate, id="infectionRate", style=graphStylesOdd, config={'displayModeBar': False})
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Div(children=[
        dcc.Graph(figure=activeCases, id="activeCases", style=graphStylesEven, config={'displayModeBar': False}),
        html.Div(children=[
            html.P("Active Case", style={"marginTop":"18vh", "marginBottom":"0", "display":"inline-block"}),
            html.P("This chart shows the number of active covid cases", style={"fontSize": "1.5vw", "marginRight":"1vw"}),
        ], style=textStyleGraphsEven),
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Div(children=[
        html.Div(children=[
            html.P("Active Cases Breakdown", style={"marginTop":"18vh", "marginBottom":"0", }),
            html.P("This chart shows the Breakdown of the current active cases", style={"fontSize": "1.5vw"}),
        ], style=textStyleGraphsOdd),
        dcc.Graph(figure=activeCasesBreakdown, id="activeCasesBreakdown", style=graphStylesOdd, config={'displayModeBar': False})
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Div(children=[
        dcc.Graph(figure=casesBreakdown, id="casesBreakdown", style=graphStylesEven, config={'displayModeBar': False}),
        html.Div(children=[
            html.P("Total Cases Breakdown", style={"marginTop":"18vh", "marginBottom":"0", "display":"inline-block"}),
            html.P("This chart shows the breakdown of all found covid cases", style={"fontSize": "1.5vw", "marginRight":"1vw"}),
        ], style=textStyleGraphsEven),
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Footer(children=[
        html.P(children=[
            html.P(children=[
                html.A(className="fab fa-github", href="https://github.com/Jcheez"),
                html.A(className="fab fa-linkedin", href="https://www.linkedin.com/in/jcheez/"),
                html.A(className="far fa-window-maximize", href="https://resume-199e6.firebaseapp.com/")
            ]),
            "© JCHEEZ | INFO: ",
            html.A(" APIFY", href="https://apify.com/tugkan/covid-sg", style={"color":"#8f9193"}, target="_blank"),
            " | IMAGES: ",
            html.A("FLAT ICON", href="https://www.flaticon.com/", style={"color":"#8f9193"}, target="_blank"),
        ], style={"color":"#8f9193", "fontSize":"1.5vw", "marginTop":"7vh",})
    ],style={"height" : "20vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden", "backgroundColor":"#192819", "textAlign":"center"})
])

if __name__ == '__main__':
    app.run_server(debug=True)