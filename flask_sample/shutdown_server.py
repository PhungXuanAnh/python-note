from flask import Flask, request
app = Flask(__name__)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST', 'PATCH'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run()
    
    #####################################
    # Another approach is using multiprocess
    from multiprocessing import Process
    server = Process(target=app.run)
    server.start()
    # do something...
    server.terminate()
    server.join()