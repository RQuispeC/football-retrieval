function session() {

      var r = document.getElementById("representations");
      //var rep = r.options[r.selectedIndex].value;

      var s = document.getElementById("strategies");
      //var str = s.options[s.selectedIndex].value;

      var v = document.getElementById("kvalue");
      //var val = v.value;

    var globalVariable1={
       rep: r.options[r.selectedIndex].value
    };

    var globalVariable2={
       sta: s.options[s.selectedIndex].value
    };

    var globalVariable3={
       val:v.value
    };

      //console.log(globalVariable1);
      //console.log(globalVariable2);
      //console.log(globalVariable3);

      window.location.href = "about.html";

    } 

    $("#getHtml").click(function() {
        session();
    });
  
    $("#reset").click(function(){
      $.ajax({
        url:"http://localhost:5000/receiver/55/77",
        type: 'POST',
        dataType: 'application/javascript',
        success:function(result){
            console.log("success"); //does not print
            console.log(result)
            var json = JSON.parse(result).values
            console.log(json[0])
            //console.log(result);   //does not print
        },
        error: function(e) {
        console.log("ERROR: "+ e);
      }
    });
  });