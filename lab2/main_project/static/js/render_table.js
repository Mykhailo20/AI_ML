function renderTable(fuzzySet, precision) {
    var table = document.querySelector('.matrics-table');

    // If the table doesn't exist, create a new one
    if (!table) {
        table = document.createElement('table');
        table.classList.add('matrics-table');

        // Append the table to its container element
        var container = document.querySelector('.form-container');
        container.appendChild(table);
    }

    // Clear the existing table content
    table.innerHTML = '';

    // Define the number of columns
    var colsNo = fuzzySet.parameter_values.length + 1;

    // Create and append the table header
    table.innerHTML += '<tr class="matrics-table__row">'
                       + '<th colspan=' + colsNo + ' class="matrics-table__th">Матриця попарних порівнянь</th>'
                       + '</tr>'

    // Create and append the empty row
    var emptyRowStr = '<tr class="matrics-table__row">'
    for(var i = 0; i < colsNo; i++){
        emptyRowStr += '<td class="matrics-table__td"></td>'
    }
    table.innerHTML += emptyRowStr;

    // Parameter values
    var parameterValuesStr = '<tr class="matrics-table__row">';
    parameterValuesStr += '<td class="matrics-table__td matrics-table__parameter">'
                          + '<input type="text" name="parameter_name_td_input" id="parameter_name_td_input" value="' 
                          + fuzzySet.parameter_name + '">'
                          + '</td>';
    fuzzySet.parameter_values.forEach(element => {
        parameterValuesStr += '<td class="matrics-table__td matrics-table__parameter">'
                              +  '<input type="text" name="parameter_value_td_input" value="' + element + '">'
                              + '</td>';
    });
    parameterValuesStr += '</tr>';
    table.innerHTML += parameterValuesStr;

    // Matrix A
    var matrixAStr = '';
    var matrixARowStr;
    for(var i = 0; i < fuzzySet.n; i++){
        matrixAStr += '<tr class="matrics-table__row">';
        matrixAStr += '<td class="matrics-table__td matrics-table__parameter">'
                      + fuzzySet.parameter_values[i]
                      + '</td>';

        matrixARowStr = '';
        for(var j = 0; j < fuzzySet.A[i].length; j++){
            matrixARowStr += '<td class="matrics-table__td">';
            if(i != (fuzzySet.n- 1)) {
                matrixARowStr += fuzzySet.A[i][j].toFixed(precision);
            } else {
                matrixARowStr += '<input type="text" name="expert_evaluation_td_input" value="' + fuzzySet.A[i][j].toFixed(precision) + '">';
            }
            matrixARowStr += '</td>';
        }
        matrixAStr += matrixARowStr;
        matrixAStr += '</tr>';
    }
    table.innerHTML += matrixAStr;

    // Additional rows
    var columnSumsStr = '<tr class="matrics-table__row">';
    columnSumsStr += '<td class="matrics-table__td">1</td>';
    fuzzySet.column_sums.forEach(element => {
        columnSumsStr += '<td class="matrics-table__td">';
        columnSumsStr += element.toFixed(precision);
        columnSumsStr += '</td>';
    });
    columnSumsStr += '</tr>';
    table.innerHTML += columnSumsStr;

    var columInvertedSumsStr = '<tr class="matrics-table__row">';
    columInvertedSumsStr += '<td class="matrics-table__td">2</td>'
    fuzzySet.inverted_sums.forEach(element => {
        columInvertedSumsStr += '<td class="matrics-table__td">'
        columInvertedSumsStr += element.toFixed(precision)
        columInvertedSumsStr += '</td>'
    })
    columInvertedSumsStr += '</tr>'
    table.innerHTML += columInvertedSumsStr;

    var columnMembFuncStr = '<tr class="matrics-table__row">'
    columnMembFuncStr += '<td class="matrics-table__td">M(X)</td>'
    fuzzySet.membership_function.forEach(element => {
        columnMembFuncStr += '<td class="matrics-table__td">'
        columnMembFuncStr += element.toFixed(precision)
        columnMembFuncStr += '</td>'
    })
    columnMembFuncStr += '</tr>'
    table.innerHTML += columnMembFuncStr;
}