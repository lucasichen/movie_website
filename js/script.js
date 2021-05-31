var tableData = [{'Genre': ['Mystery', 'Thriller'], 'Liked': ['Shawn'], 'Rating': 8.5, 'Runtime': 112, 'Seen': ['Shawn'], 'Title': 'Rear Window'},
 {'Genre': ['Crime', 'Drama'], 'Rating': 9.0, 'Runtime': 96, 'Title': '12 Angry Men'}, ]
buildTable(tableData)

function buildTable(data) {
    var table = document.getElementById('movie-table')
    for (i in data){
        var row = `<div class="table-spacing"></div>
                    <tbody class="list-item">
                        <tr class="list-table-data">
                            <td>${data[i].Title}</td>
                            <td>${data[i].Runtime}</td>
                            <td>${data[i].Genre}</td>
                            <td>${data[i].Rating}</td>
                        </tr>
                    </tbody>`
        table.innerHTML += row
    }
}

