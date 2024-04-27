class EditButtonComponent {
    constructor() {
        this.eGui = document.createElement("div");
        this.eButton = document.createElement("button");
        this.eButton.className = "btn btn-primary"; // Bootstrap button for styling
        this.eButton.innerText = "Edit";
        this.eButton.style.padding = '5px 10px'; // Smaller padding
        this.eButton.style.fontSize = '12px'; // Smaller font size
        this.eGui.appendChild(this.eButton);
    }

    init(params) {
        this.params = params;
        this.eventListener = () => {
            this.editRow(this.params.data);
        };
        this.eButton.addEventListener("click", this.eventListener);
    }

    editRow(data) {
        console.log("*************")
        console.log(data);
        // Fill the form with data when the edit button is clicked
        document.getElementById('inputProcessId').value = data.process_id;
        document.getElementById('inputLayer').value = data.layer;
        document.getElementById('inputBins').value = data.bin_lst;
        document.getElementById('inputSignature').value = data.signature;
        document.getElementById('inputUser').value = data.user;
        document.getElementById('inputSWLYName').value = data.name;
        document.getElementById('inputSWLYDesc').value = data.desc;
        document.getElementById('inputTool').value = data.tool;
        document.getElementById('inputType').value = data.type;
        // Add more fields as necessary
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        // Optional: Update button properties or data if needed
        return true;
    }

    destroy() {
        // Clean up event listeners when the button is removed from the grid
        this.eButton.removeEventListener("click", this.eventListener);
    }
}


// Declare gridOptions and gridApi globally
var gridOptions, gridApi;
var columnDefs; 

// Define the render_image component
var render_image = function(params) {
    return `<img src="${params.value}" width="80" height="80">`;
};

// Custom comparator function for date fields
var dateComparator = function(filterLocalDateAtMidnight, cellValue) {
    var dateParts = cellValue.split('/');
    var cellDate = new Date(Number(dateParts[2]), Number(dateParts[1]) - 1, Number(dateParts[0]));
    return cellDate - filterLocalDateAtMidnight;
};


document.addEventListener('DOMContentLoaded', function() {
    columnDefs = [
        {
            headerName: "Edit",
            field: "edit",
            cellRenderer: EditButtonComponent,
        },
        {"headerName": "process_id", "field": "process_id"},
        {"headerName": "Layer", "field": "layer"},
        {"headerName": "EQP", "field": "tool"},
        {"headerName": "Bins", "field": "bin_lst"},
        {"headerName": "Signature", "field": "signature"},
        {"headerName": "Type", "field": "type"},
        {"headerName": "SWLY_Name", "field": "name"},
        {"headerName": "Desc", "field": "desc"},
        {"headerName": "User", "field": "user"},
        {"headerName": "Last Update", "field": "last_update"},

    ];
    gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,
        defaultColDef: {
            flex: 1,
            minWidth: 100,
            filter: "agTextColumnFilter",
            filterParams: {
                comparator: dateComparator
            },
            menuTabs: ["filterMenuTab"],
        },
    };

    var gridDiv = document.querySelector('#ag-grid-label');
    gridApi = agGrid.createGrid(gridDiv, gridOptions);
});

$(document).ready(function() {
    // Initialize Select2
    $('.select2').select2({
        placeholder: "Select process IDs",
        allowClear: true,
    });
})

$("#submit_swly_list").submit(function (e) {
    e.preventDefault();

    var formData = new FormData(this);
    console.log(formData);
    $.ajax({
        url: "/submit_swly_list_data",
        type: "POST",
        data: formData, 
        contentType: false, 
        processData: false,
        success: function (response) {
            if (gridApi) {
                gridApi.setRowData(response.rowData);
            }
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText); // Log response text which might contain useful error messages
        }
    });
});