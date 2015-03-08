var temp = cekstatustemp();
if(temp == 'locked'){
  $("#qrlock").load('locked');
  temp = 'locked';
}else if(temp == 'unlocked'){
  $("#qrlock").load('unlocked');
  temp = 'unlocked';
}

function lock(){
	$.ajax({
                type: "POST",
                url: "lock",
                data: {lock:"dce7c4174ce9323904a934a486c41288"}
        });

}


setInterval(function(){
  var baru = cekstatus();
  if (baru != temp ){
    if (baru == 'locked'){
      $("#qrlock").load('locked');
      temp = 'locked';
    } else if(baru == 'unlocked'){
      $("#qrlock").load('unlocked');
      temp = 'unlocked';
    };
  };
}, 2000);


function cekstatustemp(){
  $.ajax({
    type: "GET",
    url: "statusplain",
    success: function(html){
      $("#temp").val(html);
    }
  });

  return $("#temp").val();
}

function cekstatus(){
  $.ajax({
    type: "GET",
    url: "statusplain",
    success: function(html){
      $("#baru").val(html);
    }
  });
  return $("#baru").val();
}

