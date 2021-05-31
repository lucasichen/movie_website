var tableData = [{'Genre': ['Mystery', 'Thriller'], 'Liked': ['Shawn'], 'Rating': 8.5, 'Runtime': 112, 'Seen': ['Shawn'], 'Title': 'Rear Window'},
 {'Genre': ['Crime', 'Drama'], 'Rating': 9.0, 'Runtime': 96, 'Title': '12 Angry Men'}, ]
buildTable(tableData)

function buildTable(data) {
    var table = document.getElementById('table-body')
    for (i in data){
        var row = `<tr>
                    <td>${data[i].Title}</td>
                    <td>${data[i].Runtime}</td>
                    <td>${data[i].Genre}</td>
                    <td>${data[i].Rating}</td>
                </tr>`
        table.innerHTML += row
    }
}

