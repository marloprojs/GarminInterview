# GarminInterview
## How to run the code

```bash
python server.py
```
Please note this is a Flask server so you may need to install flask:
```bash
pip install flask
```

While the flask server is running, open a new tab in your terminal and open to the same directory as server.py

From here, you can test the api resource with the url: http://127.0.0.1:5000/compositeUsers

PLEASE NOTE****** When you run the curl command, you MUST put the url in quotation marks.

## Sample commands
```bash
curl "http://127.0.0.1:5000/compositeUsers/ce6f566e-93e8-464e-a7de-95012f1218b1?creditCardState=ACTIVE"
```
```bash
curl "http://127.0.0.1:5000/compositeUsers/ce6f566e-93e8-464e-a7de-95012f1218b1"
```
```bash
curl "http://127.0.0.1:5000/compositeUsers/ce6f566e-93e8-464e-a7de-95012f1218b1?creditCardState=ACTIVE&deviceState=INITIALIZATION_FAILED"
```
