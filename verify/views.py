from django.shortcuts import render, redirect #puedes importar render_to_response
from verify.forms import UploadForm, LoginForm
from verify.models import Registro, Sesion
from azure.storage.blob import BlockBlobService, PublicAccess, ContentSettings
from django.conf import settings #or from my_project import settings
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
import time
import os



# Create your views here.
def pictures_list(request):
    return render(request, 'verify/pictures_list.html', {})

def upload_file(request):
    f = time.strftime('/%Y/%m/%d')
    if request.method == 'POST':
      form = UploadForm(request.POST, request.FILES)
      if form.is_valid():
        name_replace = request.FILES['docfile'].name.replace(" ","_")
        name_replace = name_replace.replace("(","")
        name_replace = name_replace.replace(")","")
        name_str = time.strftime('%s') + "_" + request.POST['nombre_completo'].replace(" ","_") + "_" + name_replace
        block_blob_service = BlockBlobService(account_name='storage2ia', account_key='zYWmupNNK0F9RBZkrapMiiMuq9neJRcS44R3WTkJVeME45NTYxOoaENsN+Da5EUKd9Gcto9fG/Wh9zmzSyz0Ag==')
        subscription_key = 'c03d52b919e941de955053eced06461f'
        headers = {
          # Request headers
          'Content-Type': 'application/json',
          'Ocp-Apim-Subscription-Key': subscription_key,
        }
        uri_base = 'https://eastus2.api.cognitive.microsoft.com'
        params = {
          'returnFaceId': 'true',
          'returnFaceLandmarks': 'false',
          'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }
        newdoc = Registro(
          ruta='https://storage2ia.blob.core.windows.net/verify/' + name_str,
          nombre_completo = request.POST['nombre_completo'],
          username = request.POST['username'],
          docfile = request.FILES['docfile']
        )
        newdoc.save(form)
        path = os.path.join(settings.MEDIA_ROOT+'/documents'+f, name_str)         
        block_blob_service.create_blob_from_path(
          'verify',
          name_str,
          path,
          content_settings=ContentSettings(content_type='image/png')
        )
        url_img = 'https://storage2ia.blob.core.windows.net/verify/' + name_str
        body = {'url': url_img} 

        try:
          # Execute the REST API call and get the response.
          response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers, params=params)
          parsed = json.loads(response.text)
          Registro.objects.filter(id=newdoc.id).update(faceId=parsed[0]["faceId"])
          
        except Exception as e:
          print('Error:')
          print(e)
       
        '''return redirect("uploads")'''
    else:
        form = UploadForm()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'verify/upload.html', {'form': form})

def login(request):
  f = time.strftime('/%Y/%m/%d')
  if request.method == 'POST':
    form = LoginForm(request.POST, request.FILES)
    if form.is_valid():
      name_replace = request.FILES['docfile'].name.replace(" ","_")
      name_replace = name_replace.replace("(","")
      name_replace = name_replace.replace(")","")
      name_str = time.strftime('%s') + "_" + request.POST['username'].replace(" ","_") + "_" + name_replace
      block_blob_service = BlockBlobService(account_name='storage2ia', account_key='zYWmupNNK0F9RBZkrapMiiMuq9neJRcS44R3WTkJVeME45NTYxOoaENsN+Da5EUKd9Gcto9fG/Wh9zmzSyz0Ag==')
      
      new_sesion = Sesion(
        ruta='https://storage2ia.blob.core.windows.net/verify/' + name_str,
        username = request.POST['username'],
        sesion_file = request.FILES['docfile']
      )
      new_sesion.save(form)
      path = os.path.join(settings.MEDIA_ROOT+'/documents'+f, name_str)         
      block_blob_service.create_blob_from_path(
        'verify',
        name_str,
        path,
        content_settings=ContentSettings(content_type='image/png')
      )

      subscription_key = 'c03d52b919e941de955053eced06461f'
      headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
      }
      uri_base = 'https://eastus2.api.cognitive.microsoft.com'
      params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
      }

      url_img = 'https://storage2ia.blob.core.windows.net/verify/' + name_str
      body = {'url': url_img} 

      try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers, params=params)
        parsed = json.loads(response.text)

        try:
          Sesion.objects.filter(id=new_sesion.id).update(faceId=parsed[0]["faceId"])
        except Exception as e:
          print(e)
          return redirect("login_failed")

        params = {}
        try:
          registro = Registro.objects.get(username=request.POST['username'])
          #print(registro)
          url_img = 'https://storage2ia.blob.core.windows.net/verify/' + name_str
          body = {
            'faceId1': registro.faceId,
            'faceId2': parsed[0]["faceId"]
          } 

          try:
            response = requests.request('POST', uri_base + '/face/v1.0/verify', json=body, data=None, headers=headers, params=params)
            parsed = json.loads(response.text)
            if parsed["isIdentical"] == True:
              return redirect("login_success")
            else:
              return redirect("login_failed")
          except Exception as e:
            print('Error:')
            print(e)
            return redirect("login_failed")


        except Exception as e:
          print('Error:')
          print(e)
          return redirect("error")
        
      except Exception as e:
        print('Error:')
        print(e)
        return redirect("error")

  else:
    form = LoginForm()

  return render(request, 'verify/login.html', {'form': form})

def error(request):
  return render(request, 'verify/error.html')

def success(request):
  return render(request, 'verify/success.html')

def failed(request):
  return render(request, 'verify/failed.html')