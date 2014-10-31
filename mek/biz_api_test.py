import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'wc2bvMApMYXh9oOBX_o79g'
CONSUMER_SECRET = '8SQFO_jaTYCeykVGYYcVnlVFJMQ'
TOKEN = '3QMwXCnwAm89Pf2Vd47Dreg5CUNAI1ns'
TOKEN_SECRET = 'Onq9MyCAe58CEp6Q1OnZRmeD5XQ'

url = 'http://{0}{1}?{2}'.format(API_HOST, BUSINESS_PATH, {})
consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
oauth_request = oauth2.Request('GET', url, {})
oauth_request.update(
{
'oauth_nonce': oauth2.generate_nonce(),
'oauth_timestamp': oauth2.generate_timestamp(),
'oauth_token': TOKEN,
'oauth_consumer_key': CONSUMER_KEY
}
)
token = oauth2.Token(TOKEN, TOKEN_SECRET)
oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
signed_url = oauth_request.to_url()

print 'Querying {0} ...'.format(url)

conn = urllib2.urlopen(signed_url, None)
try:
    response = json.loads(conn.read())
finally:
    conn.close()
print response
