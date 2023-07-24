import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle

app = dash.Dash(__name__)

# initial empty DataFrame
# initial DataFrame with a dummy row
df = pd.DataFrame(
        [{'#': '1', 
          'Title': 'Template Title', 
          'Content': 'Template Content', 
          'Keywords': 'Template Keyword'}])

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i, 'editable': True} for i in df.columns],
        data=df.to_dict('records'),
        style_data={'backgroundColor': 'rgb(255, 255, 255)'}
        ),
    html.Div(id='button-container'),
    html.Button('Add Row', id='add-button'),
    html.Button('Load CSV', id='load-button'),
    html.Button('Save CSV', id='save-button'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
        )
    ])

def get_keywords(rows):
    keywords = []
    for row in rows:
        if row['Keywords'] != 'Template':
            keywords.extend(row['Keywords'].split(', '))
    return list(set(keywords))

@app.callback(
        Output('table', 'data'),
        Output('table', 'columns'),
        Output('button-container', 'children'),
        Input('add-button', 'n_clicks'),
        Input('load-button', 'n_clicks'),
        Input('save-button', 'n_clicks'),
        Input({'type': 'keyword-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
        Input('table', 'data'),
        Input('interval-component', 'n_intervals'),
        State('table', 'data_previous'),
        State('table', 'columns'),
        )

def update_table(
        add_n, 
        load_n, 
        save_n, 
        keyword_n, 
        current_data, 
        n_intervals, 
        old_data, 
        columns):

    ctx = dash.callback_context
    if not ctx.triggered:
        if not old_data:
            df = pd.DataFrame(
                    data = [{'#': '1',
                             'Title': 'Template Title',
                             'Content': 'Template Content',
                             'Keywords': 'Template Keyword'}]
                    )
        old_data = df.to_dict('records')
        columns=[{"name": i, "id": i, 'editable': True} for i in df.columns]
        return old_data, columns, dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'add-button' in button_id:
        df = pd.DataFrame(old_data) 
        df = df.append(
                pd.DataFrame(
                    data = [{'#': '1',
                             'Title': 'Template Title',
                             'Content': 'Template Content',
                             'Keywords': 'Template Keyword'}]
                    )
                )
        columns=[{"name": i, "id": i, 'editable': True} for i in df.columns]
        return df.to_dict('records'), columns, dash.no_update

    elif 'load-button' in button_id:
        df = pd.read_pickle('output.pkl')
        keywords = get_keywords(df.to_dict('records'))
        buttons = [html.Button(k, id={'type': 'keyword-button', 'index': k}) for k in keywords]
        columns=[{"name": i, "id": i, 'editable': True} for i in df.columns]
        # Save the keywords set to a pickle file
        with open('keywords.pkl', 'wb') as f:
            pickle.dump(set(keywords), f)
        return df.to_dict('records'), columns, buttons

    elif 'save-button' in button_id:
        df = pd.DataFrame(old_data)
        df.to_pickle('output.pkl')  # Save the dataframe as a pickle file
        return old_data, columns, dash.no_update

    elif 'keyword-button' in button_id:
        if old_data:
            selected_keyword = eval(button_id)['index']
            for row in old_data:
                if row['Keywords'] == 'Template':
                    row['Keywords'] = selected_keyword
                else:
                    row['Keywords'] += ', ' + selected_keyword
        return old_data, columns, dash.no_update

    else:
        # The table is updated when a change is made or the interval passes
        keywords = get_keywords(current_data)
        buttons = [html.Button(k, id={'type': 'keyword-button', 'index': k}) for k in keywords]
        return current_data, columns, buttons

if __name__ == '__main__':
    app.run_server(debug=True)

