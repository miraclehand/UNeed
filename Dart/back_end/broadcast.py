import json
import requests
from constants import BCAST_URL, BCAST_HDR
from db.models import User, UserWatch, Disc, Chat, UserChatRoom
from api.util import make_payload, post_broadcast_async
import requests
from concurrent.futures import ThreadPoolExecutor

"""
curl -H "Content-Type: application/json" -X POST "https://exp.host/--/api/v2/push/send" -d '{
    "to": "ExponentPushToken[Xz4dwpIDmHYRqoGf5QlyPN]",
    "title":"hello",
    "body": "world"
    }'
"""
def post_url(args):
    return requests.post(args[0], data=args[1])
        
def postman():
    form_data = {
        "foo1":"bar1",
        "foo2":"bar2"
    }
    list_of_urls = [("https://postman-echo.com/post",form_data)]*10

    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(post_url,list_of_urls))

    for response in response_list:
        print(response)

if __name__ == '__main__':
    #postman()
    #exit(0)
    user = User.objects.get({'email':'miraclehand@gmail.com'})

    ucr = UserChatRoom.objects.get({'user':user._id})

    room = ucr.rooms[0]
    watch = room.watch
    chat = room.chats[-1]

    payloads = [make_payload(chat)]
    post_broadcast_async(payloads)


