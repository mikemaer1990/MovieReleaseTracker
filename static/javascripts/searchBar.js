// Select our input element / will select the main pages input OR the navbar input if not on the main page
const input =
    document.querySelector("input#movie_title") ||
    document.querySelector("#searchBarInput");
// Select our list element to insert search results into
const resultsList = document.querySelector(".search-results");
// Create array element to store results inside
let searchResultsList = [];

// Query TMDB api for results
const searchResults = async (query) => {
    const request = await fetch(
        `https://api.themoviedb.org/3/search/multi?api_key=aa3bb4dfce8ff1e70491e21f7ac128d9&language=en-US&query=${query}&page=1&include_adult=false&region=US`
    );
    const data = await request.json();
    return data.results;
};

// Call our api function based on the user's input
const displayResults = async () => {
    try {
        const query = input.value;
        // If the user clears their search - reset the list and exit function
        if (query === "" || query === null) {
            resultsList.innerHTML = "";
            return;
        }
        // Get a response from our api based on the query and then store it in our array
        await searchResults(query).then((result) => {
            searchResultsList.push(result);
        });
        // Only keep the most recently returned api call
        if (searchResultsList.length >= 1) {
            searchResultsList = searchResultsList.slice(
                searchResultsList.length - 1,
                searchResultsList.length
            );
        }

        // Create an html element containing search results as a list item
        const html = searchResultsList[0]
            .map((item) => {
                // Store the title (movie/person) or name (tv)
                const title = item.title || item.name;
                // Store the date / (movie) or (tv)
                let date = item.release_date || item.first_air_date;
                if (date != 'TBA' && date != undefined) {
                    date = date.slice(0, 4)
                } else {
                    date = 'TBA'
                }
                // Store the id & media type
                const id = item.id;
                const media = item.media_type;
                // Create a list item for person - which leads to a different route
                if (media === "person") {
                    return `
                    <a href="/profile/${id}">
                        <li>${title}</li>
                    </a>
                `;
                    // Create a list item for tv and movies
                } else {
                    return `
                <a href="/details/${media}/${id}">
                    <li>${title} (${date})</li>
                </a>
            `;
                }
            })
            .join(""); // Join all li items together and then insert into our unordered list
        resultsList.innerHTML = html;
    } catch {
        // Ignore - this only happens when user hits enter to search before api call ends
    }
};

// Listen for key up events and make api calls and display results
input.addEventListener("keyup", displayResults);
// Listen for clicks oustside of search input/items
document.addEventListener("click", (e) => {
    // Clear results and text if user clicks off the search input
    if (e.target != input && e.screenX != 0 && e.screenY != 0 && !e.target.classList.contains("btn") && !e.target.parentElement.classList.contains("btn")) { // Had to add 0 / 0 for X/Y coords to make hitting enter when submitting works
        // Clear the search bar and remove results
        input.value = "";
        resultsList.innerHTML = "";
    }
});



const toggleColorMode = e => {
    // Switch to Light Mode
    if (e.currentTarget.classList.contains("light--hidden")) {
        // Sets the custom HTML attribute
        document.documentElement.setAttribute("color-mode", "light");

        //Sets the user's preference in local storage
        localStorage.setItem("color-mode", "light")
        return;
    }

    /* Switch to Dark Mode
    Sets the custom HTML attribute */
    document.documentElement.setAttribute("color-mode", "dark");

    // Sets the user's preference in local storage
    localStorage.setItem("color-mode", "dark");
};

// Get the buttons in the DOM
const toggleColorButtons = document.querySelectorAll(".color-mode__btn");

// Set up event listeners
toggleColorButtons.forEach(btn => {
    btn.addEventListener("click", toggleColorMode);
});

// This code assumes a Light Mode default
if (
    /* This condition checks whether the user has set a site preference for dark mode OR a OS-level preference for Dark Mode AND no site preference */
    localStorage.getItem('color-mode') === 'dark' ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches &&
        !localStorage.getItem('color-mode'))
) {
    // if true, set the site to Dark Mode
    document.documentElement.setAttribute('color-mode', 'dark')
}