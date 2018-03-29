var $birdInput = document.getElementById("birdInput");
var $birdSearchBtn = document.getElementById("birdSearchBtn");
var $speciesTable = document.getElementById("speciesTable");
var n = 50;

var fullSubset = getData("");

buildTable(fullSubset, 1)

// A callback function is called in response to a click of the increment button
$birdSearchBtn.addEventListener("click", function(){pageTable(1)});

function pageTable(pageNum){
    event.preventDefault();

    if (document.contains(document.getElementById("buttons"))) {
        document.getElementById("buttons").remove();
    }   

    for(var i = $speciesTable.rows.length - 1; i > 0; i--)
    {$speciesTable.deleteRow(i);}

    var fullSubset = getData($birdInput.value);
    buildTable(fullSubset, pageNum);
    console.log($birdInput.value)
};

// fxn to filter by an input for a key
function getbyInput(input, key){
    // if no input is passed, return full dataset
    if (input == "" || input =="all") {
        return birdDB
    // else filter by key & input
    } else {
        return birdDB.filter(function (a) {
            return a[key] == input;
        });
    }
};


function getData(bird) {

    // filter by each possible input
    birdSubset = getbyInput(bird, "comName");

    return birdSubset;
    };
  
// fxn to build the summary-table
function buildTable(data, pageNum) {
    
    // store number of rows
    rowNum = data.length;

    // store number of pages
    var pageCount = Math.ceil(rowNum / n);

    // create an array with the keys for each row of data
    var dk = Object.keys(data[0]);

    // for each row of data....
    function tableInside(first, last){

        for (var i = first; i < last; i++) {

            // create a tr
            var tr = document.createElement("tr");

            // for each key in each row of data...
            for (var j=0; j < dk.length; j++){
                // create a tr
                var td = document.createElement("td");
                // create a txt with the datum of interest
                var txt = document.createTextNode(data[i][dk[j]]);
                // append the txt to the td
                td.appendChild(txt);
                // append the td to the tr
                tr.appendChild(td);
            };

            // append the tr to the table
            $table.appendChild(tr);
        };
  };

  /* generate table with the start & end position determined
   by the page number*/
  if (rowNum <= n){
      tableInside(0, rowNum);
    } else if (pageNum == 1) {
        tableInside(0, 49);

    } else if (pageNum == pageCount) {
        first = (pageNum-1)*50;
        tableInside(first, rowNum);
    } else {
        var first = (pageNum-1)*50;
        var last = first + 49;
        tableInside(first, last);
    };
    if (rowNum > n){
        $speciesTable.insertAdjacentHTML("afterend","<div id='buttons'></div");
        // create the pagination buttons
        document.getElementById("buttons").innerHTML = pageButtons(pageCount, pageNum);
        // CSS Stuff
        document.getElementById("id"+pageNum).setAttribute("class","active");
    };

};

function pageButtons(pageCount,pageNum) {
    var prevDis = (pageNum == 1)?"disabled":"";
    var nextDis = (pageNum == pageCount)?"disabled":"";

    
    if(pageCount <= 10){
        buttons = "<input type='button' id='id1' value='1' class='nums' onclick='pageTable(1)'>";
        for (i=2; i<=pageCount;i++){
            buttons += "<input type='button' class='nums' id='id"+i+"'value='"+i+"' onclick='pageTable("+i+")'>";
        }
    } else if (pageNum>=pageCount-9 && pageNum<=pageCount){
        buttons = "<input type='button' value='First' class='ends' onclick='pageTable(1)'>";
        buttons += "<input type='button' class='arrows' value='&lt;' onclick='pageTable("+(pageNum - 1)+")' "+prevDis+">";
        
        for (i=pageCount-9; i<=pageCount;i++){
            buttons += "<input type='button' class='nums' id='id"+i+"'value='"+i+"' onclick='pageTable("+i+")'>";
        } 
    } else {
        buttons = "<input type='button' value='First' class='ends' background:black; color:lightgreen;' onclick='pageTable(1)'>";
        buttons += "<input type='button' class='arrows' value='&lt;' onclick='pageTable("+(pageNum - 1)+")' "+prevDis+">";
        
        for (i=pageNum; i<=pageNum+9; i++){
            buttons += "<input type='button' class='nums' id='id"+i+"'value='"+i+"' onclick='pageTable("+i+")'>";
            }

        buttons += "<input type='button' class='arrows' value='&gt;' onclick='pageTable("+(pageNum + 1)+")' "+nextDis+">";
        buttons += "<input type='button' class='ends' value='Last' onclick='pageTable("+pageCount+")'>";
    }

    
    
    return buttons;
};

