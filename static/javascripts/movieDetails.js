// Trailer lightbox plugin
$(window).on('load', function () {
    var img = $("#exampleImage");

    var configObject = {
        sourceUrl: img.attr("data-videourl"),
        triggerElement: "#" + img.attr("id"),
        progressCallback: function () {
            console.log("Callback Invoked.");
        }
    };
    if (configObject.sourceUrl) {
        var videoBuild = new YoutubeOverlayModule(configObject);
        videoBuild.activateDeployment();
    }
});

// Script for scrolling through related movies
const leftScroll = document.querySelector('#slideLeft');
const rightScroll = document.querySelector('#slideRight');
const cover = document.querySelector('.relatedMovieCover img')

if (leftScroll) {
    leftScroll.addEventListener("click", () => {
        const distance = cover.scrollWidth * 2 + 8
        const container = document.querySelector('#related');
        sideScroll(container, 'left', 10, distance, 5);
    })
}
if (leftScroll) {
    rightScroll.addEventListener("click", () => {
        const distance = cover.scrollWidth * 2 + 8
        const container = document.querySelector('#related');
        sideScroll(container, 'right', 10, distance, 5);
    })
}

// Calculate what to scroll and how far
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