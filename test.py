import requests

BASE = "http://127.0.0.1:5000/"

#data = [{"likes": 178, "name": "Nando", "views": 1000},
#        {"likes": 10, "name": "This is an examplo of name of the video", "views": 103400},
#        {"likes": 10, "name": "This is the title of other video", "views": 10}]

#for i in range(len(data)):
#    response = requests.put(BASE + "video/" +str(i), data[i])
#    print(response.json())

#input()
#response = requests.delete(BASE + "video/0")
#print(response)
#input()
#response = requests.get(BASE + "video/6")
#print(response.json())

#response = requests.get(BASE + "video/6")
#print(response.json())
response = requests.get(BASE + "video/2", {"views":99, "likes":101})
print(response.json())