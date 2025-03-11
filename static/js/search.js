document.addEventListener("DOMContentLoaded", function () {
    // Get references to the filter and sort elements
    const dateFrom = document.getElementById("filterDateFrom");
    const dateTo = document.getElementById("filterDateTo");
    const popularityMin = document.getElementById("filterPopularityMin");
    const popularityMax = document.getElementById("filterPopularityMax");
    const sortField = document.getElementById("sortField");
    const sortOrder = document.getElementById("sortOrder");
    const sourceCheckboxes = document.querySelectorAll("#filterSource input[type='checkbox']");
    const polarityCheckboxes = document.querySelectorAll("#filterPolarity input[type='checkbox']");
    const subjectivityCheckboxes = document.querySelectorAll("#filterSubjectivity input[type='checkbox']");
    const categoryCheckboxes = document.querySelectorAll("#filterCategory input[type='checkbox']");
    const applyFiltersButton = document.getElementById("applyFilters");
    
    // Collect filter values from checkboxes
    function getCheckedValues(checkboxes) {
        return Array.from(checkboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
    }

    // Handle Apply Filters button click
    applyFiltersButton.addEventListener("click", function () {
        // Collect all the filter values
        const filters = {
            date: {
                start: dateFrom.value || "*",  // If empty, match everything
                end: dateTo.value || "*"       // If empty, match everything
            },
            popularity: {
                min: popularityMin.value || 0,
                max: popularityMax.value || 100
            },
            source: getCheckedValues(sourceCheckboxes),
            polarity: getCheckedValues(polarityCheckboxes),
            subjectivity: getCheckedValues(subjectivityCheckboxes),
            category: getCheckedValues(categoryCheckboxes),
            sort: {
                field: sortField.value,
                order: sortOrder.value
            }
        };

        // Build the query string to send to the server (e.g., Solr)
        const queryParams = buildQueryParams(filters);
        fetchResults(queryParams);
    });

    // Build query params based on selected filters
    function buildQueryParams(filters) {
        let query = `q=*:*`;  // Default query to get all documents

        // Add date range filter
        if (filters.date.start !== "*" || filters.date.end !== "*") {
            query += `&fq=date:[${filters.date.start} TO ${filters.date.end}]`;
        }

        // Add popularity range filter
        query += `&fq=popularity:[${filters.popularity.min} TO ${filters.popularity.max}]`;

        // Add source filter
        if (filters.source.length > 0) {
            query += `&fq=source:(${filters.source.join(" OR ")})`;
        }

        // Add polarity filter
        if (filters.polarity.length > 0) {
            query += `&fq=polarity:(${filters.polarity.join(" OR ")})`;
        }

        // Add subjectivity filter
        if (filters.subjectivity.length > 0) {
            query += `&fq=subjectivity:(${filters.subjectivity.join(" OR ")})`;
        }

        // Add category filter
        if (filters.category.length > 0) {
            query += `&fq=category:(${filters.category.join(" OR ")})`;
        }

        // Add sorting option
        if (filters.sort.field) {
            query += `&sort=${filters.sort.field} ${filters.sort.order || "asc"}`;
        }

        return query;
    }

    // Fetch filtered results from the server
    function fetchResults(queryParams) {
        // Make a request to the server or Solr (this example uses a placeholder URL)
        const url = `/search?${queryParams}`;

        // Use fetch to request data (assuming Solr is set up at this endpoint)
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Render results
                renderResults(data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }

    // Render the search results dynamically
    function renderResults(data) {
        const resultsContainer = document.getElementById("resultsContainer");
        const resultsList = document.getElementById("resultsList");

        resultsList.innerHTML = "";  // Clear existing results

        if (data && data.response && data.response.docs.length > 0) {
            data.response.docs.forEach(result => {
                const listItem = document.createElement("li");
                listItem.classList.add("list-group-item");

                listItem.innerHTML = `
                    <strong>ID: ${result.id}</strong><br>
                    <p class="content">${result.text}</p>
                    <small>Date: ${result.date}</small><br>
                    <small>Popularity: ${result.popularity}</small><br>
                    <small>Source: ${result.source}</small><br>
                    <small>Polarity: ${result.polarity}</small><br>
                    <small>Subjectivity: ${result.subjectivity}</small><br>
                    <small>Category: ${result.category}</small>
                `;

                resultsList.appendChild(listItem);
            });
        } else {
            resultsContainer.innerHTML = "<p class='mt-3'>No results found.</p>";
        }
    }
});
