const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );
const fs = require('fs');

// http://stackoverflow.com/questions/901115/get-query-string-values-in-javascript
function getParameterByName(name) {
	name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
	var regexS = "[\\?&]" + name + "=([^&#]*)";
	var regex = new RegExp(regexS);
	var results = regex.exec(window.location.search);

	if (results == null) {
		return "";
	} else {
		return decodeURIComponent(results[1].replace(/\+/g, " "));
	}
}

function makeListItems(key, val) {
	var items = [];
	if (key == "id")
	{
		items.push("\n");
	}
	items.push(key + ', ');

	$.each(val, function(key, val) {
		if (typeof(val) == 'object') {
			items.push(makeListItems(key, val));
		} else {
			items.push(key + ', ' + val + ',');
		}
		if (key == "id")
		{
			items.push("\n");
			console.log("yes");
		}
	});

	return items.join('');
}

$(global).ready(function() {
	var page = '';
	var loan_id = '';
	var url;
	var title;

	// Get page parameter from URL
	if (page = getParameterByName('page')) {
		page = '&page='+page;
	}

	// Is this a request for an individual loan?
	if (loan_id = getParameterByName('loan_id')) {
		url = 'http://api.kivaws.org/v1/loans/'+loan_id+'.json';
		title = 'Loan';
	} else {
		url ='http://api.kivaws.org/v1/loans/newest.json';
		title = 'Loans';
	}

	// Request loan data
	$.getJSON(url+page, function(data) {
		var items = [];

		// Build the list
		items.push(makeListItems(title, data.loans));
        fs.appendFile("outputs/kiva.csv", makeListItems(title, data.loans), (err) => {
            if (err) {
              console.log(err);
            }
            else {
              // Get the file contents after the append operation
                fs.readFileSync("outputs/kiva.csv", "utf8");
            }
          });
	});
});
