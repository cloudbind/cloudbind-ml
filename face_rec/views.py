from django.shortcuts import render
# import main_video
import cv2
import json
import pymongo
import urllib.request
import numpy as np
from bson import json_util
from django.http import JsonResponse
from simple_facerec import SimpleFacerec
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from django.conf import settings
connect_string = 'mongodb+srv://sarthakcr007:Sarthak466@cluster0.leawjlu.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['CloudBind']
collection_name = dbname["Faces"]
collection_id = dbname["_ids"]

# import random
# def uniqueid():
#     seed = random.getrandbits(32)
#     while True:
#        yield seed
#        seed += 1

def parse_json(data):
    return json.loads(json_util.dumps(data))

@csrf_exempt 
def faceRecognition(request):
    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")

    # # Load Camera
    # cap = cv2.VideoCapture(0)

    '''
    request format:{
        url: <url link>
    }
    '''
    json_data = json.loads(request.body)
    url = json_data['url']
    
    # url = 'https://res.cloudinary.com/dtgkbztkz/image/upload/v1681322957/Sarthak_Bhan_pofunf.jpg'
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)

    # ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(img)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        # cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        print(name)
    if name == "Unkown":
        new_json = {
            "name" : "unknown",
            "img_url" : url
        }
        collection_name.insert_one(new_json)
        return JsonResponse(res_json)
    name = str(name)
    res_json = {
        'name' : name,
        'img_url' : url
    }
    # print(type(url))
    # print(str(name))
    print(res_json)
    # res_json = parse_json(res_json)
    # res_json = json.dumps(res_json)
    # collection_name.insert_one(res_json)

    return JsonResponse(res_json)


    # while True:
    #     ret, frame = cap.read()

    #     # Detect Faces
    #     face_locations, face_names = sfr.detect_known_faces(frame)
    #     for face_loc, name in zip(face_locations, face_names):
    #         y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

    #         cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
    #         print(name)
    #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    #     cv2.imshow("Frame", frame)

    #     key = cv2.waitKey(1)
    #     if key == 27:
    #         break

    # cap.release()
    # cv2.destroyAllWindows()