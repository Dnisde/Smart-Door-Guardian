from requests import exceptions
import argparse
import requests
import cv2
import os
# construct the argument parser and parse the arguments

API_KEY = "ed7345f16ba942ab9ac8024406e531f1"
MAX_RESULTS = 250
GROUP_SIZE = 50

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True, help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
args = vars(ap.parse_args())

URL = "https://api.bing.microsoft.com/"
# working with network requests there are a number of exceptions that can be thrown
EXCEPTIONS = set([IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout])

# Store the search term in a convenience variable then set the headers and search parameters
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

# Doing the search
print("[INFO] searching Images through Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

# Grab the results from the search into Json format: including the total number of
results = search.json()
# Estimated results returned by the Bing API
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)

print("[INFO] {} total results for '{}'".format(estNumResults, term))
# initialize the total number of images downloaded thus far
total = 0

# loop over the estimated number of results in `GROUP_SIZE` groups
for offset in range(0, estNumResults, GROUP_SIZE):
	# update the search parameters using the current offset, then
	# make the request to fetch the results
	print("[INFO] making request for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
	
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	print("[INFO] saving images for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))
