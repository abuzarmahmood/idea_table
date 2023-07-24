import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import pickle

app = dash.Dash(__name__)

df = pd.DataFrame(columns=['#', 'Title', 'Content', 'Keywords'])
df.loc[0] = ['1', 'Template Title', 'Template Content', 'Template Keyword']

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i, 'editable': True} for i in df.columns],
        data=df.to_dict('records'),
        style_data={'backgroundColor': 'rgb(255, 255, 255)',
						'whiteSpace': 'normal',
						'height': 'auto',
					},
					style_cell={
						'whiteSpace': 'normal',
						'height': 'auto',
					},
        editable=True,
		style_cell_conditional=[
				{'if': {'column_id': '#'},
				 'width': '10%'},
				{'if': {'column_id': 'Title'},
				 'width': '30%'},
				{'if': {'column_id': 'Content'},
				 'width': '30%'},
				{'if': {'column_id': 'Keywords'},
				 'width': '30%'},
			],
    ),
    html.Div(id='button-container'),
    html.Button('Add Row', id='edit-button', n_clicks=0),
    html.Button('Load CSV', id='load-button', n_clicks=0),
    html.Button('Save CSV', id='save-button', n_clicks=0),
])

def get_keywords(rows):
    keywords = []
    for row in rows:
        if row['Keywords'] != 'Template':
            keywords.extend(row['Keywords'].split(', '))
    return list(set(keywords))

@app.callback(
    [Output('table', 'data'),
     Output('table', 'columns'),
     Output('button-container', 'children')],
    [Input('edit-button', 'n_clicks'),
     Input('load-button', 'n_clicks'),
     Input('save-button', 'n_clicks'),
     Input({'type': 'keyword-button', 'index': ALL}, 'n_clicks')],
    [State('table', 'data'),
     State('table', 'columns'),
     State('table', 'selected_cells')]
)
def update_table(edit_n, load_n, save_n, keyword_n, current_data, columns, selected_cells):
    ctx = dash.callback_context
    if not ctx.triggered or not current_data:
        return current_data, columns, dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'edit-button':
        current_data.append({'#': str(len(current_data) + 1), 'Title': 'Template', 'Content': 'Template', 'Keywords': 'Template'})
        columns = [{"name": i, "id": i, 'editable': True} for i in current_data[0].keys()]
    
    elif button_id == 'load-button':
        df = pd.read_pickle('output.pkl')
        current_data = df.to_dict('records')
        columns = [{"name": i, "id": i, 'editable': True} for i in df.columns]
    
    elif button_id == 'save-button':
        df = pd.DataFrame(current_data)
        df.to_pickle('output.pkl')

    elif 'keyword-button' in button_id:
        selected_keyword = eval(button_id)['index']
        if selected_cells:
            for cell in selected_cells:
                row, column = cell['row'], cell['column']
                current_data[row]['Keywords'] += ', ' + selected_keyword

    keywords = get_keywords(current_data)
    buttons = [html.Button(k, id={'type': 'keyword-button', 'index': k}) for k in keywords]
    return current_data, columns, buttons


if __name__ == '__main__':
    app.run_server(debug=True)

