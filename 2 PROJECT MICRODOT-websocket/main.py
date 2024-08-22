from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
from powerLab import POWERlab
import ujson


app = Microdot()
Response.default_content_type = 'text/html'

bz = POWERlab(2)
bz.offPower()

   
@app.route('/')
async def index(request): 
    return render_template('index.html')

@app.route('/updateData')
async def get_sensor_data(request):
    print("Receive get data request!")
    ip= '192.168.5.31'
    
    return ujson.dumps({
        "ip":ip
    })

@app.route("/ws")
@with_websocket
async def kontrolButton(request, ws):
    while True:
        data = await ws.receive()
        print(data)
        if data == 'on4':
            bz.onPower()
        if data == 'off4':
            bz.offPower()
            
        await ws.send("OK")

@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')