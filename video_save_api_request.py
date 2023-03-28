import json
import logging
import requests
import os
import cv2
import time
import datetime
import traceback
import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Set the filename and bucket name
# filename = 'file.txt'




log_path = r'C:\Users\viora\OneDrive\Desktop\AWS_mahindra\logs'
current_date = str(datetime.datetime.now()).split(' ')[0]
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(filename = os.path.join(log_path,f'api_{current_date}.log'),format='%(asctime)s : %(levelname)s : %(message)s')


logging.info(f"Code execution started")

url = "http://127.0.0.1:8000/iotgateway/read?ids=D1_BLOCK.BSS_SpotWeldingGun_OEM.SpotWeldingGun_Trigger1"

payload = json.dumps({
  "Tag1": "D1_BLOCK.BSS_SpotWeldingGun_OEM.SpotWeldingGun_Trigger1"
})
headers = {
  'Content-Type': 'application/json'
}

# try:
while True:
    try:
        response = requests.request("GET", url,headers=headers,data=payload)
        response_dict = json.loads(response.text)
        weldgun_list = response_dict['readResults']
        first_dict = dict(weldgun_list[0])
        print(f'First dict {first_dict}')
        # second_dict = dict(weldgun_list[1])
        # print(f'First dict {second_dict}')
    except:
        logging.error(traceback.format_exc())

    try:
        if first_dict['v'] == True:
            print('Inside if conditions')
            timestamp_1 = first_dict['t']
            # current_timestamp = int(time.time())
            triger_time = str(datetime.datetime.fromtimestamp(timestamp_1)).replace(' ','_').replace(':','-').replace('.','-')
            date_921  = datetime.datetime.fromtimestamp(timestamp_1 / 1000.0)
            logging.info(f"MG 921 trigger at {triger_time}")
            cap = cv2.VideoCapture(r"C:\Users\viora\OneDrive\Desktop\AWS_mahindra\Weldgun_1\Logistice-Camera 03_weldtip123_weldtip123_20230109090000_20230109092516_1406944_0_82.mp4")
            # Get the frames per second (fps) of the input video stream
            fps = cap.get(cv2.CAP_PROP_FPS)
            # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            filename = f'video_MG921_{triger_time}.mp4'
            out = cv2.VideoWriter(rf'C:\Users\viora\OneDrive\Desktop\AWS_mahindra\video_to_aws\{filename}', fourcc, fps, (640,640))
            x1=1200
            y1=700
            x2=1700
            y2=1900
            # frame_count = int(fps*60*1)
            # cnt = 0
            logging.info(f"video saving for MG921 at {date_921}")
            print(f"video saving for MG921 at {date_921}")
            while(cap.isOpened()):
                ret, frame = cap.read()
                # if frame.any() == None:
                if ret:
                    frame = frame[300:900 , 200:900]
                    frame = cv2.resize(frame, (640,640))
                    out.write(frame)
                else:
                    break
            out.release()
            cap.release()
            # Upload the file to S3
            try:
                bucket_name = 'mahindra-test'
                s3.upload_file(rf'C:\Users\viora\OneDrive\Desktop\AWS_mahindra\video_to_aws\video_MG921_{triger_time}.mp4', bucket_name, filename)
                current_time = datetime.datetime.now()
                logging.info(f'Video has uploaded for {filename} at {current_time}')
                # Generate a pre-signed URL for the uploaded file
                # url = s3.generate_presigned_url(
                #     ClientMethod='get_object',
                #     Params={'Bucket': bucket_name, 'Key': filename},
                #     ExpiresIn=3600)
                print(f'Pre-signed url :{url}')
                logging.info(f"Video upload completed for {url}")
                headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded',}
                params = {
                    'file_name': filename,
                    'triger_timestamp':triger_time,
                }
                response = requests.post('http://13.232.235.59/inference/', params=params, headers=headers)
                logging.info(f'Resquest has made succesfully')
                print(response)
                if first_dict['v'] == True:
                    break
            except Exception as e:
                print(e)
                logging.error(traceback.format_exc())     
               
    except Exception as e:
        print(e)
        logging.error(traceback.format_exc())
    # print(response.json())
    time.sleep(1)
    # break






