var tableData = {"12345":{'Genre': ['Mystery', 'Thriller'], 'Liked': ['Shawn'], 'Rating': 8.5, 'Runtime': 112, 'Seen': ['Shawn'], 'Title': 'Rear Window'},
 "3456":{'Genre': ['Crime', 'Drama'], 'Rating': 9.0, 'Runtime': 96, 'Title': '12 Angry Men'}}
buildTable(tableData)

function buildTable(table_data) {
    var table = document.getElementById('movie-table')
    for (i in table_data){
        var row = `<div class="table-spacing"></div>
                    <tbody class="list-item">
                        <tr class="list-table-data">
                            <td>${table_data[i]['Title']}</td>
                            <td>${table_data[i]['Runtime']}</td>
                            <td>${table_data[i]['Genre']}</td>
                            <td>${table_data[i]['Rating']}</td>
                        </tr>
                    </tbody>`
        table.innerHTML += row
        // println(data[i]['Title'])
    }
}

