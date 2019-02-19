#!/usr/bin/env python3
import cgi
from cgitb import enable
enable()  # Traceback. Comment out in production

import json
import os

# Response Headers
print('Content-Type: text/html')
print()  # End of headers

# Use os and json to populate the techtalks section
talks = []
for name in sorted(os.listdir('techtalks')):
    path = 'techtalks/%s' % name
    if os.path.isdir(path):
        # Assume that it is a techtalk
        # Open the meta.json
        with open('%s/meta.json' % path) as f:
            meta = json.load(f)
            for k, v in meta.items():
                meta[k] = str(v).lower()
        talks.append("""<a href="/%(path)s/" target="_blank" class="card">
                            <h2>%(title)s</h2>
                            <img src="/%(path)s/title.png" alt="%(title)s title slide" />
                            <p><em>%(quote)s</em></p>
                        </a>""" % ({'path': path, **meta}))

# Response Body
print("""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>freyamade some techtalks</title>
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <meta name="author" content="freyamade" />
        <meta name="description" content="freyamade some techtalks for netsoc and they're pretty cool" />
        <link href="//fonts.googleapis.com/css?family=Montserrat:200" rel="stylesheet" type="text/css">
        <link href="style.css" type="text/css" rel="stylesheet" />
        <meta property="og:title" content="freyamade" />
        <meta property="og:url" content="http://%(http_host)s%(request_uri)s" />
        <meta property="og:image" content="http://freyamade.netsoc.co/demo.png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:site_name" content="freyamade.netsoc.co" />
        <meta property="fb:admins" content="1385961037" />
        <meta property="og:description" content="freyamade a netsoc homepage" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:site" content="@freyamade" />
        <meta name="twitter:description" content="freyamade a netsoc homepage" />
        <meta itemprop="image" content="http://freyamade.netsoc.co/demo.png" />
    </head>
    <body>
        <div class="container">
            <div class="content">
                <div class="title">techtalks</div>
                <div class="cards">
                    %(cards)s
                </div>
            </div>
            <a href="https://github.com/freyamade/" class="social-link" target="blank">my github</a>
        </div>
    </body>
</html>
""" % ({
    'http_host': os.environ.get('HTTP_HOST', ''),
    'request_uri': os.environ.get('REQUEST_URI', ''),
    'cards': ''.join(talks),
}))
