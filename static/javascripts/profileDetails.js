const leftScroll = document.querySelector('#slideLeftProfile');
const rightScroll = document.querySelector('#slideRightProfile');
const leftScrollPics = document.querySelector('#slideLeftProfilePics');
const rightScrollPics = document.querySelector('#slideRightProfilePics');

leftScroll.addEventListener("click", () => {
    const container = document.querySelector('#profileRelated');
    sideScroll(container, 'left', 10, 470, 10);
})

rightScroll.addEventListener("click", () => {
    const container = document.querySelector('#profileRelated');
    sideScroll(container, 'right', 10, 470, 10);
})

leftScrollPics.addEventListener("click", () => {
    const container = document.querySelector('.profilePics');
    sideScroll(container, 'left', 10, 470, 10);
})

rightScrollPics.addEventListener("click", () => {
    const container = document.querySelector('.profilePics');
    sideScroll(container, 'right', 10, 470, 10);
})

function sideScroll(element,direction,speed,distance,step) {
    scrollAmount = 0;
    let slideTimer = setInterval(function() {
        if (direction == "left") {
            element.scrollLeft -= step;
        } else if (direction == "right") {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        if(scrollAmount >= distance) {
            window.clearInterval(slideTimer)
        }
    }, speed);
}