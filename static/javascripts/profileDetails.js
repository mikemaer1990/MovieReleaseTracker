const leftScroll = document.querySelector('#slideLeftProfile');
const rightScroll = document.querySelector('#slideRightProfile');
const leftScrollPics = document.querySelector('#slideLeftProfilePics');
const rightScrollPics = document.querySelector('#slideRightProfilePics');
const profilePics = document.querySelector('.profilePicsPictures img')
const profileCover = document.querySelector('.profileRelatedMovieCover img')
const buttons = [leftScroll, rightScroll, leftScrollPics, rightScrollPics]

// buttons.forEach(button => button.addEventListener("click", (e) => {
//     const parentElement = e.target.parentElement.parentElement
//     let distance
//     console.log(e.target.parentElement.id === 'slideRightProfilePics');
//     if (e.target.parentElement.id == "slideRightProfilePics" || e.target.parentElement.id == "slideLeftProfilePics") {
//         distance = profilePics.scrollWidth * 2 + 8
//     } else if (e.target.parentElement.id == "slideRightProfile" || e.target.parentElement.id == "slideLeftProfile") {
//         distance = profileCover.scrollWidth * 2 + 8
//     }
//     sideScroll(parentElement, e.target.dataset.direction, 10, distance, 5)
// }))


leftScroll.addEventListener("click", (e) => {
    console.log(e.target.parentElement);
    const distance = profileCover.scrollWidth * 2 + 8
    const container = document.querySelector('#profileRelated');

    sideScroll(container, 'left', 10, distance, 5);
})

rightScroll.addEventListener("click", () => {
    const distance = profileCover.scrollWidth * 2 + 8
    const container = document.querySelector('#profileRelated');
    sideScroll(container, 'right', 10, distance, 5);
})

leftScrollPics.addEventListener("click", () => {
    const distance = profilePics.scrollWidth * 2 + 8
    const container = document.querySelector('.profilePics');
    sideScroll(container, 'left', 10, distance, 5);
})

rightScrollPics.addEventListener("click", () => {
    const distance = profilePics.scrollWidth * 2 + 8
    const container = document.querySelector('.profilePics');
    sideScroll(container, 'right', 10, distance, 5);
})

function sideScroll(element, direction, speed, distance, step) {
    scrollAmount = 0;
    let slideTimer = setInterval(function () {
        if (direction == "left") {
            element.scrollLeft -= step;
        } else if (direction == "right") {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        if (scrollAmount >= distance) {
            window.clearInterval(slideTimer)
        }
    }, speed);
}