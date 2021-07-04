import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import font
import time
import boto3
import requests

BUCKET='inboxgowhich'
OBJECT_NAME='tempFace.png'
DELAY=500
BASE_URL = "https://japaneast.api.cognitive.microsoft.com/face/v1.0/"
SUBSCRIPTION_KEY  = "5fe7753fda7944b9bceaa338a19353d9"
GROUP_NAME = "dakoku"

class Application(tk.Frame):
    def __init__(self,master, video_source=0):
        super().__init__(master)

        self.master.geometry("700x700")
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font( family="Meiryo UI", size=15, weight="normal" )
        self.font_btn_big = font.Font( family="Meiryo UI", size=20, weight="bold" )
        self.font_btn_small = font.Font( family="Meiryo UI", size=15, weight="bold" )

        self.font_lbl_bigger = font.Font( family="Meiryo UI", size=45, weight="bold" )
        self.font_lbl_big = font.Font( family="Meiryo UI", size=30, weight="bold" )
        self.font_lbl_middle = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_small = font.Font( family="Meiryo UI", size=12, weight="normal" )

        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture( video_source )
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT )

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = DELAY #[mili seconds]
        self.update()

    def create_widgets(self):

        #Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text = 'Camera', font=self.font_frame)
        self.frame_cam.place(x = 10, y = 10)
        self.frame_cam.configure(width = self.width+30, height = self.height+50)
        self.frame_cam.grid_propagate(0)

        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=0,padx = 10, pady=10)

        # Frame_Button
        self.frame_btn = tk.LabelFrame( self.master, text='Control', font=self.font_frame )
        self.frame_btn.place( x=10, y=550 )
        self.frame_btn.configure( width=self.width + 30, height=120 )
        self.frame_btn.grid_propagate( 0 )
        '''
        #Snapshot Button
        self.btn_snapshot = tk.Button( self.frame_btn, text='Snapshot', font=self.font_btn_big)
        self.btn_snapshot.configure(width = 15, height = 1, command=self.press_snapshot_button)
        self.btn_snapshot.grid(column=0, row=0, padx=30, pady= 10)
        '''

        # Close
        self.btn_close = tk.Button( self.frame_btn, text='Close', font=self.font_btn_big )
        self.btn_close.configure( width=15, height=1, command=self.press_close_button )
        self.btn_close.grid( column=0, row=0, padx=20, pady=10 )

    def update(self):
        #Get a frame from the video source
        _, frame = self.vcap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

        #self.photo -> Canvas
        self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)

        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imwrite( OBJECT_NAME,
                     cv2.cvtColor( frame1, cv2.COLOR_BGR2RGB ) )
        faceId = self.detectFace()
        person = self.identifyPerson(faceId["faceId"]) 

        if person["candidates"]: #学習データに候補があれば 
            personId = person["candidates"][0]["personId"] 
            print("personId " + personId) 
            personInfo = self.getPersonInfoByPersonId(personId) 
            print(personInfo["name"]) 
            print(personInfo["userData"]) 
        else: 
            print ("No candidates found")

        """
        s3 = boto3.resource('s3')

        bucket = s3.Bucket(BUCKET)
        bucket.upload_file(OBJECT_NAME, OBJECT_NAME)

        s3client = boto3.client('s3')

        url = s3client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : BUCKET, 'Key' : OBJECT_NAME},
        ExpiresIn = 600,
        HttpMethod = 'GET')

        print('-----\n{}\n-----'.format(url))
        """
        self.master.after(self.delay, self.update)

    def press_snapshot_button(self):
        # Get a frame from the video source
        _, frame = self.vcap.read()

        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imwrite( "frame-" + time.strftime( "%Y-%d-%m-%H-%M-%S" ) + ".jpg",
                     cv2.cvtColor( frame1, cv2.COLOR_BGR2RGB ) )

    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()

    def detectFace(self):
        end_point = BASE_URL + "detect?returnFaceId=true&recognitionModel=recognition_04&returnRecognitionModel=false&detectionModel=detection_03&faceIdTimeToLive=600"
        headers = {
            "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY,
            "Content-Type": "application/octet-stream",
            "Host": "japaneast.api.cognitive.microsoft.com"
        }
        # 画像ファイルを開く
        f = open(OBJECT_NAME, "rb")
        reqbody = f.read()
        f.close()

        r = requests.post(
            end_point,
            data = reqbody,
            #json = payload,
            headers = headers
        )
        try:
            faceId = r.json()[0]["faceId"]
            print ("faceId Found:{}".format(faceId))
            return r.json()[0]
        except Exception as e:
            print("faceId not found:{}".format(e))
        return None

    def identifyPerson(self,faceId):
        end_point = BASE_URL + "identify"
        headers = {
            "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY,
            "Host": "japaneast.api.cognitive.microsoft.com"
        }
        faceIds = [faceId]
        payload = {
            "faceIds" :faceIds,
            "personGroupId" :GROUP_NAME,
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5
        }
        r = requests.post(
            end_point,
            json = payload,
            headers = headers
        )
        print(r.json())

        return r.json()[0]

    def getPersonInfoByPersonId(self,personId):
        end_point = BASE_URL + "persongroups/"+ GROUP_NAME +"/persons/" + personId
        headers = {
            "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY,
            "Host": "japaneast.api.cognitive.microsoft.com"
        }
        r = requests.get(
            end_point,
            headers = headers
        )
        print(r.json())
        return r.json()

def main():
    root = tk.Tk()
    app = Application(master=root)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()