import json

#f=open("costumize/costumize.json", "r")
#a=f.read()
#print(json.dumps(a))

score=4
dictionary = {
    "score":score
}
jsonFile = json.dumps(dictionary)
with open("costumize/score.json", "w") as outfile:
    outfile.write(jsonFile)
print(dictionary)
