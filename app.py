from base import app

port = 2348

app.run(threaded=True, debug=True, port=port)
