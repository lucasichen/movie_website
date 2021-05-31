var tableData = [{'Title':'21',
                'Runtime': 123,
                'Genres':['Comedy','Horror'],
                'Rating':7.0},
                {'Title':'Alien',
                'Runtime':123,
                'Genres':['Action','Comedy'],
                'Rating':8.0},
                {'Title':'Bob',
                'Genres':['Action'],
                'Rating': 7}]
buildTable(tableData)

function buildTable(data) {
var table = document.getElementById('table-body')
for (i in data){
    var row = `<tr>
                <td>${data[i].Title}</td>
                <td>${data[i].Runtime}</td>
                <td>${data[i].Genres}</td>
                <td>${data[i].Rating}</td>
            </tr>`
    table.innerHTML += row
    }
}

