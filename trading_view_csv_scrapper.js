// search for _createItem
function arrayToCSV(data) {
    const csvRows = [];
    // Add headers if necessary, for example:
    csvRows.push('Timestamp,Open,High,Low,Close,Volume');

    // Loop through items and convert each to CSV row
    data.forEach(item => {
        const csvRow = item.value.join(',');
        csvRows.push(csvRow);
    });

    return csvRows.join("\n");
}

// Function to trigger the CSV download
function downloadCSV(csvData, filename = 'stock_data.csv') {
    const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Generate CSV from data and initiate download
const csvData = arrayToCSV(h._items);
downloadCSV(csvData);
