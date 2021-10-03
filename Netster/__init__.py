import time
import socket
import speedtest
import multiprocessing

__all__ = ["Netster"]

class Netster:
    def __init__(self):
        self._speedTester = speedtest.Speedtest()
        self._pingAddresses = ["1.1.1.1"] # Cloudflare's DNS address
        self._timeout = -1 # Will be added later

    def ping(self):
        results = {}
        for i in range(len(self._pingAddresses)):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if (self._timeout != -1):
                pass
            past = time.time()
            try:
                sock.connect((self._pingAddresses[i], 80))
                results.update({self._pingAddresses[i] : time.time() - past})
                sock.shutdown(socket.SHUT_RDWR)
            except:
                results.update({self._pingAddresses[i] : -1.0})
        return results

    def speedtest(self):
        for i in b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            try:
                self._speedTester.get_closest_servers()
                self._speedTester.get_best_server()
                break
            except:
                pass
        else:
            return (0,0)
        self._speedTester.download(threads=12)
        self._speedTester.upload(threads=multiprocessing.cpu_count())
        results = self._speedTester.results.dict()
        return (results["download"]/1000000, results["upload"]/1000000)

    def add_ping_address(self, iph):
        if type(iph) == type(""):
            if (iph not in self._pingAddresses):
                self._pingAddresses.append(iph)
            return
        raise Exception("IP or Hostname not a string")

    def remove_ping_address(self, input):
        try:
            del self._pingAddresses[input]
        except:
            self._pingAddresses.remove(input)