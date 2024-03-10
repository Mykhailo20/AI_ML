// Function to handle adding a new row and input to a table
function addNewRow(tableId, parameterName, newValue, maxRowCells, maxParameterValues) {
    var table = document.querySelector('#' + tableId + ' tbody');
    var lastRow = table.lastElementChild;
    var lastRowInputsCount = lastRow.querySelectorAll('input[name="' + parameterName + '_td"]').length;

    // If the number of inputs reaches max_row_cells, create a new row
    if (lastRowInputsCount >= maxRowCells) {
        // Create a new row
        var newRow = document.createElement('tr');
        newRow.classList.add('data-table__row');
        
        var newCell = document.createElement('td');  // Since the first cell is labeled 'Введені значення'
        newCell.classList.add('data-table__td');
        newRow.appendChild(newCell);
        table.appendChild(newRow);
        lastRow = newRow;  // Update lastRow to point to the newly created row
    }

    // Create a new cell and input element
    var newCell = document.createElement('td');
    newCell.classList.add('data-table__td');
    var newInput = document.createElement('input');
    newInput.setAttribute('type', 'text');
    newInput.setAttribute('name', parameterName + '_td');
    newInput.setAttribute('value', newValue);
    newCell.appendChild(newInput);
    lastRow.appendChild(newCell);

    // Check if the number of inputs is max_parameter_values and disable the button if true
    var inputsCount = table.querySelectorAll('input[name="' + parameterName + '_td"]').length;
    if (inputsCount >= maxParameterValues) {
        document.getElementById('add-' + parameterName.replace('_', '-') + '-btn').disabled = true;
    }
}