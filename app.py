import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Header import Header
from dash_html_components.I import I
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from parallel import result as latest
from parallel import twoWeeks as historical
from parallel import oneMonth as historical2
from parallel import latestStatsComparison as lsc

external_stylesheets = [
{
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="COV-INFO")
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

iconStyle = {
    "color":"white"
}

### Main Graphs ###
labels = ['Discharged', 'Active Cases', 'Deceased']
values = [latest['discharged'], latest['activeCases'], latest['deceased']]
casesBreakdown = go.Figure(data=[go.Pie(labels=labels, values=values)])

casesBreakdown.update_layout({
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_size' : 20,
})

### Conditional rendering of icons
childs = []

for item in lsc.values():
    if item == 0:
        childs.append([
            html.Span(className="fas fa-equals",style={"color":"white", "paddingRight": "0.5vw"}),
            item
        ])
    elif item > 0:
        childs.append([
            html.Span(className="fa fa-arrow-circle-up", style={"color":"white", "paddingRight": "0.5vw"}),
            item
        ])
    elif item < 0:
        childs.append([
            html.Span(className="fa fa-arrow-circle-down", style={"color":"white", "paddingRight": "0.5vw"}),
            item
        ])

### Main HTML ###
app.layout = html.Div(children=[
    html.Div(children=[
        html.Section(children=[
            html.Hr(style=hrStyle), 
            html.B("COV-INFO", style=textStyleMain), 
            html.Hr(style=hrStyle), 
            html.P("A SIMPLE VISUAL ON THE COVID-19 SITUATION IN SINGAPORE", style=DescStyleMain),
            html.P(f"LAST UPDATED: {latest['lastUpdatedAtApify']}", style=DescStyleMain)
            ], style=sectionMain),
        html.Div(html.A("Learn More", href="#daily-covid-cases", style={"textDecoration" : "none", "color" : "white"}, id="aMain"), style=aStyleMain)
    ], style=bodyMain),
    html.Div(children=[
        html.Header("Latest Statistics", style={"color":"white", "fontSize": "3vw", "textAlign":"center", "height":"7vh", "marginTop":"3vh"}),
        html.Section(children=[
            html.Span(children=[
                "Infected",
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{latest['updatedInfected']}",
                    html.Span(children=childs[0], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "Discharged", 
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{latest['discharged']}",
                    html.Span(children=childs[1], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "Quarantined", 
                html.Br(), 
                html.Br(),
                html.Span(children=[
                    f"{latest['inCommunityFacilites']}",
                    html.Span(children=childs[2], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "Hospitalised (Stable)", 
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{latest['stableHospitalized']}",
                    html.Span(children=childs[3], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "Hospitalised (Critical)", 
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{latest['criticalHospitalized']}",
                    html.Span(children=childs[4], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "Active Cases", 
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{latest['updatedActive']}",
                    html.Span(children=childs[5], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "Deceased", 
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{latest['deceased']}",
                    html.Span(children=childs[6], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats"),
            html.Span(children=[
                "New Cases", 
                html.Br(), 
                html.Br(), 
                html.Span(children=[
                    f"{historical[-1]['communityCases']}",
                    html.Span(children=childs[10], style={"marginLeft": "2vw"})
                ], className="resultOverallStats"),
            ], className="overallStats")
        ], style={"display" : "flex", "justifyContent" : "center", "alignItems" : "center", "flexWrap" : "wrap", "height" : "90vh", "width":"100vw"}),
    ], style={"height" : "100vh", "margin" : "8px -8px -8px -8px", "backgroundColor" : "#21b2a6", "overflowX" : "hidden",}, id="daily-covid-cases"),
    html.Div(children=[
        html.Div(children=[
            html.P("New Cases", style={"marginTop":"17vh", "marginBottom":"0", }),
            html.P("This chart shows the number of new infections", style={"fontSize": "1.5vw"}),
            dcc.Dropdown(
                id="infectionRateDropdown", 
                options=[{'label':"2 weeks", 'value':"2 weeks"},{'label':"4 weeks", 'value':"4 weeks"}], 
                style={"color":"black", "cursor":"pointer","width":"14vw", "paddingLeft":"8vw", "fontSize":"1.5vw"},
                searchable=False,
                value='2 weeks'
            )
        ], style=textStyleGraphsOdd),
        dcc.Graph(id="infectionRate", style=graphStylesOdd, config={'displayModeBar': False})
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Div(children=[
        dcc.Graph(id="activeCases", style=graphStylesEven, config={'displayModeBar': False}),
        html.Div(children=[
            html.P("Active Cases", style={"marginTop":"17vh", "marginBottom":"0", "display":"inline-block"}),
            html.P("This chart shows the number of active covid cases", style={"fontSize": "1.5vw", "marginRight":"1vw"}),
            dcc.Dropdown(
                id="activeCasesDropdown", 
                options=[{'label':"2 weeks", 'value':"2 weeks"},{'label':"4 weeks", 'value':"4 weeks"}], 
                style={"color":"black", "cursor":"pointer","width":"14vw", "paddingLeft":"8vw", "fontSize":"1.5vw"},
                searchable=False,
                value='2 weeks'
            )
        ], style=textStyleGraphsEven),
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Div(children=[
        html.Div(children=[
            html.P("Active Cases Breakdown", style={"marginTop":"18vh", "marginBottom":"0", }),
            html.P("This chart shows the Breakdown of the current active cases", style={"fontSize": "1.5vw"}),
            dcc.Dropdown(
                id="activeCasesBreakdownDropdown", 
                options=[{'label':"2 weeks", 'value':'2 weeks'},{'label':"4 weeks", 'value':'4 weeks'}], 
                style={"color":"black", "cursor":"pointer","width":"14vw", "paddingLeft":"8vw", "fontSize":"1.5vw"},
                searchable=False,
                value='2 weeks'
            )
        ], style=textStyleGraphsOdd),
        dcc.Graph(id="activeCasesBreakdown", style=graphStylesOdd, config={'displayModeBar': False})
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Div(children=[
        dcc.Graph(figure=casesBreakdown, id="casesBreakdown", style=graphStylesEven, config={'displayModeBar': False}),
        html.Div(children=[
            html.P("Total Cases Breakdown", style={"marginTop":"18vh", "marginBottom":"0", "display":"inline-block"}),
            html.P("This chart shows the breakdown of all found covid cases", style={"fontSize": "1.5vw", "marginRight":"1vw"}),
        ], style=textStyleGraphsEven),
    ], style={"height" : "50vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden"}),
    html.Footer(children=[
        html.Div(children=[
            html.P(children=[
                html.A(className="fab fa-github", href="https://github.com/Jcheez", target="_blank"),
                html.A(className="fab fa-linkedin", href="https://www.linkedin.com/in/jcheez/", target="_blank"),
                html.A(className="far fa-window-maximize", href="https://resume-199e6.firebaseapp.com/", target="_blank")
            ]),
            "V2.3.235 | © JCHEEZ 2021 | INFO: ",
            html.A(" APIFY", href="https://apify.com/tugkan/covid-sg", style={"color":"#8f9193"}, target="_blank"),
            " | IMAGES: ",
            html.A("FLAT ICON", href="https://www.flaticon.com/", style={"color":"#8f9193"}, target="_blank"),
            html.P("Information displayed is meant for reference only, it can be slightly inaccurate due to update lags by MOH")
        ], style={"color":"#8f9193", "fontSize":"1vw", "marginTop":"5vh",})
    ],style={"height" : "20vh", "margin" : "8px -8px -8px -8px", "overflowX" : "hidden", "backgroundColor":"#192819", "textAlign":"center"})
])

### Callbacks ###
@app.callback(
    Output(component_id='infectionRate', component_property='figure'),
    Input(component_id='infectionRateDropdown', component_property='value')
)
def updateActiveCases(value):
    if value == "4 weeks":
        df = pd.DataFrame(historical2)[1:]
        infectionRate = px.line(
            data_frame=df,
            x='date',
            y='communityCases',
            labels={"date":"Date", "communityCases":"Number of new Cases"}
        )

        infectionRate.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_size' : 20,
            'xaxis' : {
                'tickformat':'%d %B'
            }
        })
        return infectionRate

    else:
        df = pd.DataFrame(historical)[1:]
        activeCases = px.line(
            data_frame=df,
            x='date',
            y='communityCases',
            labels={"date":"Date", "communityCases":"Number of active Cases"}
        )

        activeCases.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_size' : 20,
            'xaxis' : {
                'tickformat':'%d %B'
            }
        })
        return activeCases

@app.callback(
    Output(component_id='activeCases', component_property='figure'),
    Input(component_id='activeCasesDropdown', component_property='value')
)
def updateActiveCases(value):
    if value == "4 weeks":
        df = pd.DataFrame(historical2)
        activeCases = px.line(
            data_frame=df,
            x='date',
            y='updatedActive',
            labels={"date":"Date", "updatedActive":"Number of active Cases"}
        )

        activeCases.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_size' : 20,
            'xaxis' : {
                'tickformat':'%d %B'
            }
        })
        return activeCases

    else:
        df = pd.DataFrame(historical)
        activeCases = px.line(
            data_frame=df,
            x='date',
            y='updatedActive',
            labels={"date":"Date", "updatedActive":"Number of active Cases"}
        )

        activeCases.update_layout({
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_size' : 20,
            'xaxis' : {
                'tickformat':'%d %B'
            }
        })
        return activeCases

@app.callback(
    Output(component_id='activeCasesBreakdown', component_property='figure'),
    Input(component_id='activeCasesBreakdownDropdown', component_property='value')
)
def updateActiveCasesBreakdown(value):
    if value == "4 weeks":
        df = pd.DataFrame(historical2)
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
        return activeCasesBreakdown

    else:
        df = pd.DataFrame(historical)
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
        return activeCasesBreakdown

if __name__ == '__main__':
    app.run_server(debug=True)