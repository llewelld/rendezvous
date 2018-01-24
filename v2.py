from channel import Channel
from response import Ok
from twisted.web.server import Site
from twisted.web.resource import Resource, NoResource
from twisted.internet.error import AlreadyCalled, AlreadyCancelled
from twisted.internet import reactor
import uuid
import argparse


_REQUEST_TIMEOUT = 40 
_CHANNEL_CLOSE_TIMEOUT = 1800
_CHANNEL_CLOSE_ENABLED = True

assert(_REQUEST_TIMEOUT < 60) # nginx default is 60, and this must be less.
assert(_REQUEST_TIMEOUT < _CHANNEL_CLOSE_TIMEOUT)


def _close_channel(channel, channels):
    #If a global channel timeout on that channel is set, cancel it.
    try:
        channel.close_call.cancel()
    except AttributeError:
        pass
    channel.close()
    del channels[channel.name]


class NewChannelResource(Resource):
    def __init__(self, channels, fixed):
        Resource.__init__(self)
        self._channels = channels
        self._fixed = fixed

    def render_GET(self, request):
        # Get channel name, either fixed for debugging or random
        if self._fixed:
            name = self._fixed
        else:
            name = uuid.uuid4().hex

        # Close any existing channel of the same name
        # TODO: Is this a good idea?
        existing = self._channels.get(name, None)
        if existing:
            _close_channel(existing, self._channels)
        
        return name


class ChannelsResource(Resource):
    def __init__(self, channels, reactor):
        Resource.__init__(self)
        self.channels = channels
        self.reactor = reactor

    def getChild(self, name, request):
        channel = self.channels.get(name, None)
        if channel is None:
            # Make the new channel
            channel = Channel(name, self.reactor, _REQUEST_TIMEOUT) 
            self.channels[name] = channel

            # Make the long-term inactivity close call
            if _CHANNEL_CLOSE_ENABLED:
                channel.close_call = self.reactor.callLater(
                   _CHANNEL_CLOSE_TIMEOUT, _close_channel, channel, self.channels)

            # This header lets JavaScripts on other websites use the results of
            # this resource
            request.setHeader('Access-Control-Allow-Origin', '*')

            print('Created new channel: ' + str(channel))
        
        return ChannelResource(channel, self.channels)


class ChannelResource(Resource):
    def __init__(self, channel, channels):
        Resource.__init__(self)
        self._channels = channels
        self._channel = channel

    # Write
    def render_POST(self, request):
        data = request.content.read()
        print("Write to channel '{}': {}".format(self._channel.name, data))
        print(self._channel)
        r = self._channel.write(request, data)
        print(self._channel)

        # This header lets JavaScripts on other websites use the results of
        # this resource
        request.setHeader('Access-Control-Allow-Origin', '*')

        return r
        
    # Read
    def render_GET(self, request):
        print("Read from channel '{}'".format(self._channel.name))
        print(self._channel)
        r = self._channel.read(request)
        print(self._channel)

        # This header lets JavaScripts on other websites use the results of
        # this resource
        request.setHeader('Access-Control-Allow-Origin', '*')

        return r

    # Close channel
    def render_DELETE(self, request):
        print("Closing channel '{}'".format(self._channel.name))
        try:
            _close_channel(self._channel, self._channels)
        except (AlreadyCancelled, AlreadyCalled):
            # Fine
            pass

        # This header lets JavaScripts on other websites use the results of
        # this resource
        request.setHeader('Access-Control-Allow-Origin', '*')

        return Ok().render(request)

def start_rendezvous_server(port = 8080, fixed = None):
    channels = dict()
    root = Resource()
    root.putChild("channel", ChannelsResource(channels, reactor))
    root.putChild("new", NewChannelResource(channels, fixed))

    factory = Site(root)

    reactor.listenTCP(port, factory)
    reactor.run()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', type=int, default=8080, 
        help='port to run rendezvous server on')
    parser.add_argument(
        '-f', '--fixed',
        help='fixed channel name (debug only)')
    args = parser.parse_args()

    print('Starting rendezvous server on port {}...'.format(args.port))
    start_rendezvous_server(args.port, args.fixed)

