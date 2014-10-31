# -*- coding: utf-8 -*-
"""
Yelp API v2.0 code sample.

This program demonstrates the capability of the Yelp API version 2.0
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/documentation for the API documentation.

This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
import os
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import re
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


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    encoded_params = urllib.urlencode(url_params)

    url = 'http://{0}{1}?{2}'.format(host, path, encoded_params)

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

    #print 'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term.encode('utf-8','replace'),
        'location': location.encode('utf-8','replace'),
        'limit': SEARCH_LIMIT
    }

    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location,data):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    #print term.encode('utf-8')
    try:
        #query_api(data["name"].decode('utf8'), data["full_address"].decode('utf8'))
        response = search(term.decode('iso-8859-1'), location.decode('iso-8859-1'))
    except UnicodeEncodeError as error:
        f4.write((term+';'+location+';'+'\n').encode('utf8'))
        print term,';',location
        return

    businesses = response.get('businesses')

    if not businesses:
        print 'No businesses for {0} in {1} found.'.format(term, location)
        f2.write(term+';'+location+'\n')
        return
    count=0
    choice=0
    if len(businesses) > 1:
        flag=1
        for b in businesses:
            if ((b['name']==term) and ((' '.join(b['location']['display_address']))==location)):
                choice=count
                flag=0
                break
            else :
                count+=1
        if flag==1:
            count=0
            choice=0
            print ">>>>>>>>>USER ATTENTION>>>>"
            for b in businesses:
                print count,'->',b
                count+=1
                print '#################'
            print "USER ENTER CHOICE FROM 0 TO "+str(count)
            #choice=input()
            choice=-1
    if choice != -1:
        business_id = businesses[choice]['id']
        response = get_business(business_id)
        f1.write((response["name"]+';'+ business_id+';'+response["url"]+'\n').encode('utf8'))
    else :
        #temp=raw_input("enter web link manually>>>>")
        temp="YYYY"
        f3.write(term+';'+location+'\n')
        #f1.write((term+';'+ "XXX"+';'+temp+'\n').encode('utf8'))        
        
#    print '{0} businesses found, querying business info for the top result "{1}" ...'.format(
#        len(businesses),
#        business_id
#    )


    #print 'Result for business "{0}" found:'.format(business_id)
    #pprint.pprint(response["url"], indent=2)
    


def main(data):
#    parser = argparse.ArgumentParser()

#    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
#    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
    
    try:
        #query_api(data["name"].decode('utf8'), data["full_address"].decode('utf8'))
        query_api(re.sub('\n',' ',data["name"]),re.sub('\n',' ',data["full_address"]),data)
    except urllib2.HTTPError as error:
        f4.write((re.sub('\n',' ',data["name"])+';'+re.sub('\n',' ',data["full_address"])+';'+'\n').encode('utf8'))
        return

if __name__ == '__main__':
    num=1
    data_dir="/home/karthik/yelp/mek/yelp_dataset_challenge_academic_dataset"
    data_gen_dir="/home/karthik/yelp/mek/data_generated"
    biz_file=os.path.join(data_dir,"yelp_academic_dataset_business.json")
    #biz_file=os.path.join(data_dir,"test.json")
    file=open(biz_file,'r')
    #f=open(os.path.join(data_gen_dir,"biz_names.dat"),'w')
    #count=1
    data_gen_dir="/home/karthik/yelp/mek/data_generated"
    f1=open(os.path.join(data_gen_dir,"biz_urls.dat"),'w')
    f2=open(os.path.join(data_gen_dir,"biz_urls_not_there.dat"),'w')
    f3=open(os.path.join(data_gen_dir,"biz_urls_closed.dat"),'w')        
    f4=open(os.path.join(data_gen_dir,"encode_error.dat"),'w')
    for line in file:
        #print line.strip()
        data=json.loads(line.strip('\n'))
        #print data["name"].encode('utf8')
        #print count,' ',data["name"]
        #print data["name"]
        #f.write(data["name"].encode('utf8')+';'+data["full_address"].encode('utf8')+'\n')
    #data=1
        print num
        num+=1
        main(data)
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    #f.close()
    #file.close();
