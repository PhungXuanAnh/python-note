"""
    pip install pyngrok

    https://pyngrok.readthedocs.io/en/latest/index.html
"""

from pyngrok import ngrok


def open_a_tunnel(port=80, protocal='http'):
    tunnel = ngrok.connect(port, protocal)
    return tunnel

def get_active_tunnel():
    tunnels = ngrok.get_tunnels()
    print(tunnels.public_url)

if __name__ == '__main__':
    # tn = open_a_tunnel()
    # get_active_tunnel()
    # ngrok_process = ngrok.get_ngrok_process()
    pass
