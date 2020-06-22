$(document).ready(function() {
    $('.bonecard').css("cursor", "pointer");
    for (var i = 0; i < 46; i++) {
        var pin = '<div class="pin" id="P8_';
        pin += '' + (i + 1);
        pin += '" style="left:';
        pin += ((Math.floor(i / 2) * 25) + 200).toFixed(0);
        pin += 'px;top:';
        pin += '' + (((i % 2) * 25) + 5).toFixed(0);
        pin += 'px;"></div>';
        $('.bonecard').append(pin);
    }
    for (var i = 0; i < 46; i++) {
        var pin = '<div class="pin" id="P9_';
        pin += '' + (i + 1);
        pin += '" style="left:';
        pin += ((Math.floor(i / 2) * 25) + 200).toFixed(0);
        pin += 'px;top:';
        pin += (((i % 2) * 25) + 490).toFixed(0);
        pin += 'px;"></div>';
        $('.bonecard').append(pin);
    }
    
    var initiateUpdate = (function (passedurl){
        $.ajax({
        	url: passedurl,
        	type: 'get',
        	dataType: 'JSON',
        	success: updatePage,
        	error: function(e) {
        	   console.log(e.message);
        	}
        });
    });
        
    $(".pin, .led").each(function(){
       $(this).click(function(){
           var myID = $(this).prop('id');
           console.log(myID);
           initiateUpdate('_do?cmd=toggleState&pin=' + myID + '#simulator.html');
       });
        
    });
    var updatePage = (function(data, textStatus, xhr){
    	//console.log(textStatus);
    	if (data['cmd']=='allPins'){
        	var count = parseInt(data['data']['count']);
        	for (var i = 0; i < count; i++){
        		var myPin = data['data'][i.toString()];
        		//console.log('myPins - ' + JSON.stringify(myPin));
        		//var $master = $('#master');
        		var myID = myPin['pin'];
        		
        	    $('#' + myID).addClass('active');
        	    //console.log(myPin['state'] )
        	    if (myPin['state'] == 1){
        	    	$('#' + myID).css('background-color','white');
        	    }else if (myPin['state'] == 0){    
        	    	$('#' + myID).css('background-color','black');
        	    }else{
        	    	$('#' + myID).css('background-color','blue');
        	    }
        	}
    	}else{
            initiateUpdate('_fetch?cmd=allPins');
    	}
    });

    initiateUpdate('_fetch?cmd=allPins');
});

    
 