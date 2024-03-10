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

    var tableInnerHTMLStr = '';

    // Define the number of columns
    var colsNo = fuzzySet.parameter_values.length + 1;

    // Create and append the table header
    tableInnerHTMLStr += '<tr class="matrics-table__row">'
                       + '<th colspan=' + colsNo + ' class="matrics-table__th">Матриця попарних порівнянь</th>'
                       + '</tr>'

    // Create and append the empty row
    var emptyRowStr = '<tr class="matrics-table__row">'
    for(var i = 0; i < colsNo; i++){
        emptyRowStr += '<td class="matrics-table__td"></td>'
    }
    tableInnerHTMLStr += emptyRowStr;

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
    tableInnerHTMLStr += parameterValuesStr;

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
    tableInnerHTMLStr += matrixAStr;

    // Additional rows
    var columnSumsStr = '<tr class="matrics-table__row">';
    columnSumsStr += '<td class="matrics-table__td">1</td>';
    fuzzySet.column_sums.forEach(element => {
        columnSumsStr += '<td class="matrics-table__td">';
        columnSumsStr += element.toFixed(precision);
        columnSumsStr += '</td>';
    });
    columnSumsStr += '</tr>';
    tableInnerHTMLStr += columnSumsStr;

    var columInvertedSumsStr = '<tr class="matrics-table__row">';
    columInvertedSumsStr += '<td class="matrics-table__td">2</td>'
    fuzzySet.inverted_sums.forEach(element => {
        columInvertedSumsStr += '<td class="matrics-table__td">'
        columInvertedSumsStr += element.toFixed(precision)
        columInvertedSumsStr += '</td>'
    })
    columInvertedSumsStr += '</tr>'
    tableInnerHTMLStr += columInvertedSumsStr;

    var columnMembFuncStr = '<tr class="matrics-table__row">'
    columnMembFuncStr += '<td class="matrics-table__td">M(X)</td>'
    fuzzySet.membership_function.forEach(element => {
        columnMembFuncStr += '<td class="matrics-table__td">'
        columnMembFuncStr += element.toFixed(precision)
        columnMembFuncStr += '</td>'
    })
    columnMembFuncStr += '</tr>'
    tableInnerHTMLStr += columnMembFuncStr;
    table.innerHTML = tableInnerHTMLStr;
}

function renderGraph(xAxis, yAxis, title, xAxisTitle, yAxisTitle) {
    var canvas = document.getElementById("FuzzySetChart");

    // If the canvas doesn't exist, create it
    if (!canvas) {
        canvas = document.createElement("canvas");
        canvas.id = "FuzzySetChart";
        canvas.classList.add("chart-canvas");
        canvas.width = 750;
        canvas.height = 350;

        // Append the canvas to its container element
        var container = document.querySelector('.form-container');
        container.appendChild(canvas);
    }

    var ctx = canvas.getContext("2d");
    var options = {
        responsive: false,
        plugins: {
            title: {
                display: true,
                text: title || 'Графік нечіткої множини',
                font: {
                    family: 'Times',
                    size: 20,
                    style: 'normal',
                    lineHeight: 1.2,
                },
                color: 'black',
            },
            legend: {
                display: false,
            },  
        },
        scales: {}
    };

    if (xAxisTitle) {
        options.scales.x = {
            title: {
                display: true,
                text: xAxisTitle,
                font: {
                    family: 'Arial',
                    size: 14,
                    style: 'normal',
                    lineHeight: 1.2,
                },
                color: 'black',
            },
        };
    }

    if (yAxisTitle) {
        options.scales.y = {
            title: {
                display: true,
                text: yAxisTitle,
                font: {
                    family: 'Arial',
                    size: 14,
                    style: 'normal',
                    lineHeight: 1.2,
                },
                color: 'black',
            },
        };
    }

    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xAxis,
            datasets: [{
                data: yAxis,
                borderWidth: 1,
            }]
        },
        options: options
    });
}