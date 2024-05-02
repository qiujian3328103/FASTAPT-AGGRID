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