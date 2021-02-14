import json

path = "C:/Edward/TreeHacks2021/Quora/result.json"

with open(path) as f:
  data = json.load(f)

dict = {"0":"Same Question", "1":"Same Topic", "2":"Unrelated"}
for item in data:
    item = data[item]
    print(item["sent1"], item["sent2"], dict[item["prediction"][2]])
