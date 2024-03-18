const g1 = document.querySelector('#g1')
const refreshBtn = document.querySelector('.refresh-btn')

const server_ip = '145.93.148.94'

const updateSensors = () => {
    // access the svg document
    const svgDoc = g1.contentDocument;
    const sensors = svgDoc.querySelectorAll('.sensor_bg')
    sensors.forEach(element => {

        fetch(`http://${server_ip}:1234/get-sensor-data/${g1.id}/${element.id}`)
            .then(response => response.json())
            .then((data) => {
                console.log(data.display)
                if (data.display) {
                    element.setAttribute('fill', '#00FF00')
                } else {
                    element.setAttribute('fill', '#FF0000')
                }
            })
            .catch(error => console.log("error:", error))
    });
}

g1.addEventListener('load', () => {
    updateSensors()
})

refreshBtn.addEventListener('click', (e) => {
    // console.log('Button clicked')
    updateSensors()
})

setInterval(updateSensors, 5000)
