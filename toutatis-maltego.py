from toutatis import *
import json
from MaltegoTransform import *
import json

with open('config.json') as json_file:
    data = json.load(json_file)

username=sys.argv[1]
sessionsID=data["sessionsID"]
mt = MaltegoTransform()
#print(username)

trx = MaltegoTransform()
userId=getUserId(username,sessionsID)

recoveryemail=recoveryEmail(username)
cookies = {'sessionid': sessionsID}
headers = {'User-Agent': 'Instagram 64.0.0.14.96',}
response = get('https://i.instagram.com/api/v1/users/'+userId+'/info/', headers=headers, cookies=cookies)
info = json.loads(response.text)
infos = info["user"]
try:
    publicEmail=infos["public_email"]
    if publicEmail!="":
        trx.addEntity("maltego.EmailAddress", str(publicEmail)).setNote("Public Email")
except:
    pass
try:
    publicPhone=str(infos["public_phone_country_code"]+infos["public_phone_number"])
    if publicPhone!="":
        trx.addEntity("maltego.PhoneNumber", str(publicPhone)).setNote("Public Phone number")
except:
    publicPhone=""
    pass
info = {"username":username,"userID":userId,"FullName":infos["full_name"],"biography":str(infos["biography"]),"public_phone_number":publicPhone,"recoveryEmail":recoveryemail,"ProfilePicture":infos["profile_pic_url"]}




isnta = trx.addEntity("quidam.Instagramaccount", username)
isnta.addProperty(fieldName="Biography",value=str(infos["biography"]))
isnta.addProperty(fieldName="userID",value=str(info["userID"]))
isnta.addProperty(fieldName="FullName",value=str(info["FullName"]))
isnta.addProperty(fieldName="Verified",value=str(str(infos['is_verified'])))
isnta.addProperty(fieldName="Is_buisness_Acount",value=str(str(infos["is_business"])))
isnta.addProperty(fieldName="Is_private_Account",value=str(str(infos["is_private"])))
isnta.addProperty(fieldName="Follower",value=str(str(infos["follower_count"])))
isnta.addProperty(fieldName="Following",value=str(str(infos["following_count"])))
isnta.addProperty(fieldName="Number_of_posts",value=str(str(infos["media_count"])))
isnta.addProperty(fieldName="Number_of_tag_in_posts",value=str(str(infos["following_tag_count"])))
isnta.addProperty(fieldName="External_url",value=str(str(infos["external_url"])))
isnta.addProperty(fieldName="IGTV_posts",value=str(str(infos["total_igtv_videos"])))
isnta.addProperty(fieldName="Biography",value=str(str(infos["biography"])))

if info["recoveryEmail"]!="NULL":
    trx.addEntity("maltego.EmailAddress", str(info["recoveryEmail"])).setNote("Recovery Email")
trx.addEntity("maltego.Image", username+" Profile Picture").setIconURL(info["ProfilePicture"].split("?")[0])


trx.addUIMessage("completed!")
print(trx.returnOutput())
