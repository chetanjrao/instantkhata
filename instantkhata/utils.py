from urllib.parse import urlencode
from urllib.request import Request, urlopen

def createMessage(message:str, status:int):
    return {
        "message": message,
        "status": status
    }

def send_message(message: str, mobile: str):
    url = "http://api.msg91.com/api/sendhttp.php" 
    values = {
        "authkey": "213839AHVCFomzdt5e274930P1",
        "mobiles": mobile,
        "message": message,
        'sender': 'MAZONT',
        'route': 4
    }
    postdata = urlencode(values).encode("utf-8")
    request = Request(url, postdata)
    response = urlopen(request)
    output = response.read()