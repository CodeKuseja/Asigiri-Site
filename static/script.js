// Check whether the page was reached through an internal action
const internalNavigation = sessionStorage.getItem("internalNavigation");

// Get the loader and website content
const loader = document.getElementById("loader");
const content = document.getElementById("content");


// If this was an internal navigation/search, skip the loader
if (internalNavigation === "true") {

    loader.style.display = "none";
    content.style.display = "block";

    // Remove it so a manual refresh can show the loader again
    sessionStorage.removeItem("internalNavigation");

} else {

    // Show loading screen
    loader.style.display = "block";
    content.style.display = "none";

    // Wait before showing the website
    setTimeout(function () {

        loader.style.display = "none";
        content.style.display = "block";

    }, 2000);
}


// --------------------------------------------------
// SEARCH FORM
// --------------------------------------------------

const searchForm = document.querySelector(".search-container");

if (searchForm) {

    searchForm.addEventListener("submit", function () {

        // Tell the next page load to skip the loader
        sessionStorage.setItem("internalNavigation", "true");

    });

}


// --------------------------------------------------
// NAVIGATION LINKS
// --------------------------------------------------

const navigationLinks = document.querySelectorAll("nav a");

navigationLinks.forEach(function (link) {

    link.addEventListener("click", function () {

        // Skip loader when moving between website pages
        sessionStorage.setItem("internalNavigation", "true");

    });

});