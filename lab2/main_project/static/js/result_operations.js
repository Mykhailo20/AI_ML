function addEventListeners(elements, eventName, eventHandler) {
    // Loop through each key in the elements dictionary
    Object.keys(elements).forEach(function(key) {
        // Get the selector for the current key
        var selector = elements[key];
        // Check if the selector corresponds to one or multiple elements
        var elementsMatchingSelector = document.querySelectorAll(selector);
        // If there are matching elements, attach the event handler to each one
        if (elementsMatchingSelector.length > 0) {
            elementsMatchingSelector.forEach(function(element) {
                element.addEventListener(eventName, eventHandler);
            });
        } else {
            // If there's only one matching element, attach the event handler to it
            var singleElement = document.querySelector(selector);
            if (singleElement) {
                singleElement.addEventListener(eventName, eventHandler);
            }
        }
    });
}

function getFuzzySetValues(elements) {
    var data = {};

    // Iterate over the keys of the dictionary
    Object.keys(elements).forEach(function(key) {
        var element = document.querySelectorAll(elements[key]);
        if (element) {
            if (element.length === 1) {
                data[key] = element[0].value;
            } else {
                data[key] = [];
                element.forEach(function(item) {
                    data[key].push(item.value);
                });
            }
        }
    });

    return data;
}

// Function to handle the Enter key press event
function handleEnter(event) {
    if (event.key === 'Enter') {
        console.log("Enter btn was clicked!");

        // Get the updated fuzzySet values
        var elements = {
            'parameter_name': 'input[name="parameter_name_td_input"]',
            'parameter_values': 'input[name="parameter_value_td_input"]',
            'expert_evaluations': 'input[name="expert_evaluation_td_input"]'
        };
        var data = getFuzzySetValues(elements);

        // Send the updated parameter name, parameter values, and expert evaluations to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/update_parameters', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Handle the response from the server (update the matrix and graph)
                    var response = JSON.parse(xhr.responseText);

                    // Update the input values with the new parameter values
                    var fuzzySet = JSON.parse(response.fuzzy_set);

                    // Render the table
                    renderTable(fuzzySet, response.precision);

                    // Add eventListeners
                    addEventListeners(elements, 'keypress', handleEnter);

                    // Redraw the graph with the new data
                    var existingChart = Chart.getChart("FuzzySetChart");
                    if (existingChart) {
                        existingChart.destroy();
                    }

                    renderGraph(response.graph_data.x_axis, response.graph_data.y_axis, 'Графік нечіткої множини', fuzzySet.parameter_name);
                } else {
                    // Handle errors
                    console.error('Failed to update parameters:', xhr.status);
                }
            }
        };
        xhr.send(JSON.stringify(data));
    }
}