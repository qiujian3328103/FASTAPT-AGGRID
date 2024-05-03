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
        document.getElementById('username').value = data.user_id;
        document.getElementById('first_name').value = data.first_name;
        document.getElementById('last_name').value = data.last_name;
        document.getElementById('email').value = data.email;
        document.getElementById('role').value = data.auth;
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

function submitEditForm() {
    var formData = {
        user_id: $('#dataForm_user_create #username').val(),
        first_name: $('#dataForm_user_create #first_name').val(),
        last_name: $('#dataForm_user_create #last_name').val(),
        email: $('#dataForm_user_create #email').val(),
        auth: $('#dataForm_user_create #role').val(),
        // Include other fields as necessary
    };

    // Send the data to the server using fetch or jQuery's ajax method
    fetch(`/edit_admin/${formData.user_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    }).then(response => response.json()).then(data => {
          console.log('Success:', data);
        //   $('#editModal').modal('hide');
          reloadData();
          // Optionally refresh the grid or handle UI update
      }).catch(error => {
          console.error('Error:', error);
      });
}


// Handle form submission to prevent default action
document.getElementById('dataForm_user_create').addEventListener('submit', function(event) {
    event.preventDefault();  // This stops the page from refreshing
    submitEditForm();
});

function reloadData() {
    fetch('/admin_reload')
        .then(response => response.json())
        .then(data => {
            gridApi.setRowData(data);
        })
        .catch(error => console.error('Error loading the data:', error));
}

// Declare gridOptions and gridApi globally
var gridOptions, gridApi;
var columnDefs; 

document.addEventListener('DOMContentLoaded', function() {
    columnDefs = [
        {
            headerName: "Edit",
            field: "edit",
            cellRenderer: EditButtonComponent,
        },
        {headerName: "Username", field: "user_id"},
        {headerName: "First Name", field: "first_name"},
        {headerName: "Last Name", field: "last_name"},
        {headerName: "Email", field: "email"},
        {headerName: "Role", field: "auth"},
        {headerName: "Last Updated", field: "last_update"}
    ];

    gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,
        defaultColDef: {
            sortable: true,
            filter: true
        },
    };

    // Setup the grid after the page has finished loading
    var gridDiv = document.querySelector('#ag-grid-account');
    gridApi = agGrid.createGrid(gridDiv, gridOptions);
});