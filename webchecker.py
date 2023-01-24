import requests
import json
import os.path
import sys

file_name = "webdata.json"
no_data = "Not following any web pages, do 'python3 webchecker.py +[URL]' to add page"

if len(sys.argv) > 1:
	argument = sys.argv[1]
	if argument == "list":
		if os.path.exists(file_name):
			with open(file_name, "r") as file:
				data = json.load(file)
			if data:
				for page in data:
					print(page["url"])
			else:
				print(no_data)
		else:
			print(no_data)
	elif argument[0] == "+":
		url = argument[1:]
		response = requests.get(url, headers = {"User-Agent": "webchecker"})
		data = []
		if os.path.exists(file_name):
			with open(file_name, "r") as file:
				data = json.load(file)
		data.append({"url": url, "text": response.text})
		with open(file_name, "w") as file:
			json.dump(data, file)
		print("Added " + url)
	elif argument[0] == "-":
		url = argument[1:]
		if os.path.exists(file_name):
			with open(file_name, "r") as file:
				data = json.load(file)
			if data:
				removed = False
				for page in data:
					if page["url"] == url:
						data.remove(page)
						removed = True
						break
				if removed:
					with open(file_name, "w") as file:
						json.dump(data, file)
					print("Removed " + url)
				else:
					print("URL not found")
			else:
				print(no_data)
		else:
			print(no_data)
	else:
		print("Unknown argument")
else:
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
				for index, line in enumerate(old):
					if line in new:
						new[new.index(line)] = ""
					else:
						removed += str(index + 1) + "| " + line.strip(" \t\u00a0") + "\n"
				added = ""
				for index, line in enumerate(new):
					if line:
						added += str(index + 1) + "| " + line.strip(" \t\u00a0") + "\n"
				if removed or added:
					changes = True
					page["text"] = response.text
					print("CHANGES ON " + page["url"] + "\n")
					if removed:
						print("REMOVED:\n" + removed)
					if added:
						print("ADDED:\n" + added)
			if changes:
				with open(file_name, "w") as file:
					json.dump(data, file)
			else:
				print("No changes")
	else:
		print(no_data)
