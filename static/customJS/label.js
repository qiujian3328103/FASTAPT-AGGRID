console.log('Script loaded');
// Declare gridOptions and gridApi globally
var gridOptions, gridApi;

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
        components: {
            render_image: render_image
        },
        getRowHeight: function(params) {
            return 80; // Set a fixed row height
        },
        onCellClicked: function(event) {
            if (event.column.colId === 'lot_id') {
                var url = '/detail_page?lot_id=' + event.data.lot_id + '&wafer_id=' + event.data.wafer_id;
                window.open(url, '_blank');
            } else if (event.column.colId === 'wafer_id') {
                var url = '/lot_review?lot_id=' + event.data.lot_id + '&wafer_id=' + event.data.wafer_id;
                window.location.href = url;
            }
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