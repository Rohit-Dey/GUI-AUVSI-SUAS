from ctypes import *
import random
import cv2
import numpy as np
from gps_correction import Correct_Gps
from calc_gps import gps
import os
import time
from dronekit import mavutil , connect
import sys
import socket
import pickle
import json
import logging
import tensorflow as tf 
from sklearn.cluster import KMeans
import random
import k_means
import color
import test

try:
    path=sys.argv[1]
    os.chdir(path)
except:
    pass

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

    


class IplROI(Structure):
    pass

class IplTileInfo(Structure):
    pass

class IplImage(Structure):
    pass

IplImage._fields_ = [
    ('nSize', c_int),
    ('ID', c_int),
    ('nChannels', c_int),               
    ('alphaChannel', c_int),
    ('depth', c_int),
    ('colorModel', c_char * 4),
    ('channelSeq', c_char * 4),
    ('dataOrder', c_int),
    ('origin', c_int),
    ('align', c_int),
    ('width', c_int),
    ('height', c_int),
    ('roi', POINTER(IplROI)),
    ('maskROI', POINTER(IplImage)),
    ('imageId', c_void_p),
    ('tileInfo', POINTER(IplTileInfo)),
    ('imageSize', c_int),          
    ('imageData', c_char_p),
    ('widthStep', c_int),
    ('BorderMode', c_int * 4),
    ('BorderConst', c_int * 4),
    ('imageDataOrigin', c_char_p)]


class iplimage_t(Structure):
    _fields_ = [('ob_refcnt', c_ssize_t),
                ('ob_type',  py_object),
                ('a', POINTER(IplImage)),
                ('data', py_object),
                ('offset', c_size_t)]

class inference(object):

    #lib = CDLL("./darknet/libdarknet.so", RTLD_GLOBAL)
    path=os.getcwd()
    print(path)
    #lib = CDLL(path+"/"+"darknet/libdarknet.so", RTLD_GLOBAL)
    # lib = CDLL(path+"/darknet/libdarknet.so", RTLD_GLOBAL)
    lib = CDLL("/home/uas-dtu/Desktop/VISION/darknet/libdarknet.so", RTLD_GLOBAL)
    lib.network_width.argtypes = [c_void_p]
    lib.network_width.restype = c_int
    lib.network_height.argtypes = [c_void_p]
    lib.network_height.restype = c_int

    predict = lib.network_predict
    predict.argtypes = [c_void_p, POINTER(c_float)]
    predict.restype = POINTER(c_float)

    set_gpu = lib.cuda_set_device
    set_gpu.argtypes = [c_int]

    make_image = lib.make_image
    make_image.argtypes = [c_int, c_int, c_int]
    make_image.restype = IMAGE

    get_network_boxes = lib.get_network_boxes
    get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
    get_network_boxes.restype = POINTER(DETECTION)

    make_network_boxes = lib.make_network_boxes
    make_network_boxes.argtypes = [c_void_p]
    make_network_boxes.restype = POINTER(DETECTION)

    free_detections = lib.free_detections
    free_detections.argtypes = [POINTER(DETECTION), c_int]

    free_ptrs = lib.free_ptrs
    free_ptrs.argtypes = [POINTER(c_void_p), c_int]

    network_predict = lib.network_predict
    network_predict.argtypes = [c_void_p, POINTER(c_float)]

    reset_rnn = lib.reset_rnn
    reset_rnn.argtypes = [c_void_p]

    load_net = lib.load_network
    load_net.argtypes = [c_char_p, c_char_p, c_int]
    load_net.restype = c_void_p

    do_nms_obj = lib.do_nms_obj
    do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

    do_nms_sort = lib.do_nms_sort
    do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

    free_image = lib.free_image
    free_image.argtypes = [IMAGE]

    letterbox_image = lib.letterbox_image
    letterbox_image.argtypes = [IMAGE, c_int, c_int]
    letterbox_image.restype = IMAGE

    load_meta = lib.get_metadata
    lib.get_metadata.argtypes = [c_char_p]
    lib.get_metadata.restype = METADATA

    load_image = lib.load_image_color
    load_image.argtypes = [c_char_p, c_int, c_int]
    load_image.restype = IMAGE

    rgbgr_image = lib.rgbgr_image
    rgbgr_image.argtypes = [IMAGE]

    predict_image = lib.network_predict_image
    predict_image.argtypes = [c_void_p, IMAGE]
    predict_image.restype = POINTER(c_float)


    def __init__(self):
        logging.basicConfig(filename=str(path) + "/logs/human_detection" + str(len(os.listdir(str(path) + "/logs"))) + ".log",
                            format=' %(module)s %(lineno)d %(message)s',
                            filemode='w')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        pass


    def classify(self,net, meta, im):
        out = inference.predict_image(net, im)
        res = []
        for i in range(meta.classes):
            res.append((meta.names[i], out[i]))
        res = sorted(res, key=lambda x: -x[1])
        return res


    def array_to_image(self,arr):
        # need to return old values to avoid python freeing memory
        arr = arr.transpose(2,0,1)
        c, h, w = arr.shape[0:3]
        arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
        data = arr.ctypes.data_as(POINTER(c_float))
        im = IMAGE(w,h,c,data)
        return im, arr

    def detect(self,net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
        """if isinstance(image, bytes):
            # image is a filename
            # i.e. image = b'/darknet/data/dog.jpg'
            im = load_image(image, 0, 0)
        else:
            # image is an nparray
            # i.e. image = cv2.imread('/darknet/data/dog.jpg')
            im, image = array_to_image(image)
            rgbgr_image(im)
        """
        im, image = self.array_to_image(image)
        inference.rgbgr_image(im)
        num = c_int(0)
        pnum = pointer(num)
        inference.predict_image(net, im)
        dets = inference.get_network_boxes(net, im.w, im.h, thresh,hier_thresh, None, 0, pnum)
        num = pnum[0]
        if nms: inference.do_nms_obj(dets, num, meta.classes, nms)

        res = []
        for j in range( num ):
            a = dets[j].prob[0:meta.classes]
            if any(a):
                ai = np.array(a).nonzero()[0]
                for i in ai:
                    b = dets[j].bbox
                    res.append((meta.names[i], dets[j].prob[i],
                               (b.x, b.y, b.w, b.h)))

        res = sorted(res, key=lambda x: -x[1])
        if isinstance(image, bytes): inference.free_image(im)
        inference.free_detections(dets, num)
        return res

    def set_servo(self,vehicle, servo_number, pwm_value):
        pwm_value_int = int(pwm_value)
        msg = vehicle.message_factory.command_long_encode(
            0, 0,
            mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
            0,
            servo_number,
            pwm_value_int,
            0, 0, 0, 0, 0
        )
        for i in range(5):
            vehicle.send_mavlink(msg)
        print("..................DROPPED_PAYLOAD..........................")
        self.logger.info("..................DROPPED_PAYLOAD..........................")

    def frame_to_npimage(self,array,shape):
        frame=np.frombuffer(array, dtype=np.float64).reshape(shape)
        return frame.astype("uint8")


    def runOnVideo(self,array,event,vid_source,shape,path,net, meta,  thresh=.3, hier_thresh=.5, nms=.45):
        #VIDEO WRITER
        video_writer = cv2.VideoWriter((path + "/save/" + 'human_detecton' + str(len(os.listdir(path + "/save"))) + ".avi" ), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (640, 360))
        print(os.getcwd())
       # logging.basicConfig(filename="logs/human_detection" + str(len(os.listdir("logs"))) + ".log", format="%(module)s %(lineno)d %(message)s", filemode='w')
       # self.logger = logging.getLogger()
       # self.logger.setLevel(logging.INFO)

        cfg_path=path+"/darknet/files/yolov3_tiny_detection.cfg"
        weight_path=path+"/darknet/backup/yolov3_tiny_detection_22000.weights"
        data_path=path+"/darknet/files/obj.data"
        #net = inference.load_net(b"./darknet/cfg/yolov3-tiny.cfg", b"./darknet/yolov3-tiny.weights", 0)
        #meta = inference.load_meta(b"./darknet/cfg/coco.data")
        net = self.load_net(cfg_path.encode(),weight_path.encode(),0)
        meta = self.load_meta(data_path.encode())#(b"/home/uas-dtu/Desktop/new_on_uav/VISION/darknet/files/human.data")
        #odlc_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #odlc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        local_ip="192.168.0.253"
        odlc_port=6969 
        #odlc_socket.connect((local_ip, odlc_port))
        odlc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        odlc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        odlc_sock.bind((local_ip, odlc_port))
        print("SOCKET CREATED")
        odlc_sock.listen(5)
        client, addr = odlc_sock.accept()
        print("ACCEPTED")
        ### CHARACTER CLASSIFICATION ###
        interpreter_classification = tf.lite.Interpreter(model_path="/home/uas-dtu/Desktop/VISION/classification_mobilenet_binary.tflite")
        interpreter_classification.allocate_tensors()
        #input_details_classification = interpreter_classification.get_input_details()
        #output_details_classification = interpreter_classification.get_output_details()
        print("CHARACRTER CLASSIFIER LOADED")

        ### ORIENTATION CLASSIFICATION ###
        interpreter_orientation = tf.lite.Interpreter(model_path="/home/uas-dtu/Desktop/VISION/orientation_cnn_small.tflite")
        interpreter_orientation.allocate_tensors()
        #input_details_orientation = interpreter_orientation.get_input_details()
        #output_details_orientation = interpreter_orientation.get_output_details()
        print("ORIENTATION CLASSIFIER LOADED")
        #video = cv2.VideoCapture(vid_source)
        count = 0
        human_list=[]
        gps_obj=Correct_Gps(addr="127.0.0.1",port="14553")
        save_gps=gps()
        classes_box_colors = [(0, 0, 255), (0, 255, 0)]  #red for palmup --> stop, green for thumbsup --> go
        classes_font_colors = [(255, 255, 0), (0, 255, 255)]
        cent_lat,cent_lon,alti,bear=[0,0,0,0]
        class_dict = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 
                        18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z"}
        orientation_dict = {0: "E", 1: "N", 2: "NE", 3: "NW", 4: "S", 5: "SE", 6: "SW", 7: "W"}
        pic_count = 0
        print("PIC COUNT", pic_count)
        while True:
            #odlc_sock.listen(5)
            #client, addr = odlc_sock.accept()
            print("GCS connected @", addr)
            if not event.is_set():
                video_writer.release()
                print("......................waiting to be set again.............................................")
                self.logger.info("......................waiting to be set again.............................................")
                event.wait()
                video_writer = cv2.VideoWriter((path + "/frames/" + 'human_detecton' + str(len(os.listdir(path + "/frames"))) + ".avi"),cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (640, 360))
                print(os.getcwd())
                #pause the run on video
            start = time.time()

            try:

                li1=gps_obj.tag_attitude()
                frame=self.frame_to_npimage(array,shape)
                print("......................waiting to be cleared.............................................",event.is_set())
                self.logger.info("......................waiting to be cleared.............................................")
                #res, frame = video.read()
                li2=gps_obj.tag_attitude()
                cent_lat,cent_lon,alti,bear=gps_obj.save_gps(li1,li2)
            except Exception as err:
                print("error in runOnVideo",err)
                self.logger.warning("error in runOnVideo: " + str(err))
                self.logger.debug(err)
                continue
            #frame=self.frame_to_npimage(array,shape)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im, arr = self.array_to_image(rgb_frame)

            #cv2.imshow("frame",frame)
            #if cv2.waitKey(10)==ord("q"):
            #    break

            num = c_int(0)
            pnum = pointer(num)
            inference.predict_image(net, im)

            dets = inference.get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
            num = pnum[0]
            print("AND IT STARTED")
            if (nms): inference.do_nms_obj(dets, num, meta.classes, nms);
            # res = []
            font = cv2.FONT_HERSHEY_SIMPLEX
            print(count)
            self.logger.info("count: " + str(count))
            for j in range(num):
                for i in range(meta.classes):
                    pic_count += 1
                    if dets[j].prob[i] > 0:
                        try:

                            shape_class = meta.names[i]
                            print("SHAPE CLASS", str(shape_class).split("'")[1])
                            print("SHAPE CLASS TYPE", type(shape_class))
                            b = dets[j].bbox
                            x1 = int(b.x - b.w / 2.)
                            y1 = int(b.y - b.h / 2.)
                            x2 = int(b.x + b.w / 2.)
                            y2 = int(b.y + b.h / 2.)
                            print("X1, X2, Y1, Y2", x1, x2, y1, y2)
                            img_color = frame[y1 - 10 : y2 + 10, x1 - 10 : x2 + 10]
                            img = frame[y1 - 20 : y2 + 20, x1 - 20 : x2 + 20]
                            output = k_means.binarize(img)
                            #color_of_character = color.cmyk_color((output[0][0], output[0][1], output[0][2]))
                            #color_of_shape = color.cmyk_color((output[1][0], output[1][1], output[1][2]))
                            color_of_character, color_of_shape = test.color_output(img_color)
                            lat, lon=save_gps.compute_gps(int((x1 + x2)/2), int((y1+y2)/2.0), bear, alti, cent_lat, cent_lon, frame.shape)

                            # img = cv2.imread(img, 0)
                            orient_mask = cv2.resize(output[4], (32, 32))
                            mask = np.reshape(orient_mask, (32, 32, 1))
                            mask = np.expand_dims(mask, axis = 0)
                            mask = np.array(mask, np.float32)/255.0
                            #cv2.imwrite("/home/uas-dtu/Desktop/VISION/save/mask" + str(pic_count) + '.jpg', mask)
                            class_mask = cv2.merge((orient_mask, orient_mask, orient_mask))
                            print("CLASS_MASK", class_mask)
                            print("MASK TYPE", class_mask.shape)
                            class_mask = cv2.resize(class_mask, (32, 32))
                            class_mask = np.reshape(class_mask, (32, 32, 3))
                            class_mask = np.expand_dims(class_mask, axis = 0)
                            class_mask = np.array(class_mask, np.float32)/255.0
                            ######################################### APLHANUMERIC CHARACTER #############################################
                            input_details_classification = interpreter_classification.get_input_details()
                            output_details_classification = interpreter_classification.get_output_details()
                            interpreter_classification.set_tensor(input_details_classification[0]['index'], class_mask)
                            interpreter_classification.invoke()
                            output_details_classification = interpreter_classification.get_tensor(output_details_classification[0]['index'])
                            print(output_details_classification)
                            class_name = class_dict[np.argmax(output_details_classification)]
                            print(class_name)
                            ######################################### ORIENTATION #############################################
                            input_details_orientation = interpreter_orientation.get_input_details()
                            output_details_orientation = interpreter_orientation.get_output_details()
                            interpreter_orientation.set_tensor(input_details_orientation[0]['index'], mask)
                            interpreter_orientation.invoke()
                            output_details_orientation = interpreter_orientation.get_tensor(output_details_orientation[0]['index'])
                            orientation_name = orientation_dict[np.argmax(output_details_orientation)]
                            print(output_details_orientation)

                            cv2.imwrite('/home/uas-dtu/Desktop/VISION/ODLC/' + str(pic_count) + '.jpg', img)
                            img_dictionary = {"Shape" : str(shape_class).split("'")[1], 
                                                "Shape_Color" : color_of_shape, 
                                                "Alphanumeric" : class_name, 
                                                "Alphanumeric_Color" : color_of_character, 
                                                "Orientation" : orientation_name, 
                                                "Latitude" : lat, 
                                                "Longitude" : lon, 
                                                 "Type": "STANDARD"}
                            
                            json_object = json.dumps(img_dictionary, indent = 4).encode('utf-8')
                            print("DICTIONARY DUMPED")
                            with open("/home/uas-dtu/Desktop/VISION/ODLC/" + str(pic_count) + '.json', "wb") as json_file:
                                json_file.write(json_object)
                                print("FILE WRITTEN")
                            message = str(pic_count) + '.jpg'
                            message_1 = str(pic_count) + '.json'
                            client.send(message.encode("utf-8"))#, (local_ip, odlc_port)) 
                            client.send(message_1.encode("utf-8"))
                            print("Data sent: ", pic_count)
                            #local_img = "/home/uas-dtu/Desktop/VISION/save/" + str(pic_count) + '.jpg'
                            #local_json = "/home/uas-dtu/Desktop/VISION/save/" + str(pic_count) + '.json'
                            #os.system('scp "%s" "%s:%s"' % (local_img, "uas-dtu@192.168.0.252", "~/interop_odlc/"))  
                            #os.system('scp "%s" "%s:%s"' % (local_json, "uas-dtu@192.168.0.252", "~/interop_odlc/"))
                                
                            #cv2.rectangle(frame, (x1, y1), (x2, y2), classes_box_colors[i], 2)
                            #print(meta.names[i],meta.names[i])
                            #cv2.putText(frame, str(meta.names[i]), (x1, y1 - 20), 2, font, classes_font_colors[i], 5, cv2.LINE_AA)
                            #cv2.putText(frame, str(meta.names[i]), (x1, y1 - 20), font,1, classes_font_colors[i], 1, cv2.LINE_AA)

                            # try:

                            #     if  meta.names[i] == b'HUMAN':
                            #         count += 1
                            #         #humans_list.append([lat,lon])
                            #         print("In classifier",bear,alti,cent_lat,cent_lon,frame.shape)
                            #         self.logger.info("In classifier: " + str(bear) + " " + str(alti) + " " + str(cent_lat) + " " + str(cent_lon) + " " + str(frame.shape))
                            #         cv2.rectangle(frame, (x1, y1), (x2, y2), classes_box_colors[i], 2)
                            #         #print(meta.names[i],meta.names[i])
                            #         #cv2.putText(frame, str(meta.names[i]), (x1, y1 - 20), 2, font, classes_font_colors[i], 5, cv2.LINE_AA)
                            #         cv2.putText(frame, str(meta.names[i]), (x1, y1 - 20), font,1, classes_font_colors[i], 1, cv2.LINE_AA)

                            #         lat,lon=save_gps.compute_gps(int((x1 + x2)/2),int((y1+y2)/2.0),bear,alti,cent_lat,cent_lon,frame.shape)


                            #         cv2.putText(frame, str(lat)+" "+str(lon), (x1, y1 + 20), font,1, classes_font_colors[i], 1, cv2.LINE_AA)

                            #         print("lat,long")
                            #         print(lat,lon)
                            #         self.logger.info("lat lon: " + str(lat) + " " + str(lon))
                            #         name = path+"/save/" + str(lat) + " " + str(lon) + ".jpg"
                            #         self.logger.info(str(lat) + " " + str(lon))
                            #         cv2.imwrite(name, frame)
                            #         print("lat ", "lon ", lat, lon)

                            #         message="PAYLOAD"
                            #         """            elif event == "PAYLOAD":
                            #         print("Sending PAYLOAD")
                            #         message = "PAYLOAD"
                            #         sysid = int(values["UAV_NO"])
                            #         L_thread = threading.Thread(target=send_to_uav, args=(message, sysid,send_mode))
                            #         L_thread.start()

                                    
                            #         """
                            #         dt={}
                            #         dt["MESSAGE"]="DROP"
                            #         dt["SYS_ID"]=0
                            #         dt["PAYLOAD"]=[]
                            #         dt["PACKET_NO"]=0
                            #         dt["TIMESTAMP"]=0

                            #         #payload_sock.sendto(message.encode("utf-8"), (local_ip, payload_port))
                            #         app_json = json.dumps(dt).encode("UTF-8")
                            #         payload_sock.sendto(app_json, (local_ip, payload_port))

                            #         print("____________DROPPING PAYLOAD____________")
                            #         self.logger.info("____________DROPPING PAYLOAD____________")
                            #         dt={}
                            #         dt["HUMANS"]=[lat,lon,1,0]
                            #         if(count<=1):
                            #             self.send_to_modified_server(payload_sock,dt)
                            #             print(lat, lon)

                                # elif  meta.names[i] == b'CAR':
                                #     count += 1
                                #     #humans_list.append([lat,lon])
                                #     print("In classifier",bear,alti,cent_lat,cent_lon,frame.shape)
                                #     self.logger.info("In classifier: " + str(bear) + " " + str(alti) + " " + str(cent_lat) + " " + str(cent_lon) + " " + str(frame.shape))
                                #     cv2.rectangle(frame, (x1, y1), (x2, y2), classes_box_colors[i], 2)
                                #     #print(meta.names[i],meta.names[i])
                                #     #cv2.putText(frame, str(meta.names[i]), (x1, y1 - 20), 2, font, classes_font_colors[i], 5, cv2.LINE_AA)
                                #     cv2.putText(frame, str(meta.names[i]), (x1, y1 - 20), font,1, classes_font_colors[i], 1, cv2.LINE_AA)

                                #     lat,lon=save_gps.compute_gps( int((x1 + x2)/2),int((y1+y2)/2.0),bear,alti,cent_lat,cent_lon,frame.shape)


                                #     cv2.putText(frame, str(lat)+" "+str(lon), (x1, y1 + 20), font,1, classes_font_colors[i], 1, cv2.LINE_AA)

                                #     print("lat,long")
                                #     print(lat,lon)
                                #     self.logger.info("lat lon: " + str(lat) + " " + str(lon))
                                #     name = path+"/save/" + str(lat) + " " + str(lon) + ".jpg"
                                #     self.logger.info(str(lat) + " " + str(lon))

                                #     cv2.imwrite(name, frame)
                                #     print("lat ", "lon ", lat, lon)

                                #     message="PAYLOAD"

                                #     dt={}
                                #     dt["MESSAGE"]="DROP"
                                #     dt["SYS_ID"]=0
                                #     dt["PAYLOAD"]=[]
                                #     dt["PACKET_NO"]=0
                                #     dt["TIMESTAMP"]=0

                                #     #payload_sock.sendto(message.encode("utf-8"), (local_ip, payload_port))
                                #     app_json = json.dumps(dt).encode("UTF-8")
                                #     payload_sock.sendto(app_json, (local_ip, payload_port))

                                #     print("____________DROPPING PAYLOAD____________")
                                #     self.logger.info("____________DROPPING PAYLOAD____________")
                                #     dt={}
                                #     dt["CARS"]=[lat,lon,1,0]
                                #     if(count<=1):
                                #         self.send_to_modified_server(payload_sock,dt)
                                #         print(lat, lon)
                                #     # self.drop_waypoint()

                                #     #self.drop_waypoint()


                                #     #write_str=str(str(lat)+" " +str(lon)+"\n")
                                #     #self.signs_txt.write(write_str)
                                #     #self.signs_txt.flush()


                                # #add the lat long to a dict with different classes and list of gps coordinates
                            # except Exception as err:
                            #     self.logger.warning("error in RUNONVIDEO: " + str(err))
                            #     print("error in RUNONVIDEO",err)

                        except Exception as err:
                            self.logger.warning("Rect_not_printed: " + str(err))
                            print("Rect_not_printed",err)
            video_writer.write(cv2.resize(frame, (640, 480)))
            #cv2.imshow('Human_Detection', frame)
            # print(1/(time.time()-start))
            #if cv2.waitKey(1) == ord('q'):
            #    break
            # print res




if __name__ == "__main__":
    obj=inference()
    video_source = -1
    obj.runOnVideo2(video_source,obj.net, obj.meta)
    #obj.runOnVideo(None, None, video_source)


    #runOnVideo(net, meta, vid_source)