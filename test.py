import requests
BASE_URL = "https://westus2.api.cognitive.microsoft.com/face/v1.0/"
SUBSCRIPTION_KEY  = "0cd899ff649740308319ae1d779367a1"
GROUP_NAME = "idle"

def detectFace(imageUrl):
  """
  学習済みのpersonGroupの中で、送信する画像のURLから似ている候補(candidates)を
  取得できます。
  """
  end_point = BASE_URL + "detect?recognitionModel=recognition_03"
  headers = {
      "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY,
      "Content-Type": "application/octet-stream"
  }
  # 画像ファイルを開く
  f = open("tempFace.png", "rb")
  reqbody = f.read()
  f.close()
  payload = {
      "url": imageUrl
  }
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

def identifyPerson(faceId):
  end_point = BASE_URL + "identify"
  headers = {
      "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  faceIds = [faceId]
  payload = {
      "faceIds" :faceIds,
      "personGroupId" :GROUP_NAME,
      #"maxNumOfCandidatesReturned" :maxNumOfCandidatesReturned
  }
  r = requests.post(
      end_point,
      json = payload,
      headers = headers
  )
  print(r.json())

  return r.json()[0]

def getPersonInfoByPersonId(personId):
  end_point = BASE_URL + "persongroups/"+ GROUP_NAME +"/persons/" + personId
  headers = {
    "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  r = requests.get(
    end_point,
    headers = headers
  )
  print(r.json())
  return r.json()

if __name__ == '__main__': 
    #画像から、personを特定するときのサンプルコード 
  image = "https://s.akb48.co.jp/sousenkyo2017/70004.jpg" 
  faceId = detectFace(image) 
  person = identifyPerson(faceId["faceId"]) 
  if person["candidates"]: #学習データに候補があれば 
    personId = person["candidates"][0]["personId"] 
    print("personId " + personId) 
    personInfo = getPersonInfoByPersonId(personId) 
    print(personInfo["name"]) 
    print(personInfo["userData"]) 
  else: 
    print ("No candidates found")