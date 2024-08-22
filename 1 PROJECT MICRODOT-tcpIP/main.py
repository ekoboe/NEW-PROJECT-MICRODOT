from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
import ujson
import random

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
async def index(request): 
    return render_template('index.html')

@app.route('/updateData')
async def get_sensor_data(request):
    ip= '192.168.5.31'
    sensor_reads_temp = random.uniform(10, 60)
    
    return ujson.dumps({
        "readingTemp": sensor_reads_temp,
        "ip":ip
    })

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
