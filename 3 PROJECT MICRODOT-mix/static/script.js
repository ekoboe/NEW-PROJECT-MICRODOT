                /* TEMPERATURE GAUGE */

// FUNGSI UNTUK MENGAMBIL DATA SUHU AKTUAL DARI SERVER
function fetchTemperatureData() {
    return fetch(`/updateData`)
        .then((response) => response.json())
        .then(data => {
            return data.readingTemp; // MENDAPARKAN NILAI SUHU DARI SERVER
        })
        .catch(error => {
            console.error("Error fetching temperature data:", error);
            return 0; // MENGEMBALIKAN NILAI 0 JIKA TERJADI ERROR
        });
}

// FUNGSI UNTUK MEMPERBARUI SUHU
function updateTemperatureGauge() {
    const gaugeElement = document.querySelector(".gauge-card-1 .gauge");
    fetchTemperatureData()
        .then(temperatureInCelsius => {
            const normalizedTemperature = temperatureInCelsius / 100; // NORMALISASI NILAI SUHU DARI RANGE O KE 1
            setTemperatureGaugeValue(gaugeElement, normalizedTemperature);
            setTimeout(updateTemperatureGauge, 6000); // MEMPERBARUI SETIAP 6 DETIK
        });
}

// FUNGSI UNTUK MENGATUR NILAI SUHU
function setTemperatureGaugeValue(gauge, value) {
    if (value < 0 || value > 1) {
        return;
    }
    const angle = value * 180; // MENGKONVERSI NILAI YANG DINORMALISASI MENJADI SUDUT (0 HINGGA 180 DERAJAT)
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${angle}deg)`;
    gauge.querySelector(".gauge__cover").textContent = `${Math.round(value * 100)}°C`; // DISPLAY SATUAN SUHU YAITU CELCIUS
}
updateTemperatureGauge(); // MEMULAI MEMPERBARUI NILAI SUHU



                /* LINE CHART PADA CARD SUHU */

// FUNGI UNTUK MEMPERBARUI CHART DATA DAN LABEL
function updateChart(chart, temperatureData, label) {
    if (chart.data.labels.length >= 30) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(temperatureData);
    chart.update();
}

// FUNGSI UNTUK MEMBUAT LINE CHART PADA CARD SUHU
function createLineChart() {
    const ctx = document.getElementById('lineChart').getContext('2d');
    const lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: '#E7D7C4',
                    backgroundColor: 'rgba(255, 133, 81, 0.2)',
                    tension: 0.4,
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'category',
                    display: true,
                    grid: {
                        display: false,
                    },
                },
                y: {
                    display: true,
                    grid: {
                        display: true,
                    },
                },
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                },
            },
        },
    });

    return lineChart;
}

// FUNGSI UNTUK MEMPERBARUI LINE CHART SETIAP 6 DETIK
function startUpdatingChart() {
    const lineChart = createLineChart();
    setInterval(async () => {
        const temperatureData = await getActualTemperatureData();
        const currentTime = moment().format('HH:mm');
        updateChart(lineChart, temperatureData, currentTime);
    }, 6000); // MENGATUR INTERVAL KE 6 DETIK
}

// FUNGSI UNTUK MENGAMBIL DATA AKTUAL SUHU DARI SERVER
async function getActualTemperatureData() {
    const response = await fetch('/updateData');
    const data = await response.json();
    return data.readingTemp;
}
startUpdatingChart(); // UNTUK MEMULAI PEMBARUAN LINE CHART

// MENGAMBIL DATA IP DARI SERVER
async function fetchIpData() {
    try {
        const response = await fetch('/updateData');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('Error fetching IP data:', error);
        return '0.0.0.0'; // MENAMPILKAN IP 0.0.0.0 JIKA TERJADI KESALAHAN ATAU ERROR
    }
}

// MEMPERBARUI TAMPILAN IP PADA HALAMAN WEB
async function updateIpDisplay() {
    const displayElement = document.querySelector('.ip h3');
    try {
         const ipAddress = await fetchIpData();
        displayElement.textContent = `${ipAddress}`; // MENAMPILKAN ALAMAT IP DI ELEMEN YANG DIPILIH
        setTimeout(updateIpDisplay, 6000); // MENGULANGI PEMBARUAN SETIAP 6 DETIK
    } catch (error) {
        console.error('Error updating IP display:', error);
    }
}
updateIpDisplay(); // MEMANGGIL FUNCTION UNTUK MENGUPDATE IP