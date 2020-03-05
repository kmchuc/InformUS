function autocomplete(inp, arr) {
    ///autocomplete takes in 2 arguments: text field element and array of possible autcomplete values
    var currentFocus;

    ///executes function when someone writes in text field
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;

        ///close any already open lists of autocompleted values
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;

        ///create a div element that will contain items 
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        ///appends the div element as a child of the autocomplete container
        this.parentNode.appendChild(a);

        ///for each item in the array
        for (i = 0; i < arr.length; i++) {

            ///checks to see if the item starts with the same letters as field value
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                ///creates a div element for each matching element
                b = document.createElement("DIV");

                ///makes the matching letters bold
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);

                ///insert an input field that will hold the current array item's value
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

                ///executes function when someone clicks the item value (div element)

                    b.addEventListener("click", function(e) {
                        ///inserts the value for the autocomplete text field
                        inp.value = this.getElementsByTagName("input")[0].value;

                        ///closes the list of autocompleted values
                        closeAllLists();
                    });
                    a.appendChild(b);
            }
        }
    });

    ///executes functions when user presses key on keyboard
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");

        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {

            ///if down key is pressed, increases currentFocus variable
            currentFocus++;

            ///makes the current item more visible
            addActive(x);
        } else if (e.keyCode == 38) {

            ///if up button pressed, decrease currentFocus variable 
            currentFocus--;

            ///makes the current item more visible
            addActive(x);
        } else if (e.keyCode == 13) {

            //if the enter key is pressed, prevents form from being submitted
            e.preventDefault();
            if (currentFocus > -1) {

                ///simulates click on "active" item
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        ///this function classifies an item as "active"

        if (!x) return false;

        ///removes "active" class on all items
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length-1);

        ///adds class "autocomplete-active"
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        ///this function removes the "active" class from all autocomplete items

        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        ///closes all autocomplete lists in the document, except the one passed as argument

        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
}

///executes function when someone clicks in the document
document.addEventListener("click", function(e) {
    closeAllLists(e.target);
});

var parties = ["Ace Party", "Alaskan Independence Party", "American Independence Conservative", "American Independent Party", "American Party", "American People's Freedom Party", "Americans Elect", "Citizen's Party", "Commandments Party", "Commonwealth Party of the U.S.", "Communist Party", "Concerned Citizens Party Of Connecticut", "Constitution Party", "Constitutional", "Country", "D.C. Statehood Green Party", "Democratic-Nonpartisan League", "Democratic Party", "Democratic/Conservative", "Democratic-Farmer-Labor", "Desert Green Party", "Federalist", "Freedom Labor Party", "Freedom Party", "George Wallace Party", "Grassroots", "Green Party", "Green-Rainbow", "Human Rights Party", "Independence Party", "Independent", "Independent American Party", "Independent Conservative Democratic", "Independent Green", "Independent Party of Delaware", "Industrial Government Party", "Jewish/Christian National", "Justice Party", "La Raza Unida", "Labor Party", "Less Federal Taxes", "Liberal Party", "Libertarian Party", "Liberty Union Party", "Mountain Party", "National Democratic Party", "Natural Law Party", "New Alliance", "New Jersey Conservative Party", "New Progressive Party", "No Party Affiliation", "No Party Preference", "None", "Nonpartisan", "Non-Party", "One Earth Party", "Other", "Pacific Green", "Party for Socialism and Libertarian", "Peace and Freedom", "Peace and Freedom Party", "People Over Politics", "People's Party", "Personal Choice Party", "Popular Democratic Party", "Progressive Party", "Prohibition Party", "Puerto Rican Independence Party", "Raza Unida Party", "Reform Party", "Republican Party", "Resource Party", "Right To Life", "Socialist Equality Party", "Socialist Labor Party", "Socialist Party", "Socialist Party U.S.A.", "Socialist Workers Party", "Taxpayers", "Taxpayers Without Representation", "Tea Party", "Theo-Democratic", "U.S. Labor Party", "U.S. Taxpayers Party", "Unaffiliated", "United Citizen", "United Party", "Unknown", "Veterans Party", "We The People", "Write-In"]