const g1 = document.querySelector('#g1')
const refreshBtn = document.querySelector('.refresh-btn')

const server_ip = '145.93.148.94'




const updateSensors = () => {
    const ghsSvgs = document.querySelectorAll('.greenhouse')
    ghsSvgs.forEach(svg => {
        // access the svg document
        const svgDoc = svg.contentDocument;
        const sensors = svgDoc.querySelectorAll('.sensor_bg')
        sensors.forEach(element => {

            fetch(`http://${server_ip}:1234/get-sensor-data/${svg.id}/${element.id}`)
                .then(response => response.json())
                .then((data) => {
                    console.log(data)
                    if (data.display === 'green') {
                        element.setAttribute('fill', '#00FF00')
                    } else if (data.display === 'red') {
                        element.setAttribute('fill', '#FF0000')
                    } else if (data.display === 'none') {
                        element.setAttribute('fill', "#ced4da")
                    } else if (data.display === 'blue') {
                        element.setAttribute('fill', "#0000FF")
                    }
                })
                .catch(error => console.log("error:", error))
        });
    })
}

g1.addEventListener('load', () => {
    updateSensors()

    // add sensor event listeners 
    document.querySelectorAll('.greenhouse').forEach(greenhouse => {
        const sensors = greenhouse.contentDocument.querySelectorAll('.sensor_bg')

        sensors.forEach(sensor => {
            sensor.style.cursor = 'pointer'
            sensor.addEventListener('click', (e) => {
                // console.log('Print', greenhouse.id, sensor.id)
                window.location.href = `http://${server_ip}:1234/monitor/${greenhouse.id}/${sensor.id}`
            })
        })
    })
})

refreshBtn.addEventListener('click', (e) => {
    // console.log('Button clicked')
    updateSensors()
})

setInterval(updateSensors, 5000)
