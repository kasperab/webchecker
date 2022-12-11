import requests
import json
import os.path
import sys

file_name = "webdata.json"

if len(sys.argv) > 1:
	url = sys.argv[1]
	response = requests.get(url, headers = {"User-Agent": "webchecker"})
	data = []
	if os.path.exists(file_name):
		with open(file_name, "r") as file:
			data = json.load(file)
	data.append({"url": url, "text": response.text})
	with open(file_name, "w") as file:
		json.dump(data, file)
else:
	no_data = "Not following any web pages, do 'python3 webchecker.py [URL]' to add page"
	if os.path.exists(file_name):
		with open(file_name, "r") as file:
			data = json.load(file)
		if not data:
			print(no_data)
		else:
			changes = False
			for page in data:
				response = requests.get(page["url"], headers = {"User-Agent": "webchecker"})
				old = page["text"].split("\n")
				new = response.text.split("\n")
				removed = ""
				for line in old:
					if line in new:
						new.remove(line)
					else:
						removed += line + "\n"
				added = "\n".join(new)
				if removed or added:
					changes = True
					page["text"] = response.text
					print("CHANGES ON " + page["url"] + "\n")
					if removed:
						print("REMOVED:\n" + removed)
					if added:
						print("ADDED:\n" + added + "\n")
			if changes:
				with open(file_name, "w") as file:
					json.dump(data, file)
			else:
				print("No changes")
	else:
		print(no_data)
