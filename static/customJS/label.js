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
        // Fill the form with data when the edit button is clicked
        document.getElementById('inputRootLotId').value = data.lot_id;
        document.getElementById('inputWaferId').value = data.wafer_id;
        document.getElementById('inputYield').value = data.yield;
        document.getElementById('inputFailBins').value = data.fail_bin;
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
        {headerName: "Lot ID", field: "lot_id"},
        {headerName: "Wafer ID", field: "wafer_id"},
        {headerName: "Yield", field: "yield"},
        {headerName: "Fail Bins", field: "fail_bin"},
        {headerName: "SWLY Label", field: "swly_label"},
        {
            headerName: "Edit",
            field: "edit",
            cellRenderer: EditButtonComponent,
        }
    ];
    console.log(columnDefs);  // Check if it's defined as expected


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