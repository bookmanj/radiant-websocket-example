#!/usr/bin/env python3

from twisted.internet import reactor, protocol
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS
from twisted.python.log import startLogging, msg
import sys


class ProcessProtocol(protocol.ProcessProtocol):
  """ I handle a child process launched via reactor.spawnProcess.
  I just buffer the output into a list and call WebSocketProcessOutputterThingFactory.broadcast when
  any new output is read
  """

  def __init__(self, websocket_factory):
    self.ws = websocket_factory
    self.buffer = []

  def outReceived(self, message):
    self.ws.broadcast(message)
    self.buffer.append(message)
    self.buffer = self.buffer[-10:]  # Last 10 messages please

  def errReceived(self, data):
    print("Error: %s" % data)


# https://autobahn.ws/python
class WebSocketProcessOutputterThing(WebSocketServerProtocol):
  """ I handle a single connected client. We don't need to do much here, simply call the register and un-register
  functions when needed.
  """

  def onOpen(self):
    self.factory.register(self)
    for line in self.factory.process.buffer:
      self.sendMessage(line)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    #super(WebSocketProcessOutputterThing, self).connectionLost(self, reason)
    self.factory.unregister(self)


class WebSocketProcessOutputterThingFactory(WebSocketServerFactory):
  """ I maintain a list of connected clients and provide a method for pushing a single message to all of them.
  """
  protocol = WebSocketProcessOutputterThing

  def __init__(self, *args, **kwargs):
    WebSocketServerFactory.__init__(self, *args, **kwargs)
    #super(WebSocketProcessOutputterThingFactory, self).__init__(self, *args, **kwargs)
    self.clients = []
    self.process = ProcessProtocol(self)
    reactor.spawnProcess(self.process, COMMAND_NAME, COMMAND_ARGS, {}, usePTY=True)

  def register(self, client):
    msg("Registered client %s" % client)
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    msg("Unregistered client %s" % client)
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, message):
    for client in self.clients:
      client.sendMessage(message)
