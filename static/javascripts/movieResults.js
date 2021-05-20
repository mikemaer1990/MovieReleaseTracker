const loginBtn = [...document.querySelectorAll('#details_login_button')]
const detailsBtn = [...document.querySelectorAll('#details_button')]
const movieTile = [...document.querySelectorAll('#movieContainer')]
const movieTitleP = [...document.querySelectorAll('#movie-container-title')]

// Alternate colors for the follow and details buttons on the details page
if (loginBtn.length != 0) {
    loginBtn.forEach(button => button.addEventListener("mouseover", () => {
        detailsBtn[loginBtn.indexOf(button)].classList.add("light-hover-btn")
    }))
    loginBtn.forEach(button => button.addEventListener("mouseleave", () => {
        detailsBtn[loginBtn.indexOf(button)].classList.remove("light-hover-btn")
    }))
    detailsBtn.forEach(button => button.addEventListener("mouseover", () => {
        loginBtn[detailsBtn.indexOf(button)].classList.add("dark-hover-btn")
    }))
    detailsBtn.forEach(button => button.addEventListener("mouseleave", () => {
        loginBtn[detailsBtn.indexOf(button)].classList.remove("dark-hover-btn")
    }))
}

// Listen for clicks on the movie containers
movieTile.forEach(movie => movie.addEventListener("click", (e) => {
    handleClick(e)
}))

// Go to the dataset-url 
function handleClick(e) {
    if (e.target.classList.contains("btnGroup")) return
    const url = e.target.dataset.url || e.target.parentElement.dataset.url || e.target.parentElement.parentElement.dataset.url
    location.href = url
}

// Listen for mouseover and leave events on the movie containers and change the title to the full length version - if it has been cut off

movieTitleP.forEach(title => title.parentElement.parentElement.addEventListener("mouseover", () => {
    title.innerText = title.dataset.title;
}))
// Revert to abbreviated title once mouse
movieTitleP.forEach(title => title.parentElement.parentElement.addEventListener("mouseleave", () => {
    if (title.innerText.length > 18) {
        title.innerText = title.dataset.title.slice(0, 18) + '...';
    }
}))