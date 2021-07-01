window.onload = function () {
    const timeDiv = document.createElement('h2')
    timeDiv.innerText = new Date().toLocaleTimeString()
    setInterval(() => {
        timeDiv.innerText = new Date().toLocaleTimeString()
    }, 1000)
    document.querySelector('.overlay').appendChild(timeDiv)
    fetch("https://type.fit/api/quotes")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            const quote = data[randy(data.length)]
            document.querySelector('h1').innerText = quote.text
            document.querySelector('span').innerText = `- ${quote.author}`
        });


    const randy = (max) => {
        return Math.floor(Math.random() * max)
    }
}