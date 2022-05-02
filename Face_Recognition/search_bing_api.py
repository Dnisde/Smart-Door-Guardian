from requests import exceptions
import argparse
import requests
import cv2
import os
# construct the argument parser and parse the arguments

class Build_Dataset:
	def __init__(self):
		self.API_KEY = "ed7345f16ba942ab9ac8024406e531f1"
		self.MAX_RESULTS = 250
		self.GROUP_SIZE = 50
		self.URL = "https://api.bing.microsoft.com/"
		# working with network requests there are a number of exceptions that can be thrown
		self.EXCEPTIONS = set([IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout])
		# Build argument each time initialize

	def build_arugment(self):
		ap = argparse.ArgumentParser()
		ap.add_argument("-q", "--query", required=True, help="search query to search Bing Image API for")
		ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
		args = vars(ap.parse_args())
		return args

	def request(self):
		args = self.build_arugment()
		# Store the search term in a convenience variable then set the headers and search parameters
		term = args["query"]
		headers = {"Ocp-Apim-Subscription-Key": self.API_KEY}
		params = {"q": term, "offset": 0, "count": self.GROUP_SIZE}
		# Doing the search
		print("[INFO] searching Images through Bing API for '{}'".format(term))
		search = requests.get(self.URL, headers=headers, params=params)
		search.raise_for_status()
		# Grab the results from the search into Json format: including the total number of
		results = search.json()
		# Estimated results returned by the Bing API
		estNumResults = min(results["totalEstimatedMatches"], self.MAX_RESULTS)
		print("[INFO] {} total results for '{}'".format(estNumResults, term))
		# initialize the total number of images downloaded thus far
		total = 0
		# loop over the estimated number of results in `GROUP_SIZE` groups
		for offset in range(0, estNumResults, self.GROUP_SIZE):
			# update the search parameters using the current offset, then
			# make the request to fetch the results
			print("[INFO] making request for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))

			params["offset"] = offset
			search = requests.get(self.URL, headers=headers, params=params)
			search.raise_for_status()
			results = search.json()
			print("[INFO] saving images for group {}-{} of {}...".format(
				offset, offset + self.GROUP_SIZE, estNumResults))

			# loop over the results
			for v in results["value"]:
				# try to download the image
				try:
					# make a request to download the image
					print("[INFO] fetching: {}".format(v["contentUrl"]))
					r = requests.get(v["contentUrl"], timeout=30)
					# build the path to the output image
					ext = v["contentUrl"][v["contentUrl"].rfind("."):]
					p = os.path.sep.join([args["output"], "{}{}".format(
						str(total).zfill(8), ext)])
					# write the image to disk
					f = open(p, "wb")
					f.write(r.content)
					f.close()
				# catch any errors that would not unable us to download the
				# image
				except Exception as e:
					# check to see if our exception is in our list of
					# exceptions to check for
					if type(e) in EXCEPTIONS:
						print("[INFO] skipping: {}".format(v["contentUrl"]))
						continue


		return EXCEPTIONS,





