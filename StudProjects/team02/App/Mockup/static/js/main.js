function loadTable() {
    const spinner = document.getElementById("spinner");
    spinner.removeAttribute('hidden');
    
    const parkDiv = document.getElementById('parking-table');

    fetch('/spots', {
        method: 'GET',
        headers: {
            'Content-type': 'application/json'
        }
    })
    .then(data => data.json())
    .then(data => {
        spinner.setAttribute('hidden', '');
        console.log(data);

        parkDiv.style.display = 'flex';

        // get nr. of frames from db 
        nrFrames = data.length;
        
        // extract data into matrix of spots
        posTable = [];
        data[nrFrames - 1]["spots"].forEach(function(spot) {
            pos = spot['position'];
            x = pos[0];
            y = pos[1];
            if (posTable[x] == undefined) {
                posTable[x] = [];
            }
            posTable[x][y] = spot['occupied'];
        })

        tableContent = '';
        posTable.forEach(function(row) {
            tableContent += '<tr>';
            row.forEach(function(spot) {
                if (!spot) {
                    tableContent += '<td><div class="empty-spot"></div></td>';
                }
                else {
                    tableContent += '<td><div class="occupied-spot"></div></td>';
                }
            })
            tableContent += '</tr>';
        })
        document.getElementById('spots-table').innerHTML = tableContent;
        console.log(tableContent);
    })
}




function uploadFrame() {
    var input = document.querySelector('input[type="file"]');

    const data = new FormData();
    data.append('file', input.files[0]);
    data.append('filename', 'example');
 
    fetch('/upload', {
        method: 'POST',
        body: data
    });
}