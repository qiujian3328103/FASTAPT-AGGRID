// Declare gridOptions and gridApi globally
var gridOptions, gridApi;

function colorCellRenderer(params) {
    var div = document.createElement('div');
    div.style.backgroundColor = params.value;
    div.style.width = '36px';
    div.style.height = '36px';
    div.style.cursor = 'pointer';
    div.style.position = 'relative';
    div.style.border = '2px solid black'; // Add border with black color

    div.addEventListener('click', function(event) {
        var input = document.createElement('input');
        input.type = 'color';
        input.value = params.value;

        // Ensure the input appears at the cursor position
        input.style.position = 'absolute';
        input.style.left = event.pageX + 'px';
        input.style.top = event.pageY + 'px';
        input.style.opacity = '0';
        input.style.zIndex = '1000'; // Ensure it appears above other elements

        input.addEventListener('input', function(e) {
            params.setValue(e.target.value);
        });

        document.body.appendChild(input);
        input.click();
        input.addEventListener('blur', function() {
            document.body.removeChild(input);
        });
    });

    return div;
}

function submitButtonRenderer(params) {
    var button = document.createElement('button');
    button.innerText = 'Submit';
    button.className = 'btn btn-primary btn-sm'; // Add 'btn-sm' for smaller button
    button.addEventListener('click', function() {
        var updatedData = params.data;
        fetch('/update_color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Color updated successfully');
            } else {
                alert('Failed to update color');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    return button;
}

document.addEventListener('DOMContentLoaded', function() {
    var columnDefs = [
        { headerName: "Process ID", field: "process_id" },
        { headerName: "Bin", field: "bin" },
        { headerName: "Bin Group", field: "bin_group" },
        {
            headerName: "Color",
            field: "color",
            cellRenderer: colorCellRenderer,
            editable: true,
            width: 50,
        },
        {
            headerName: "Action",
            field: "action",
            cellRenderer: submitButtonRenderer,
            editable: false
        }
    ];

    gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,
        defaultColDef: {
            flex: 1,
            filter: "agTextColumnFilter",
        },
        onCellValueChanged: function(event) {
            console.log('Data after change is', event.data);
        }
    };

    var gridDiv = document.querySelector('#ag-grid-color');
    gridApi = agGrid.createGrid(gridDiv, gridOptions);
});

// Handle form submission
document.getElementById('dataForm_search_color').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = {process_id: $('#dataForm_search_color #inputSettingColor').val()}
    fetch('/filter_color', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        gridApi.setRowData(data);
    })
    .catch(error => console.error('Error:', error));
});