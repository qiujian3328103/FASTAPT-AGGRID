import dash
from dash import html, Input, Output, State, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc
import uuid
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)

# Initialize the table data as an empty list
initial_data = []

# Define the layout
app.layout = html.Div([
    fac.AntdRow([
            # Custom CSS for hover shadow
        fac.AntdCol([
            fuc.FefferyDiv(
                'Mouse hover here and press Ctrl + V to paste an image',
                id='image-paste-container',  # Add id for hover effect
                shadow='hover-shadow',
                style={
                    'height': '200px',
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'borderRadius': '6px',
                    'border': '1px solid #f0f0f0',
                    'marginBottom': '10px',
                },
                className='hover-shadow'  # Add class for hover effect
            ),           
        ], span=3),
        fac.AntdCol([
            fac.AntdTable(
                id='image-table',
                columns=[
                    {'title': 'ID', 'dataIndex': 'id'},
                    {'title': 'Image', 'dataIndex': 'image', 'renderOptions': {'renderType': 'image'}},
                    {'title': 'Foreign Key', 'dataIndex': 'foreign_key'},
                    {'title': 'Type', 'dataIndex': 'type', 'renderOptions': {'renderType': 'select'}},
                    {'title': 'Delete', 'dataIndex': 'delete', 'renderOptions': {'renderType': 'button'}}
                ],
                data=initial_data,
                bordered=True,
                locale='en-us',
                maxHeight=200,
                pagination={'pageSize': 10, 'showSizeChanger': True, 'pageSizeOptions': [5, 10, 20]},
                style={'width': '100%'},
            ), 
        ], span=21),
    ]),
    fac.AntdButton("Save Table Data", id="save-button", type="primary", style={"marginTop": "10px"}), 
    dcc.Store(id='table-data-store', data={}),
    fuc.FefferyImagePaste(
        id='image-paste-demo',
        disabled=True
    ),
])

# Client-side callback to enable image pasting when hovering
app.clientside_callback(
    '''(isHovering) => !isHovering;''',
    Output('image-paste-demo', 'disabled'),
    Input('image-paste-container', 'isHovering')
)

# Client-side callback to handle pasted image and render it
app.clientside_callback(
    '''(imageInfo) => imageInfo.base64;''',
    Input('image-paste-demo', 'imageInfo'),
    prevent_initial_call=True
)

# Callback to update the table when an image is pasted
@app.callback(
    Output('image-table', 'data', allow_duplicate=True),
    Input('image-paste-demo', 'imageInfo'),
    State('image-table', 'data'),
    prevent_initial_call=True
)
def update_table(image_info, current_data):
    if not image_info:
        return initial_data
    image_base64 = image_info['base64']
    
    # Generate a unique ID and UUID for the image
    new_id = str(len(current_data) + 1)
    foreign_key = str(uuid.uuid4())
    
    new_row = {
        'id': new_id,
        'image': {'src': image_base64, 'height': '50px'},
        'foreign_key': foreign_key,
        'type': {
            'options': [
                {'label': 'Map', 'value': 'map'},
                {'label': 'Trend', 'value': 'trend'}
            ],
            'value': 'map',  # Default to 'map'
        },
        'delete': {
            'content': 'Delete',
            'type': 'primary',
            'danger': True,
        }
    }

    return current_data + [new_row]

# Callback for handling delete button in the table
@app.callback(
    Output('image-table', 'data', allow_duplicate=True),
    Input('image-table', 'nClicksButton'),
    [
        State('image-table', 'clickedContent'),
        State('image-table', 'recentlyButtonClickedRow'),
        State('image-table', 'data')
    ],
    prevent_initial_call=True
)
def handle_button_click(nClicksButton, clickedContent, recentlyButtonClickedRow, current_data):
    if clickedContent == 'Delete':
        # Find the row index using the ID
        row_id = recentlyButtonClickedRow['id']
        # Filter out the row with this ID
        updated_data = [row for row in current_data if row['id'] != row_id]
        return updated_data

    return current_data


# Callback to save the table data to dcc.Store
@app.callback(
    Output('table-data-store', 'data'),
    Input('save-button', 'nClicks'),
    State('image-table', 'data'),
    prevent_initial_call=True
)
def save_table_data(n_clicks, table_data):
    if n_clicks is None:
        raise PreventUpdate
    
    # Initialize the dictionary structure
    saved_data = {"map": {}, "trend": {}}
    
    # Iterate through the table data and organize it by type
    for row in table_data:
        row_type = row['type']['value']  # Get the current type (map or trend)
        foreign_key = row['foreign_key']
        image_data = row['image']['src']
        
        if row_type in saved_data:
            if foreign_key not in saved_data[row_type]:
                saved_data[row_type][foreign_key] = [image_data]
            else:
                saved_data[row_type][foreign_key].append(image_data)
    # print(saved_data)

    return saved_data


if __name__ == '__main__':
    app.run_server(debug=True)
