import unittest
import urllib
import urllib2
import subprocess
import threading
import time
import v2
import argparse
import sys

class TestRendezvous(unittest.TestCase):
    serverProcess = None
    serverAddress = "localhost:8080"
    useLocalServer = True

    @classmethod
    def setUpClass(self):
        if self.useLocalServer:
            print "Starting local server"
            self.serverProcess = subprocess.Popen(["python", "v2.py"])
            time.sleep(1)

    @classmethod
    def tearDownClass(self):
        if self.useLocalServer:
            self.serverProcess.kill()

    def test_new_returns_random_channel(self):
        channel1 = urllib2.urlopen("http://%s/new" % self.serverAddress).read()
        self.assertEqual(len(channel1), 32)
        channel2 = urllib2.urlopen("http://%s/new" % self.serverAddress).read()
        self.assertEqual(len(channel2), 32)
        self.assertNotEqual(channel1, channel2)

    def test_can_send_message_to_newly_created_channel(self):
        channel = urllib2.urlopen("http://%s/new" % self.serverAddress).read()
        self.assertEqual(len(channel), 32)
        self.called = False

        def read():
            data = urllib2.urlopen("http://%s/channel/%s" % (self.serverAddress, channel)).read()
            self.assertEqual(data, "a=1&b=2")
            self.called = True

        def write():
            url = 'http://%s/channel/%s' % (self.serverAddress, channel)
            data = urllib.urlencode({'a':'1', 'b':'2'})
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
       
        readThread = threading.Thread(target=read)
        readThread.start()
        writeThread = threading.Thread(target=write)
        writeThread.start()
        readThread.join()
        writeThread.join()
        self.assertTrue(self.called)
    
    def test_can_send_message_to_arbitrary_channel(self):
        channel = "channel"
        self.called = False

        def read():
            data = urllib2.urlopen("http://%s/channel/%s" % (self.serverAddress, channel)).read()
            self.assertEqual(data, "a=1&b=2")
            self.called = True

        def write():
            url = 'http://%s/channel/%s' % (self.serverAddress, channel)
            data = urllib.urlencode({'a':'1', 'b':'2'})
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
       
        readThread = threading.Thread(target=read)
        readThread.start()
        writeThread = threading.Thread(target=write)
        writeThread.start()
        readThread.join()
        writeThread.join()
        self.assertTrue(self.called)
    
    def test_read_twice_from_same_channel_results_in_404_error(self):
        channel = "mychannel"
        self.caughtException = False
        self.called = False

        def read():
            data = urllib2.urlopen("http://%s/channel/%s" % (self.serverAddress, channel)).read()
            self.assertEqual(data, "a=555&b=555")
            self.called = True
       
        readThread = threading.Thread(target=read)
        readThread.start()
        time.sleep(0.5)      
 
        try:
            urllib2.urlopen("http://%s/channel/%s" % (self.serverAddress, channel)).read()
        except urllib2.HTTPError as e:
            self.caughtException = True
            self.assertEqual(e.code, 404)

        self.assertTrue(self.caughtException)
        
        ## Writes to the channel just to clean the thread clean    
        url = 'http://%s/channel/%s' % (self.serverAddress, channel)
        data = urllib.urlencode({'a':'555', 'b':'555'})
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        readThread.join()

        self.assertTrue(self.called)

    def test_write_twice_to_same_channel_results_in_404_error(self):
        channel = "mychannelchannel"
        self.caughtException = False

        def write():
            url = 'http://%s/channel/%s' % (self.serverAddress, channel)
            data = urllib.urlencode({'a':'10', 'b':'20'})
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
       
        writeThread = threading.Thread(target=write)
        writeThread.start()
        time.sleep(0.5)      
 
        url = 'http://%s/channel/%s' % (self.serverAddress, channel)
        data = urllib.urlencode({'a':'1', 'b':'2'})
        req = urllib2.Request(url, data)
        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            self.caughtException = True
            self.assertEqual(e.code, 404)

        self.assertTrue(self.caughtException)
        
        ## Reads the data just to clean the thread clean    
        data = urllib2.urlopen("http://%s/channel/%s" % (self.serverAddress, channel)).read()
        self.assertEqual(data, "a=10&b=20")
        writeThread.join()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--server')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()
    if args.server is not None:
        TestRendezvous.serverAddress = args.server
        TestRendezvous.useLocalServer = False

    sys.argv[1:] = args.unittest_args
    
    unittest.main()



