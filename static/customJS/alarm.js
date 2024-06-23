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

    $('#processId, #labels').on('change', function() {
        updateLotIdOptions();
    });
});
