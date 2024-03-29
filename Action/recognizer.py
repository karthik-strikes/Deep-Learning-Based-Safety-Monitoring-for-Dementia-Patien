# -*- coding: UTF-8 -*-
import numpy as np
import cv2 as cv
from pathlib import Path
from Tracking.deep_sort import preprocessing
from Tracking.deep_sort.nn_matching import NearestNeighborDistanceMetric
from Tracking.deep_sort.detection import Detection
from Tracking import generate_dets as gdet
from Tracking.deep_sort.tracker import Tracker
from keras.models import load_model
from .action_enum import Actions
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# Use Deep-sort(Simple Online and Realtime Tracking)
# To track multi-person for multi-person actions recognition
import urllib.request
import urllib.parse

url='http://192.168.1.3:8080/shot.jpg'
url1='http://192.168.1.17:8080/shot.jpg'
apikey='q9wYxbxY1nQ-gvEThnIMhy0Or9Eok0rf2cZADoA6Or'
numbers=('9962366145')
message='someone is falling down'
sender='TXTLCL'
username = 'yadav.wegot@gmail.com'





def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'username':username,'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?/")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

file_path = Path.cwd()
clip_length = 15
max_cosine_distance = 0.3
nn_budget = None
nms_max_overlap = 1.0
send_msg = 0

#deep_sort
model_filename = str(file_path/'Tracking/graph_model/mars-small128.pb')
encoder = gdet.create_box_encoder(model_filename, batch_size=1)
metric = NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = Tracker(metric)

# track_box
trk_clr = (0, 255, 0)


class ActionRecognizer(object):
    @staticmethod
    def load_action_premodel(model):
        return load_model(model)

    @staticmethod
    def framewise_recognize(pose, pretrained_model):
        frame, joints, bboxes, xcenter = pose[0], pose[1], pose[2], pose[3]
        joints_norm_per_frame = np.array(pose[-1])

        if bboxes:
            bboxes = np.array(bboxes)
            features = encoder(frame, bboxes)

            # score to 1.0 here).
            detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(bboxes, features)]

            # 进行非极大抑制
            boxes = np.array([d.tlwh for d in detections])
            scores = np.array([d.confidence for d in detections])
            indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
            detections = [detections[i] for i in indices]

            # 调用tracker并实时更新
            tracker.predict()
            tracker.update(detections)

            # 记录track的结果，包括bounding boxes及其ID
            trk_result = []
            for trk in tracker.tracks:
                if not trk.is_confirmed() or trk.time_since_update > 1:
                    continue
                bbox = trk.to_tlwh()
                trk_result.append([bbox[0], bbox[1], bbox[2], bbox[3], trk.track_id])
                # 标注track_ID
                trk_id = 'ID-' + str(trk.track_id)
                cv.putText(frame, trk_id, (int(bbox[0]), int(bbox[1]-45)), cv.FONT_HERSHEY_SIMPLEX, 0.8, trk_clr, 3)

            for d in trk_result:
                xmin = int(d[0])
                ymin = int(d[1])
                xmax = int(d[2]) + xmin
                ymax = int(d[3]) + ymin
                # id = int(d[4])
                try:
                    # xcenter是一帧图像中所有human的1号关节点（neck）的x坐标值
                    # 通过计算track_box与human的xcenter之间的距离，进行ID的匹配
                    tmp = np.array([abs(i - (xmax + xmin) / 2.) for i in xcenter])
                    j = np.argmin(tmp)
                except:
                    # 若当前帧无human，默认j=0（无效）
                    j = 0

                # 进行动作分类
                if joints_norm_per_frame.size > 0:
                    joints_norm_single_person = joints_norm_per_frame[j*36:(j+1)*36]
                    joints_norm_single_person = np.array(joints_norm_single_person).reshape(-1, 36)
                    pred = np.argmax(pretrained_model.predict(joints_norm_single_person))
                    init_label = Actions(pred).name
                    # 显示动作类别
                    cv.putText(frame, init_label, (xmin + 80, ymin - 45), cv.FONT_HERSHEY_SIMPLEX, 1, trk_clr, 3)
                # 画track_box
                cv.rectangle(frame, (xmin - 10, ymin - 30), (xmax + 10, ymax), trk_clr, 2)
        return frame

def load_action_premodel(model):
    return load_model(model)


def framewise_recognize(pose, pretrained_model):
    frame, joints, bboxes, xcenter = pose[0], pose[1], pose[2], pose[3]
    joints_norm_per_frame = np.array(pose[-1])
    init_label="unknown"
    global send_msg 
    if bboxes:
        bboxes = np.array(bboxes)
        features = encoder(frame, bboxes)

        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(bboxes, features)]

        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]


        tracker.predict()
        tracker.update(detections)


        trk_result = []
        for trk in tracker.tracks:
            if not trk.is_confirmed() or trk.time_since_update > 1:
                continue
            bbox = trk.to_tlwh()
            trk_result.append([bbox[0], bbox[1], bbox[2], bbox[3], trk.track_id])
            #track_ID
            trk_id = 'ID-' + str(trk.track_id)
            cv.putText(frame, trk_id, (int(bbox[0]), int(bbox[1]-45)), cv.FONT_HERSHEY_SIMPLEX, 0.8, trk_clr, 3)

        for d in trk_result:
            xmin = int(d[0])
            ymin = int(d[1])
            xmax = int(d[2]) + xmin
            ymax = int(d[3]) + ymin
            # id = int(d[4])
            try:
                tmp = np.array([abs(i - (xmax + xmin) / 2.) for i in xcenter])
                j = np.argmin(tmp)
            except:
                j = 0

            if joints_norm_per_frame.size > 0:
                joints_norm_single_person = joints_norm_per_frame[j*36:(j+1)*36]
                joints_norm_single_person = np.array(joints_norm_single_person).reshape(-1, 36)
                pred = np.argmax(pretrained_model.predict(joints_norm_single_person))
                init_label = Actions(pred).name	

                cv.putText(frame, init_label, (xmin + 80, ymin - 45), cv.FONT_HERSHEY_SIMPLEX, 1, trk_clr, 3)
                
        
                if init_label == 'falldown':
                    cv.putText(frame, 'WARNING: someone is falling down!', (20, 60), cv.FONT_HERSHEY_SIMPLEX,
                               1.5, (0, 0, 255), 4)
                if (init_label == 'falldown') and (send_msg == 0):
                    send_msg = 1
                    if (init_label == 'falldown') and (send_msg == 1):
                     	# resp =  sendSMS(apikey, numbers,sender, message)
                     	print("dnsjkb") 
                elif init_label=='stand' or init_label=='sit' or init_label=='sleep':
                    send_msg=0         
            cv.rectangle(frame, (xmin - 10, ymin - 30), (xmax + 10, ymax), trk_clr, 2)
            #print(init_label)
    return frame, init_label

