class EditButtonComponent {
    constructor() {
        this.eGui = document.createElement("div");
        this.eButton = document.createElement("button");
        this.eButton.className = "btn btn-primary";
        this.eButton.innerText = "Edit";
        this.eButton.style.padding = '5px 10px';
        this.eButton.style.fontSize = '12px';
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
        console.log("Edit Data:", data);
        // Open the modal and populate the form
        $('#editModal').modal('show');
        // Populate the form fields with the data from the row
        $('#editForm #processId').val(data.process_id);
        $('#editForm #layer').val(data.layer);
        $('#editForm #bins').val(data.bin_lst);
        $('#editForm #signature').val(data.signature);
        $('#editForm #name').val(data.name);
        $('#editForm #desc').val(data.desc);
        $('#editForm #tool').val(data.tool);
        $('#editForm #user').val(data.user);
        $('#editForm #type').val(data.type);
        // Populate other fields similarly
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        return true;
    }

    destroy() {
        this.eButton.removeEventListener("click", this.eventListener);
    }
}

class DeleteButtonComponent {
    constructor() {
        this.eGui = document.createElement("div");
        this.eButton = document.createElement("button");
        this.eButton.className = "btn btn-danger";
        this.eButton.innerText = "Delete";
        this.eButton.style.padding = '5px 10px';
        this.eButton.style.fontSize = '12px';
        this.eGui.appendChild(this.eButton);
    }

    init(params) {
        this.params = params;
        this.eButton.onclick = () => {
            this.showDeleteModal(this.params.data);
        };
    }

    showDeleteModal(data) {
        $('#deleteModal').modal('show');
        $('#confirmDelete').off('click').on('click', () => this.deleteRow(data));
    }

    deleteRow(data) {
        fetch(`/delete_row/${data.process_id}/${data.name}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) throw new Error('Failed to delete the item');
                return response.json();
            })
            .then(result => {
                console.log('Success:', result);
                $('#deleteModal').modal('hide');
                reloadData();  // Refresh the grid to reflect the deletion
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        return true;
    }

    destroy() {
        this.eButton.removeEventListener("click", this.onclick);
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

// reload the ag-grid data after refresh. 
function reloadData() {
    fetch('/swly_list_reload')  // Adjust the URL if needed to point to the endpoint that returns the full data set
        .then(response => response.json())
        .then(data => {
            console.log(data);
            gridApi.setGridOption("rowData", data);
        })
        .catch(error => console.error('Error loading the data:', error));
}


// send the data to fastapi to process 
function submitEditForm() {
    var formData = {
        process_id: $('#editForm #processId').val(),
        layer: $('#editForm #layer').val(),
        bins: $('#editForm #bins').val(),
        signature: $('#editForm #signature').val(),
        tool: $('#editForm #tool').val(),
        user: $('#editForm #type').val(),
        type: $('#editForm #layer').val(),
        name: $('#editForm #name').val(),
        desc: $('#editForm #desc').val(),
        // Include other fields as necessary
    };

    // Send the data to the server using fetch or jQuery's ajax method
    fetch(`/edit_row/${formData.process_id}/${formData.name}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    }).then(response => response.json())
      .then(data => {
          console.log('Success:', data);
          $('#editModal').modal('hide');
          reloadData();
          // Optionally refresh the grid or handle UI update
      }).catch(error => {
          console.error('Error:', error);
      });
}


document.addEventListener('DOMContentLoaded', function() {
    columnDefs = [
        {
            headerName: "Edit",
            field: "edit",
            cellRenderer: EditButtonComponent,
        },
        {
            headerName: "Delete",
            field: "delete",
            cellRenderer: DeleteButtonComponent,
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

    var gridDiv = document.querySelector('#ag-grid-list');
    gridApi = agGrid.createGrid(gridDiv, gridOptions);
});
