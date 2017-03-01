
requests_in_progress = []

var updateAutocomplete = function(){
    searchterm = document.getElementById('search_entry_box').value;
    if(searchterm.length == 0) return;
    requests_in_progress.forEach(function(r){
	r.abort();
    });
    xhr = fetch('/urlsearch/' + searchterm).then(function(response){
	if(!response.ok){
	    console.log('bad request')
	    return;
	}
	response.json().then(function(resp){
	    output = document.createElement('div')
	    if(resp['matches'].length){
		listy = document.createElement('ul')
		resp['matches'].forEach(function(m){
		    line = document.createElement('li')
		    ael = document.createElement('a')
		    ael.setAttribute('href', m)
		    ael.innerHTML = m
		    line.appendChild(ael)
		    listy.appendChild(line)
		    output.appendChild(listy)
		});
	    }
	    else{
		output.innerHTML = '<b>No matching URLs found</b>'
		console.log('matched out');
	    }
	    resultpane =  document.getElementById('results');
	    resultpane.innerHTML = '';
	    resultpane.appendChild(output);
	});
    });
    console.log('triggered fetch')			   
}

var initSearch = function(){
    searchbox = document.getElementById('search_entry_box')
    searchbox.addEventListener('keyup', updateAutocomplete, false);
    console.log('loaded');
}

document.addEventListener("DOMContentLoaded", initSearch);

