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
            minWidth: 80,
            maxWidth:100,
            cellStyle: { 'padding': 0, border: '1px solid'},
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

    var gridDiv = document.querySelector('#ag-grid');
    gridApi = agGrid.createGrid(gridDiv, gridOptions);
});

$(document).ready(function() {
    // Initialize Select2
    $('.select2').select2({
        placeholder: "Select process IDs",
        allowClear: true,
    });
    console.log("loaded");
    // Configure Toastr
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-left",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "500",
        "timeOut": "1000",
        "extendedTimeOut": "500",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    // Form submission handling
    $('#dataForm').submit(function(e) {
        e.preventDefault();
        console.log('Form submission intercepted');  // Debugging line
    
        toastr.info('Processing...');
        var formData = new FormData(this);
    
        $.ajax({
            url: '/form_submit',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log('Response received', response);  // Confirm the structure of the response
                if (gridApi) {
                    // Assuming `setGridOption` is correct; if not, check the documentation or try the alternative
                    gridApi.setGridOption('rowData', response.rowData);
                    toastr.success('Data loaded successfully');
                } else {
                    console.error('gridApi is not defined');
                    toastr.error('Grid API not available');
                }
            },
            error: function(xhr, status, error) {
                console.error("Error in AJAX request: " + status + " - " + error);
                toastr.error('An error occurred');
            }
        });
    });
    
});


$(function(){
    $("#startDate").datepicker({
        dateFormat: 'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        yearRange: '2010:2025'
    });
    // Show the datepicker when the calendar icon is clicked
    $("#startDatepicker .input-group-text").on('click', function() {
        $("#startDate").datepicker("show");
    });
});