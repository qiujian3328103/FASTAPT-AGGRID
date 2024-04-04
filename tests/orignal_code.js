
        // Declare gridOptions globally
        var gridOptions;

        document.addEventListener('DOMContentLoaded', function() {
            // Register the render_image component by name
            gridOptions = {
                columnDefs: {{ columnDefs | safe }},
                rowData: {{ rowData | safe }},
                // Register the render_image component by name
                components: {
                    render_image: render_image
                },
                // Set the row height to accommodate the entire image
                getRowHeight: function(params) {
                    // Adjust the row height based on the image height
                    return 80; // Set a fixed row height here
                },
                // Set column widths
                defaultColDef: {
                    width: 100 // Set a default width for columns
                },
                // Define cell renderer for "lot_id" column
                onCellClicked: function(event) {
                    // Check if the clicked cell is in the "lot_id" column
                    if (event.column.colId === 'lot_id') {
                        // Extract the row data
                        var rowData = event.data;
                        // Construct the URL with query parameters
                        var url = '/detail_page?lot_id=' + rowData.lot_id + '&wafer_id=' + rowData.wafer_id;
                        //var url = '/detail_page/' + rowData.lot_id + '?wafer_id=' + rowData.wafer_id;
                        // Redirect to the detail page with selected row data
                        window.location.href = url;
                    }
                }
            };

            var gridDiv = document.querySelector('#ag-grid');
            new agGrid.Grid(gridDiv, gridOptions);
        });

        // Define the render_image component
        var render_image = function(params) {
            const imageHtml = `<img src="${params.value}" width="80" height="80">`;
            return imageHtml;
        };

