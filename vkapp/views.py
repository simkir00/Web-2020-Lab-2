from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests

APP_ID = "7720214"
SECRET_KEY = "z85GxS0yRciINemCbHNb"


def index(request):
    href_auth = "https://oauth.vk.com/authorize?" + \
               "client_id=" + APP_ID + \
               "&display=page" + \
               "&redirect_uri=http://localhost:8000/" + \
               "&scope=" + \
               "&response_type=code" + \
               "&v=5.126"

    if (request.method == "GET") & ("code" in request.GET):
        code = request.GET.get("code")
        href_token = "https://oauth.vk.com/access_token?" + \
                     "client_id=" + APP_ID + \
                     "&client_secret=" + SECRET_KEY + \
                     "&redirect_uri=http://localhost:8000/" + \
                     "&code=" + code

        access_data = requests.get(href_token).json()
        if "error" in access_data:
            return HttpResponseRedirect(href_auth)

        access_token = access_data["access_token"]

        user_info_request = "https://api.vk.com/method/users.get?v=5.126&access_token=" + access_token
        user_info = requests.get(user_info_request).json()
        first_name = user_info["response"][0]["first_name"]
        last_name = user_info["response"][0]["last_name"]

        data = {"auth": 1,
                "first_name": first_name,
                "last_name": last_name}

    else:
        data = {"auth": 0,
                "href": href_auth}

    return render(request, "vkapp/index.html", context=data)


def vkpage(request):
    code = request.GET.get("code")
    href_token = "https://oauth.vk.com/access_token?" + \
                 "client_id=" + APP_ID + \
                 "&client_secret=" + SECRET_KEY + \
                 "&redirect_uri=http://localhost:8000/vk_page/" + \
                 "&code=" + code

    access_data = requests.get(href_token).json()
    access_token = access_data["access_token"]

    user_info_request = "https://api.vk.com/method/users.get?v=5.126&access_token=" + access_token
    user_info = requests.get(user_info_request).json()
    first_name = user_info["response"][0]["first_name"]
    last_name = user_info["response"][0]["last_name"]

    # return HttpResponseRedirect(user_info_request)
    return HttpResponse("<h2>Hello, {0} {1}</h2>".format(first_name, last_name))
