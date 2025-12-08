import requests

res = requests.get("http://localhost:8080/health")
result = str(res.json())

if("{'status': 'ok'}" == result):
    print("everything is good :)")
else:
    print("retry :(")