from cmath import isnan
from pickle import FALSE
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import cv2
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt 
import json 
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from cryptography.fernet import Fernet
import base64
from .models import users
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
import socket
import struct
import ctypes
from random import randint
import socket, sys, os 
import uuid
from django.forms.models import model_to_dict
import boto3 
from botocore.exceptions import ClientError
from django.contrib.auth.hashers import make_password, check_password
import shutil
import time
import cloudmersive_virus_api_client
from cloudmersive_virus_api_client.rest import ApiException
from pprint import pprint

from datetime import datetime
from Anj import section_01_hashing_and_duplicate_detection


aa = 'VNcUNK1aS8ULQfzjtosyey7lU6KWH4P4VU-z7f4YwLk='
def home (request): #display official storage list 
    lising = []
    client_s3 = boto3.client (
        's3',
        aws_access_key_id = '.............',
        aws_secret_access_key = '..............'
    )                                                      
    repo = client_s3.list_objects_v2(Bucket='official-storage')
    if repo['KeyCount']>0:
        for key in (repo['Contents']):
            lising.append( key['Key'])
        
    context  = {
        'listing': lising
    }
    return render(request, "home.html", context )

def uploadOtpPage(req): #personal storage key sending page
    return render(req, "otp1.html" )


def uploadOtpPageCom(req): #official storage key sending page
    return render(req, "otp2.html" )

def persona(req): #personal storage file upload
    return render(req, "pupload.html")


def personal (request): #display personal storage file list 
    lising = []
    client_s3 = boto3.client (
        's3',
        aws_access_key_id = '..............',
        aws_secret_access_key = '..............'
    )                                                      
    repo = client_s3.list_objects_v2(Bucket='personal-storages')
    print('rep',repo)
    if repo['KeyCount']>0:
        for key in (repo['Contents']):
            lising.append( key['Key'])
        
    context  = {
        'listing': lising
    }
    return render(request, "personal.html", context )

######
def analyse (request):
    cam = cv2.VideoCapture(0)
    username =request.POST.get('username')
    password =request.POST.get('password')
    print(username)
    print(password)
    
    result2 = users.objects.filter(username=username ).values('photo')
    # print(result2.get['photo'])
    print(str(result2[0]['photo']))
    cv2.namedWindow("test")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
    
        k = cv2.waitKey(1)
        
        img_name = "temp//temp.png".format(img_counter)
        # abalyse_img = result2.format(result2)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        try:
            data = DeepFace.verify('photo/'+str(result2[0]['photo']),img_name) 
            data = data['verified']
        except:
            data = (1 == 2)
        print(data)
        break
    cam.release()
    cv2.destroyAllWindows()
    return HttpResponse(data)


########
def decrypt(file):  
    print('hit')
    fernet = Fernet(aa)
 
    # opening the encrypted file
    with open((file), 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open((file), 'wb') as dec_file:
        dec_file.write(decrypted)


def upload(request):
    print(request.POST.get('photo'))
    name = request.POST.get('photo')
    gauth = GoogleAuth()           
    drive = GoogleDrive(gauth)  
    
    f = Fernet(aa)

    with open(name, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open (name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    upload_file_list = [name]
    for upload_file in upload_file_list:
        gfile = drive.CreateFile({'parents': [{'id': request.POST.get('storage')}]})
        # Read file and set it as the content of this instance.
        gfile.SetContentFile(upload_file)
        gfile.Upload() # Upload the file.a
    
    return HttpResponse(1==1)

def accDisable(request):
    username =request.POST.get('username')
    result2 = users.objects.filter(username=username).values('status')
    print("hit", result2)
    if result2:
        result2.update(status = "0")
    return HttpResponse("Done")


def download(request):
    gauth = GoogleAuth()           
    drive = GoogleDrive(gauth)  
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(request.POST.get('storage'))}).GetList()
    for file in file_list:
        print('title: %s, id: %s' % (file['title'], file['id']))

    for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
        print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
        files = file.GetContentFile(file['title'])
        dec = decrypt(file['title'])
    return HttpResponse(1==1) 

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

@csrf_exempt
def saveAccount(request):
    form= UserForm(request.POST or None)
    passw= request.POST.get('password')
    print(form)
    if form.is_valid():
        print("hit")
        dataSave = form.save()
        id = dataSave.pk
        ddd = users.objects.filter(id = id).update(password = make_password(passw))
        return render(request, "signup.html")

def uploadPage(request):
    return render(request, "upload.html")

@csrf_exempt
def logOp(request):
    username =request.POST.get('username')
    password =request.POST.get('password')
    print(username)
    print(password)
    
    result2 = users.objects.filter(username=username  ).values('id', 'password','level','name', 'status')
    result3 = users.objects.filter(username=username, password =password, status ="0" ).values('status')
    res4 = users.objects.filter(username=username, password =password, status ="0" ).values('name')

    print(result3)
    print(result3.exists())
    if(result2.exists()):
        if(result3.exists()):
            return HttpResponse(1==1)
        else:
            if(check_password(password, result2[0]['password'])):
                return JsonResponse(list(result2), safe=False)
            else: 
                return HttpResponse(1==1)

    else:
        return HttpResponse(1==1)


#########
@csrf_exempt
def ddos(requesr):
    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dict = {}
    file_txt = open("dos.txt",'a')
    file_txt.writelines("**********")
    t1= str(datetime.now())
    file_txt.writelines(t1)
    file_txt.writelines("**********")
    file_txt.writelines("n")
    print ("Detection Start .......")
    D_val =10
    D_val1 = D_val+10
    while True:
    
        pkt = s.recvfrom(9999)
        ipheader = pkt[0][14:34]
        ip_hdr = struct.unpack("!8sB3s4s4s",ipheader)
        IP = socket.inet_ntoa(ip_hdr[3])
        print ("Source IP", IP)
        if dict.has_key(IP):
            dict[IP]=dict[IP]+1
            print (dict[IP])
            if(dict[IP]>D_val) and (dict[IP]<D_val1) :

                line = "DDOS Detected "
                file_txt.writelines(line)
                file_txt.writelines(IP)
                file_txt.writelines("n")

            else:
                dict[IP]=1
                download()

def runn(request):
    for i in range(1, 1000):  
        anal() 


########
def sendmail(req): #Key sending to mails 
    random = randint(0, 10)
    subject = 'PERSONAL SECURITY KEY'
    message = 'HI THIS IS YOUR OTP     ' + str(random)
    email_from = '..............@gmail.com'
    recipient_list =  ['............@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse(random)

@csrf_exempt
def sendmails(req):
    print('hit')
    random = uuid.uuid1().int>>64
    subject = 'SECURITY KEY'
    message = 'HI THIS IS YOUR SECURITY KEY     ' + str(random)
    email_from = '.........@gmail.com'
    recipient_list = ['............@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse(str(random))

@csrf_exempt
def saveEdt (request):
    print(request.POST.get('id'))
    users.objects.filter(id="1").update(status='0')
    return HttpResponse('done')
    


#selected file uploading  
@csrf_exempt
def uploadTwo (request):
    name = request.POST.get('photo')

    client_s3 = boto3.client (
        's3',
        aws_access_key_id = '.............',
        aws_secret_access_key = '.................'
    )
    
    upload_file_list = [name]
    for upload_file in upload_file_list:
        f = Fernet(aa)

    with open(upload_file, 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original) #hybrid encryptiion method 
    virus = clean_file(upload_file)
    if str(virus) == "None":
        print('can')
        print('virus   ', virus)
        with open (upload_file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
            try:
                client_s3.upload_file(upload_file,request.POST.get('storage'), upload_file)
                
                
            except ClientError as e:
                print("credentials invalid")

            except Exception as e:
                print(e)

            return HttpResponse('success')
    else:
        return HttpResponse('Virus contained')
        

#selected file download
@csrf_exempt
def downloadTwo (request):

    client_s3 = boto3.client (
        's3',
        aws_access_key_id = '..............',
        aws_secret_access_key = '..................'
    )
    repo = client_s3.list_objects_v2(Bucket=request.POST.get('storage')) #create connection
    
    for key in (repo['Contents']):
        client_s3.download_file(request.POST.get('storage'), key['Key'], key['Key'])
        print(key['Key'])
        decrypt(key['Key']) #decryption method
    return HttpResponse(repo)

#delete files in aws 
def deleteFile(request): 
    client_s3 = boto3.client (
        's3',
        aws_access_key_id = '.............',
        aws_secret_access_key = '.....................'
    )
    repo = client_s3.delete_object(Bucket=request.POST.get('storage'),  Key=request.POST.get('file'))
    return HttpResponse(repo)

def downloadOnefile(request):
    client_s3 = boto3.client (
        's3',
        aws_access_key_id = '............',
        aws_secret_access_key = '..............'
    )
    repo = client_s3.list_objects_v2(Bucket=request.POST.get('storage'))
    client_s3.download_file(request.POST.get('storage'), request.POST.get('file'), request.POST.get('file'))
    decrypt(request.POST.get('file'))
    return HttpResponse(repo)

@csrf_exempt
def takePhoto(request):
    cam = cv2.VideoCapture(0)
    nameGen = randint(12350, 12564354)
    cv2.namedWindow("test")
    
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
    
        k = cv2.waitKey(1)
        
        img_name = str(nameGen)+".png".format(img_counter)
        cv2.imwrite('photo/'+img_name, frame)
        print("{} written!".format(img_name))
        return HttpResponse(img_name)

@csrf_exempt
def processsFiles(request):
    print("hit")
    path = "C://Users//Desktop//Upload" #want to change this path
    files = os.listdir(path)

    for file in files:
        filename,extension = os.path.splitext(file)
        extension = extension[1:]

        if os.path.exists(path+'/'+extension):
            shutil.move(path+'/'+file, path+'/'+extension+'/'+file)
        else:
            os.makedirs(path+'/'+extension)
            shutil.move(path+'/'+file, path+'/'+extension+'/'+file)
    return HttpResponse("done")

#########
def clean_file(request):
    print('na  ', request)
    configuration = cloudmersive_virus_api_client.Configuration()
    configuration.api_key['Apikey'] = 'eb2dd785-d4a5-44e7-9a5f-f24b48c57947'
    api_instance = cloudmersive_virus_api_client.ScanApi(cloudmersive_virus_api_client.ApiClient(configuration))
    input_file = 'attack_DDoS.txt'
    try:
    # Scan a file for viruses
        api_response = api_instance.scan_file(input_file)
        pprint(api_response.found_viruses)
        return api_response.found_viruses
    except ApiException as e:
        print("Exception when calling ScanApi->scan_file: %s\n" % e)

def clean_file_2(request):
    print('na  ', request.POST.get('photo'))
    configuration = cloudmersive_virus_api_client.Configuration()
    configuration.api_key['Apikey'] = 'eb2dd785-d4a5-44e7-9a5f-f24b48c57947'
    api_instance = cloudmersive_virus_api_client.ScanApi(cloudmersive_virus_api_client.ApiClient(configuration))
    input_file = 'attack_DDoS.txt'
    try:
    # Scan a file for viruses
        api_response = api_instance.scan_file(input_file)
        pprint(api_response.found_viruses)
        return HttpResponse(api_response.found_viruses) 
    except ApiException as e:
        print("Exception when calling ScanApi->scan_file: %s\n" % e)




