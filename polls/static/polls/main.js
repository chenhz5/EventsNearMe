console.log("loaded main.js");

var getJSON = function(url, successHandler, errorHandler) {
  var xhr = typeof XMLHttpRequest != 'undefined'
    ? new XMLHttpRequest()
    : new ActiveXObject('Microsoft.XMLHTTP');
  xhr.open('get', url, true);
  console.log("xhr open")
  xhr.onreadystatechange = function() {
    var status;
    var data;
    // https://xhr.spec.whatwg.org/#dom-xmlhttprequest-readystate
    if (xhr.readyState == 4) { // `DONE`
      status = xhr.status;
      if (status == 200) {
    	console.log("status 200")
        data = JSON.parse(xhr.responseText);
    	console.log("after json parse");
        successHandler && successHandler(data);
      } else {
        errorHandler && errorHandler(status);
      }
    }
  };
  xhr.send();
};


function generateDivs(numDivs){
	var divIndex=0;
	console.log("in generate divs: " + numDivs);
    for(divIndex; divIndex< numDivs; divIndex++) {
        var d_id = divIndex+1; //??
        var div = jQuery('<div style="border:1px solid black;width:50%; padding:10px;" id="eventDiv-'+ divIndex + '"></div>')
        jQuery('body').append(div);
    }
} ;

var jumpToUrl = function(){
    //redirect to a new page
	  if(val.url != null){
		  window.location.href = val.url;
	  }
	};
var deleteOldDivs = function(numDivs){
	var divIndex=0;
	console.log("deleting divs" + numDivs);
    for(divIndex; divIndex< numDivs; divIndex++) {
        var d_id = divIndex+1; //
        $("#eventDiv-"+divIndex).remove();
    }
}

var old_length = 0;
var get_event_cb = function(data) {
  //alert('Your data is ' + data);
	deleteOldDivs(data.length);
  generateDivs(data.length);
  jQuery.each(data, function(i, val) {
	  console.log(val.name + "*** " + val.url);
	  $("#eventDiv-" + i).append(document.createTextNode(" - " + val.name + "****" + val.url ));
	});
  
  jQuery.each(data, function(i, val) {
	  console.log("adding url links");
	//TODO: error because the js is called before teh UI is loaded
	  console.log("#eventDiv-" + i);
	  //$("#eventDiv-" + i).addEventListener("click", function(){
	  $("#eventDiv-" + i).bind("click", jumpToUrl, false);
		
	  old_length = data.length;
	});
  
  document.getElementById("submit_btn").disabled = false;

};

var onErrorcb = function(status) {
  alert('Something went wrong.');
  //disable submit button
  document.getElementById("submit_btn").disabled = false;
	
};


$(document).ready(function() {
	//getJSON("http://127.0.0.1:8000/event/city=bangalore&category=sports", get_event_cb, onErrorcb);
});


function onSubmitClicked(){
	
	//TODO: get params from form and generate the url
	//disable submit button
	document.getElementById("submit_btn").disabled = true;
	
	var e = document.getElementById("select_city");
	city = e.options[e.selectedIndex].value;
	console.log("city" + city);
	
	var f = document.getElementById("select_category");
	category = f.options[f.selectedIndex].value;
	console.log("category" + category);
	
	var max_results = document.getElementById("max_results").value;
	//TODO: validate if max_result is an int
	console.log("max_results " + max_results);
	
	baseUrl = "http://127.0.0.1:8000/event/";
	//baseUrl = "http://ec2-54-152-59-253.compute-1.amazonaws.com/event/"
	url = baseUrl + "city="+city+ "&category="+category;
	if(max_results != null){
		url += "&max_results="+max_results
	}
	
	console.log("final url: "+ url);
	getJSON(url, get_event_cb, onErrorcb);

}

