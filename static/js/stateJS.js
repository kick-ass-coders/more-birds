var stateKeys = Object.keys(state_center);

// Populating dropdown with state names
function dropDown(){
  
  var stateDrop = document.getElementById("stateDrop");
  for (i = 0; i < stateKeys.length; i++) {
          var stateOp = document.createElement("option");
          stateOp.text = stateKeys[i];
          stateOp.value= stateKeys[i];
          stateDrop.appendChild(stateOp);
      }
    }

function stateName(ST){
  var st_head = document.getElementById("stateName");
  st_head.innerHTML = state_center[ST].state;
}
// on first load
stateName("AL");

// create dropdown
dropDown();

// insert state name into header
stateName("AL");

// initializing map
stateMap("AL");

// initializing chart
siteChart("AL");

// initialize bird photos
birdPhotos("AL");

// what to do when the state is changed
function optionChanged(ST){
  console.log(ST);
  stateName(ST);
  stateMap(ST);
  siteChart(ST);
  birdPhotos(ST);
  }



function siteChart(ST){
  url = 'siteData/'+ST;
  Plotly.d3.json(url, function(error, siteData){
    if (error) return console.warn(error);
  var values = siteData.map(record => record.species_number);
  var sites = siteData.map(record => record.locName);
  var colors = ["#9e9ac8", "#b5afed", "#f6b2ff", "#ffc1df", "#ffebbc", "#ffc849", "#ff975b", "#ff830f", "#db6600", "#843c09"]
  var data = [
    {
      x: values,
      y: [10,9,8,7,6,5,4,3,2,1],
      type: 'bar',
      text: sites,
      marker: {
        color: colors
      }, 
      orientation: 'h'
    }
  ];

  var layout = {
    width: 300,
    height: 400,
    margin: {
            l: 20,
            r: 50,
            b: 20,
            t: 20,
            pad: 20
          },
    xaxis: {
      showline: false,
      showticklabels: false
    },
    yaxis: {
      showticklabels: false
    },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)'
  };

  Plotly.newPlot('sitesChart', data, layout);
}
)}

function birdPhotos(ST){
  url = 'birdData/'+ST;
  Plotly.d3.json(url, function(error, birdData){
    if (error) return console.warn(error);
  var names = birdData.map(record => record.comName);
  var images = birdData.map(record => record.img);
  var links = birdData.map(record => record.link);

  for(i=0; i<5; i++){
  document.getElementById('bird'+(i+1)).innerHTML = "<div id=bird"+(i+1)+"style='width: 100px; height: 100px;'></div>";
  var feature = document.getElementById('bird'+(i+1))
    if(links[i] !== "no link"){
      feature.href = links[i];
    }
    
    var birdImg = document.createElement("img");
    birdImg.style = "width: 155px;"
    if(images[i] === "no img"){
      birdImg.src = "../static/images/no-bird.png"
    } else {
      birdImg.src = images[i];
    }

    var figCap = document.createElement("figcaption");
    figCap.innerHTML = names[i];

    feature.appendChild(birdImg);
    feature.appendChild(figCap);
  }
  }
  )}


