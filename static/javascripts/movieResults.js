const loginBtn = [...document.querySelectorAll('#details_login_button')]
const detailsBtn = [...document.querySelectorAll('#details_button')]
const movieTile = [...document.querySelectorAll('#movieContainer')]

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


movieTile.forEach(movie => movie.addEventListener("click", handleClick))

function handleClick() {
    location.href = this.dataset.url
}