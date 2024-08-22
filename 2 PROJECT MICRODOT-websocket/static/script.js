// MENGAMBIL DATA IP DARI SERVER
async function fetchIpData() {
    try {
        const response = await fetch('/updateData');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('Error fetching IP data:', error);
        return '0.0.0.0'; // Return a default IP address in case of error
    }
}

// MEMPERBARUI TAMPILAN IP PADA HALAMAN WEB
async function updateIpDisplay() {
    const displayElement = document.querySelector('.ip h3');

    try {
         const ipAddress = await fetchIpData();
        displayElement.textContent = `${ipAddress}`; // Display IP address in the selected element

        // Repeat the update every 6 seconds
        setTimeout(updateIpDisplay, 6000);
    } catch (error) {
        console.error('Error updating IP display:', error);
    }
}

// MEMANGGIL FUNCTION UNTUK MENGUPDATE IP
updateIpDisplay();