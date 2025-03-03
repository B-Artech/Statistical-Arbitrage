let chart;

function updateData() {
    fetch('http://localhost:5000/data')
        .then(response => response.json())
        .then(data => {
            updateTable(data);
            updateChart(data);
        });
}

function updateTable(data) {
    let html = '<table><thead><tr>';
    // Create headers
    for (let key in data[0]) {
        html += `<th>${key}</th>`;
    }
    html += '</tr></thead><tbody>';

    // Add rows
    data.forEach(row => {
        html += '<tr>';
        for (let key in row) {
            html += `<td>${row[key]}</td>`;
        }
        html += '</tr>';
    });
    html += '</tbody></table>';
    document.getElementById('tableData').innerHTML = html;
}


// Update every minute
setInterval(updateData, 60000);
updateData(); // Initial load