var $submitBtn = document.getElementById("match");
$submitBtn.addEventListener("click", function(){birdList()});

function birdList(){
    
      var $state = document.getElementById("state");
    
      var state = $state.value;
    
      var $birdCat = document.getElementById('birdCat');

      var birdCat = $birdCat.value;

      var stateSub = getbyInput(stateChecklists, state, 'state')

      var catSub = getbyInput(stateSub, birdCat, 'category_name')

      console.log(catSub)
      }

function getbyInput(data, input, key){
        data.filter(function (a) {
            // convert to lower case
            input = input.toLowerCase();
            return a[key] == input;
        });
    };