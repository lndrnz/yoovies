from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

from django.http import JsonResponse
import djwto.authentication as auth
from .models import Account
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json

class AccountListEncoder(ModelEncoder):
    model = Account
    properties = ["first_name", "id"]


class AccountDetailEncoder(ModelEncoder):
    model = Account
    properties = [
        "email",
        "first_name",
        "last_name",
        "username",
        "password",
        "is_active",
        "date_joined",

    ]

@require_http_methods(["GET"])
def api_user_token(request):
    if "jwt_access_token" in request.COOKIES:
        token = request.COOKIES["jwt_access_token"]
        if token:
            return JsonResponse({"token": token})
    response = JsonResponse({"token": None})
    return response

@auth.jwt_login_required
def get_some_data(request):
    token_data = request.payload
    response = JsonResponse({"token": token_data['user']})
    return response

@require_http_methods(["GET", "POST"])
def api_list_accounts(request):
    if request.method == "GET":
        attendees = Account.objects.all()
        return JsonResponse(
            {"accounts": attendees},
            encoder=AccountListEncoder,
        )
    else:
        try:
            content = json.loads(request.body)
            # account = Account.objects.create(**content)
            nusername = content["username"]
            npassword = content["password"]
            nfirstname = content["first_name"]
            nlastname = content["last_name"]
            nemail= content["email"]
            account = Account.objects.create_user(
                username=nusername, password=npassword, email=nemail, first_name = nfirstname, last_name = nlastname
            )
            account.save()
            login(request, account)
            return JsonResponse(
                account,
                encoder=AccountDetailEncoder,
                safe=False,
            )
        except:
            response = JsonResponse(
                {"message": "Some credentials are not unique. Please try again to place new credentials."}
            )
            response.status_code = 400
            return response

@require_http_methods(["DELETE", "PUT", "GET"])
def api_show_account(request, pk):
    if request.method == "GET":
        account = Account.objects.get(id=pk)
        return JsonResponse(
            account, encoder=AccountDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        count, _ = Account.objects.filter(id=pk).delete()
        Account.objects.filter(id = pk).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        nusername = content["username"]
        npassword = make_password(content["password"])
        nfirstname = content["first_name"]
        nlastname = content["last_name"]
        nemail= content["email"]

        Account.objects.filter(id=pk).update(username=nusername, password=npassword, email=nemail, first_name = nfirstname, last_name = nlastname)

        account = Account.objects.get(id=pk)
        return JsonResponse(
            account,
            encoder=AccountDetailEncoder,
            safe=False,
        )
@require_http_methods(["POST"])
def neo_authenticate(request):
    nusername = request.POST['username']
    npassword = request.POST['password']
    user = authenticate(request, username=nusername, password=npassword)
    if user is not None:
        login(request, user)
        # logout(request)
        # print(request.user.is_authenticated) #used to test if login and logout actually changed authenticaiotn, noticed that sessionid in cookies would be removed if logout, could use as replacedment for jwt access token
        return JsonResponse({'message':'got it'})
    else:
        response = JsonResponse(
        {"message": "Some credentials are not unique. Please try again to place new credentials."}
        )
        response.status_code = 400
        return response

@require_http_methods(["DELETE"])
def neo_logout(request):
    logout(request)
        # logout(request)
        # print(request.user.is_authenticated) #used to test if login and logout actually changed authenticaiotn, noticed that sessionid in cookies would be removed if logout, could use as replacedment for jwt access token
    return JsonResponse({'message':'got it'})

