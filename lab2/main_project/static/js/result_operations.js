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