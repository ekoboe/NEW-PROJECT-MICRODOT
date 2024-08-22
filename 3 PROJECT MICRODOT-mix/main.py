from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
from powerLab import POWERlab
import ujson
import random

app = Microdot()
Response.default_content_type = 'text/html'

bz = POWERlab(14) # BUZZER


@app.route('/')  # Rute URL
async def index(request):
    return render_template('index.html')  # Render Template index.html


@app.route('/updateData')  # Rute URL
async def get_sensor_data(request):
    ip = "192.168.5.10"  # Inisialisasi variabel untuk mengambil alamat IP
    # Membaca nilai dari sensor BME-280
    sensor_reads_temp = random.uniform(10, 60)

    # Mengembalikan data sensor dan IP ke format JSON
    return ujson.dumps({
        "readingTemp": sensor_reads_temp,  # Data Suhu ke format JSON
        "ip": ip  # Data IP yang digunakan ke format JSON
    })


@app.route("/ws")  # Rute WebSocket
@with_websocket
async def kontrolButton(request, ws):  # Membuat fungsi untuk mengontrol Button yang ada di website
    while True:  # Loop yang berjalan terus-menerus untuk menangani pesan WebSocket
        data = await ws.receive()  # Menunggu dan menerima pesan WebSocket
        print(data)
        if data == 'on4':
            bz.onPower()
        if data == 'off4':
            bz.offPower()

        await ws.send("OK")  # Mengirim respons 'OK' kembali ke klien

@app.route('/static/<path:path>')  # Rute pelayanan file statis dari directory 'static'
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)  # Mengirim file yang diminta

@app.route('/shutdown')  # Rute untuk mematikan server
async def shutdown(request):
    request.app.shutdown()  # Mematikan server microdot
    return 'The server is shutting down...'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')  # di run dalam mode debug dengan IP