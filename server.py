#!/usr/bin/env python
import os
import io
import sys
import fnmatch
import yaml
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json

def get_holidays():
    """
    Loop through all conf files for every country and return all holidays
    :return: array
    """
    countries = []
    errors = []
    walk_dir = "./conf"
    for root, dirnames, filenames in os.walk(walk_dir):
        for filename in fnmatch.filter(filenames, '*.yml'):
            file = os.path.join(root, filename)
            print("Processing %s" % file)
            with io.open(file, "r", encoding="utf-8") as stream:
                try:
                    item = yaml.safe_load(stream)
                    country_code = (os.path.split(os.path.dirname(file)))[1]
                    item['country'] = country_code
                    countries.append(item)
                except yaml.YAMLError as exc:
                    errors.append(exc)
    return countries, errors

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)

        #Get a list of holidays for all countries
        items, errors = get_holidays()
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'items': items,
            'errors': errors
        }).encode())
        return

if __name__ == '__main__':
    server = HTTPServer(('', 8000), RequestHandler)
    server.serve_forever()