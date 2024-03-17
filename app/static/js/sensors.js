console.log('hello world')

const svgGh1 = document.querySelector('#gh1_map')

svgGh1.addEventListener('load', () => {
    // access the svg document
    const svgDoc = svgGh1.contentDocument;
    const sensors = svgDoc.querySelectorAll('.sensor_bg')
    sensors.forEach(element => {
        element.setAttribute("fill", "#FF0000")
    });
})



