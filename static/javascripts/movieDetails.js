const leftScroll = document.querySelector('#slideLeft');
const rightScroll = document.querySelector('#slideRight');

leftScroll.addEventListener("click", () => {
    const container = document.querySelector('#related');
    sideScroll(container, 'left', 10, 470, 10);
})

rightScroll.addEventListener("click", () => {
    const container = document.querySelector('#related');
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