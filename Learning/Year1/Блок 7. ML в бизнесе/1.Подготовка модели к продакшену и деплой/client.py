import requests

if __name__ == '__main__':

    r = requests.post('http://localhost:5000/predict', json={'num': 15})

    print(r.status_code)

    if r.status_code == 200:

        print(r.json()['result'])
    else:

        print(r.text)