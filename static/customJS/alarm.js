$(document).ready(function() {
    // Initialize Select2 for processId, labels, and areas
    $('#processId, #labels, #areas').select2({
        placeholder: "Select options",
        allowClear: true,
        width: "100%"
    });

    function updateLotIdOptions() {
        const selectedProcessIds = $('#processId').val();
        const selectedLabels = $('#labels').val();

        if (selectedProcessIds.length > 0 && selectedLabels.length > 0) {
            fetch(`/get_lot_ids?${new URLSearchParams({
                process_ids: selectedProcessIds,
                labels: selectedLabels
            })}`)
            .then(response => response.json())
            .then(data => {
                $('#lotid').empty();
                data.lot_ids.forEach(function(lotId) {
                    $('#lotid').append(new Option(lotId, lotId));
                });
            })
            .catch(error => console.error('Error fetching lot IDs:', error));
        }
    }

    function updateGrids() {
        const selectedAreas = $('#areas').val();

        // Clear existing grids
        $('#grids-container').empty();

        if (selectedAreas.length > 0) {
            selectedAreas.forEach(area => {
                // Create a container for each grid
                const gridDiv = document.createElement('div');
                gridDiv.classList.add('ag-theme-alpine');
                gridDiv.style.height = '200px';
                gridDiv.style.width = '100%';
                gridDiv.style.marginBottom = '20px';
                $('#grids-container').append(gridDiv);

                // Fetch data for the selected area
                fetch(`/get_area_data?${new URLSearchParams({area: area})}`)
                .then(response => response.json())
                .then(data => {
                    new agGrid.Grid(gridDiv, {
                        columnDefs: data.columnDefs,
                        rowData: data.rowData,
                        defaultColDef: {
                            sortable: true,
                            filter: true,
                            resizable: true
                        }
                    });
                })
                .catch(error => console.error('Error fetching area data:', error));
            });
        }
    }

    $('#processId, #labels').on('change', function() {
        updateLotIdOptions();
    });

    $('#areas').on('change', function() {
        updateGrids();
    });
});
