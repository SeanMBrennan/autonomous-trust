import os
import asyncio
import quart

from . import network_graph as ng
from .middleware import SassASGIMiddleware

default_port = 8000
initial_size = 12


def web_visuals(directory, port, debug, size):
    print(' * Directory on host: %s' % directory)
    appname = __package__.split('.')[0]
    app = quart.Quart(appname,
                      static_url_path='', static_folder=directory, template_folder=directory)
    app.debug = True

    os.environ['PATH_INFO'] = '/scss/tekfive.scss'
    app.asgi_app = SassASGIMiddleware(app, {appname: (os.path.join(directory, 'scss'),
                                                      os.path.join(directory, 'css'), '/css', True)})

    @app.route("/")
    async def page():
        return await quart.render_template("index.html")  # noqa

    @app.websocket('/ws')
    async def ws():
        graph = None
        while True:
            msg = await quart.websocket.receive()
            if graph is None:
                for impl in ng.Graphs.Implementation:  # noqa
                    if msg == impl.value:
                        graph = ng.Graphs.get_graph(impl.value, size, debug)
                        print(' * Simulating %s network graph' % msg)
            if msg == 'done':
                print(' * Simulation done')
                break
            seconds, data, stop = graph.get_update()
            if stop:
                break
            if data is not None:
                await quart.websocket.send(data)
            await asyncio.sleep(seconds)

    app.run(port=port)