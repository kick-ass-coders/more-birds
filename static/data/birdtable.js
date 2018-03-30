// // Get the input field
// var input = document.getElementById("birdInput");

// // Execute a function when the user releases a key on the keyboard
// input.addEventListener("keyup", function(event) {
//   // Cancel the default action, if needed
//   event.preventDefault();
//   // Number 13 is the "Enter" key on the keyboard
//   if (event.keyCode === 13) {
//     // Trigger the button element with a click
//     document.getElementById("birdSearchBtn").click();
//   }
// });

// add a click event here to get the input filter value

var DataController = {
  raw: [],
  filters: {
    textIncludes: function(search) {
      return function(datum) {
        return datum.toLowerCase().includes(search.toLowerCase())
      }
    }
  },
  filtersApplied: [],
  filtered: [],
  applyFilters: function() {
    var allRejectedRows = []
    for (const {column, filterName, value} of this.filtersApplied) {
      console.log(this.columnarFormat)
      const theseRejected = this.columnarFormat[column].map((v, i) => {
        return [v, i]
      }).filter(([v, i]) => {
        return !this.filters[filterName](value)(v)
      }).map(([v, i]) => {
        return i 
      })
      allRejectedRows = allRejectedRows.concat(theseRejected)
    }
    this.filtered = this.raw.filter(function(datum, i) {
      return !allRejectedRows.includes(i)
    })
  },
  columnarFormat: {},
  loadData: function(data) {
    this.columnarFormat = {}
    this.raw = data
    return data.reduce(function(a, x) {
      Object.entries(x).forEach(function([k, v]) {
        if (k in a) {
          a[k].push(v)
        } else {
          a[k] = [v]
        }
      })
      return a
    }, this.columnarFormat)
  },
  addFilter: function(filterName, column, value) {
    this.filtersApplied.push({
      filterName: filterName,
      column: column,
      value: value
    })
  },
  clearFilters: function() {
    this.filtersApplied = []
    this.filtered = []
  },
  paginateData: function* (n) {
    var index = 0
    while (index + n < this.filtered.length) {
      yield this.filtered.slice(index, index + n)
      index = index + n
    }
  }
}

var tabulate = function (data,columns) {
    var table = d3.select('body').append('table')
      var thead = table.append('thead')
      var tbody = table.append('tbody')
  
      thead.append('tr')
        .selectAll('th')
          .data(columns)
          .enter()
        .append('th')
          .text(function (d) { return d })
  
      var rows = tbody.selectAll('tr')
          .data(data)
          .enter()
        .append('tr')
  
      var cells = rows.selectAll('td')
          .data(function(row) {
              return columns.map(function (column) {
                  return { column: column, value: row[column] }
            })
        })
        .enter()
      .append('td')
        .text(function (d) { return d.value })
  
  return table;
}
  
d3.csv('../static/data/list.csv', function (data) {
  // console.log(data);
  DataController.loadData(data)
  var columns = ['Common Name','Species Code']
  DataController.addFilter('textIncludes', 'Common Name', 'bunting')
  DataController.applyFilters()
  const firstSlice = DataController.paginateData(50).next().value
  console.log(firstSlice)
  tabulate(firstSlice, columns)
})

function searchableBirds() {
  var filter, table, tr, td, i;
  
  filter = input.value.toLowerCase();
  tr = table.getElementsByTagName("tr");
  table = document.getElementsByTagName("table");


  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toLowerCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

d3.select("#birdInput")
  .on("keyup", function() {
    var searched_data = data,
      text = this.value.trim();

    var searchResults = searched_data.map(function(r) {
      var regex = new RegExp("^" + text + ".*", "i");
      if (regex.test(r.title)) {
        return regex.exec(r.title)[0]
      }
    })
  })

  searchResults = searchResults.filter(function(r) {
    return r != undefined;
  })

  searched_data = searchResults.map(function(r) {
    return data.filter(function(p){
      return p.title.indexOf(r) != -1;
    })
  })
