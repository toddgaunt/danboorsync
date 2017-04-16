# See LICENSE file for copyright and license details
import sys
import re
import os
import hashlib
import json
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

from imgfetch import log
from imgfetch import util

danbooru_posts_url = "http://hijiribe.donmai.us/posts"

def usage():
	sys.stderr.write("usage: imgfetch-danbooru [-h] [-p <pages>] [-e <extensions>] TAGS...\n")
	quit()

class image_post():
	""" image_post.__init__
	Creates and returns a new post object based on a dictionary from
	a danbooru json file's data


	return:
		post: a post object with all fields filled out according to the
		json file data
	"""
	def __init__(self, item=None):
		self.md5sum = item["md5"]

		self.tag_string_character = item["tag_string_character"]
		self.tag_string_general = item["tag_string_general"]
		self.tag_string_artist = item["tag_string_artist"]

		self.file_url = item["file_url"]
		self.file_ext = item["file_ext"]

def gen_filename(post):
	name = ""
	md5sum = str(post.md5sum)
	extension = str(post.file_ext)

	max_name_len = 200 - len(md5sum) - (len(extension) + 1)

	for character in post.tag_string_character.split():
		next_tag = util.remove_non_posix_chars(character) + '-'
		if len(name) + len(next_tag) >= max_name_len:
			break
		name += next_tag

	for tag in post.tag_string_general.split():
		next_tag = util.remove_non_posix_chars(tag) + '-'
		if len(name) + len(next_tag) >= max_name_len:
			break
		name += next_tag
	name += md5sum
	name += "." + extension

	return name

def gen_dirname(tag_string_character):
	path = "./"
	max_path_len = 250

	for character in tag_string_character.split():
		next_tag = util.remove_non_posix_chars(character) + '-'
		if len(path) + len(next_tag) >= max_path_len:
			break
		path += next_tag
	return path[0:-1]

def download_json_post(url):
	""" jsonize_post_url
	Uses the given url object to fetch a related json file

	Return:
		list[dict[str:str]]: this is the loaded json file
	"""
	json_url = url.scheme+"://"+url.netloc+url.path+".json"+"?"+url.query
	data = urlopen(json_url).read()
	json_file = json.loads(data.decode('utf-8'))
	# If not already a list, make it a list with one index.
	# This is for cases when there is a single post from the danbooru url
	if not type(json_file) is list:
		json_file = [json_file]
	return json_file

def string_range_parse(numbers):
	numbers = numbers.split(',')

	pages = []
	for i in numbers:
		rangematch = re.match(r'\s*(\d+)-(\d+)\s*', i)
		singlematch = re.match(r'\s*(\d+)\s*', i)
		if rangematch != None:
			for j in range(int(rangematch.group(1)), int(rangematch.group(2))+1):
				pages.append(j)
		elif singlematch:
			pages.append(int(singlematch.group(1)))
	return pages

# Driver of danbooru
def cmd(args, argi):
	lg = log.logger("imgfetch-danbooru", args['v'])

	# Default args
	args["danbooru"] = {}
	args["danbooru"]['p'] = [1]
	args["danbooru"]["e"] = []
	args["danbooru"]["tags"] = []

	# Parse args
	while (argi < len(sys.argv)):
		if ('-' == sys.argv[argi][0]):
			if ('h' == sys.argv[argi][1]):
				usage()
			elif ('p' == sys.argv[argi][1]):
				argi += 1
				try:
					args["danbooru"]['p'] = string_range_parse(sys.argv[argi])
				except IndexError:
					lg.error("No range given for -p switch.")
					usage()
			elif ('e' == sys.argv[argi][1]):
				argi += 1
				try:
					args["danbooru"]['e'] = sys.argv[argi].split(',')
				except IndexError:
					lg.error("No extensions given for -e switch.")
					usage()
			else:
				usage()
		else:
			args["danbooru"]["tags"].append(sys.argv[argi])

		argi += 1

	if ([] == args["danbooru"]["tags"]):
		usage()

	# Calculate all md5sums in target download directory recursively.
	md5sums = util.find_hash('.', hashlib.md5)

	for i in args["danbooru"]['p']:
		# Attach the queries to the url.
		url = urlparse(danbooru_posts_url)
		url = url._replace(query = "{}&tags={}&page={}".format(
			url.query, '+'.join(args["danbooru"]["tags"]), str(i)))

		json = download_json_post(url)
		if ([] == json):
			lg.fatal("Could not download json from url {}".format(
				urlparse.unparse(url)))

		# Transform the json list into a list of post objects
		posts = [];
		for item in json:
			# Load all the keys from the json dictionary
			keys = item.keys()
			# Skip the post in the jason file if it doesn't contain these keys
			if (("md5" not in keys) or ("image_width" not in keys)):
				lg.info("Skipping non-image post.")
				continue
			# Construct a new post derived from the json file data
			posts.append(image_post(item))

		# Maybe truncate the output.
		if (args['v'] == 0):
			trunc = 0
		elif (args['v'] == 1):
			trunc = 40
		elif (args['v'] == 2):
			trunc = 80
		else:
			trunc = -1

		for post in posts:
			# Check to see if the post is a desired file extension.
			if (([] != args["danbooru"]['e'])
					and (not post.file_ext in args["danbooru"]['e'])):
				continue

			filepath = gen_dirname(post.tag_string_character)

			try:
				os.mkdir(filepath)
			except FileExistsError:
				pass

			filepath = "{}/{}".format(filepath, gen_filename(post))

			if (post.md5sum not in md5sums):
				# Download the image
				with open(filepath, 'wb') as fp:
					fp.write(urlopen("http://{}/{}".format(\
							url.netloc, post.file_url)).read())

					if (args['r']):
						#TODO(todd): add robot output
						pass
					else:
						lg.info("<\033[33mNEW FILE\033[0m> " + filepath[0:trunc-9])
				# Add the new file to the dict of calculated md5sums
				md5sums[post.md5sum] = filepath
			else:
				if (args['r']):
					#TODO(todd): add robot output
					pass
				else:
					lg.info("<\033[32mFILE MATCH\033[0m> \"{}\" -> \"{}\"".format(
						filepath[0:(trunc-8)//2],
						md5sums[post.md5sum][0:(trunc-8)//2]))
					return 0
