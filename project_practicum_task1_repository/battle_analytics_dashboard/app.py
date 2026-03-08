
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

characters = pd.read_csv("data/characters.csv")
actions = pd.read_csv("data/actions.csv")
dice = pd.read_csv("data/dice_rolls.csv")
encounters = pd.read_csv("data/encounters.csv")

app = dash.Dash(__name__)
server = app.server

class_distribution = characters["class"].value_counts().reset_index()
class_distribution.columns = ["class", "count"]

avg_damage = actions.groupby("character")["damage"].mean().reset_index()

dice_distribution = dice["result"]

action_frequency = actions["action"].value_counts().reset_index()
action_frequency.columns = ["action", "count"]

fig_classes = px.pie(class_distribution, names="class", values="count")

fig_damage = px.bar(
    avg_damage,
    x="character",
    y="damage",
    title="Средний урон персонажей"
)

fig_dice = px.histogram(
    dice_distribution,
    nbins=20,
    title="Распределение бросков кубов"
)

fig_actions = px.bar(
    action_frequency,
    x="action",
    y="count",
    title="Частота действий"
)

app.layout = html.Div([

    html.H1("Панель аналитики боевых событий"),

    html.Div([

        html.Div([
            dcc.Graph(figure=fig_classes)
        ], className="card"),

        html.Div([
            dcc.Graph(figure=fig_damage)
        ], className="card")

    ], className="row"),

    html.Div([

        html.Div([
            dcc.Graph(figure=fig_dice)
        ], className="card"),

        html.Div([
            dcc.Graph(figure=fig_actions)
        ], className="card")

    ], className="row"),

    html.H2("Журнал столкновений"),

    dcc.Dropdown(
        id="encounter-filter",
        options=[{"label": i, "value": i} for i in encounters["result"].unique()],
        placeholder="Выберите результат столкновения"
    ),

    html.Div(id="table-container")

])


@app.callback(
    Output("table-container", "children"),
    Input("encounter-filter", "value")
)
def update_table(value):

    if value:
        filtered = encounters[encounters["result"] == value]
    else:
        filtered = encounters

    return html.Table([

        html.Thead(html.Tr([html.Th(col) for col in filtered.columns])),

        html.Tbody([
            html.Tr([
                html.Td(filtered.iloc[i][col]) for col in filtered.columns
            ])
            for i in range(len(filtered))
        ])

    ])


if __name__ == "__main__":
    app.run(debug=True)
