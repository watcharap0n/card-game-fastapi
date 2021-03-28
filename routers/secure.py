from fastapi import APIRouter, File, UploadFile, Form, Depends, Response, Request, HTTPException
from fastapi_login import LoginManager
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from firebase_admin import credentials
from db import MongoDB
import firebase_admin
import os
from pusher import Pusher
import pyrebase
from typing import Optional
from firebase_admin import auth

router = APIRouter()
SECRET = 'watcharaponweeraborirak'
manager = LoginManager(SECRET, tokenUrl='/secure/login', use_cookie=True)

var_authentication = os.environ.get
var_mongodb = os.environ['MONGODB_URI']
db = MongoDB(database_name='Poker', uri=var_mongodb)
# db = MongoDB(database_name='Poker', uri='mongodb://127.0.0.1:27017')

pusher_client = Pusher(
    app_id='1109558',
    key='0e4e34e901bbfddd5557',
    secret='b672e605bf72fbd0ec03',
    cluster='us2',
    ssl=True
)

set_firebase = {
    "apiKey": os.environ['apiKey'],
    "authDomain": os.environ['authDomain'],
    "projectId": os.environ['projectId'],
    "databaseURL": os.environ['databaseURL'],
    "storageBucket": os.environ['storageBucket'],
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId'],
    "measurementId": os.environ['measurementId']
}

set_authentication = {
    "type": os.environ['type'],
    "project_id": os.environ['project_id'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'].replace("\\n", "\n"),
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    "auth_uri": os.environ['auth_uri'],
    "token_uri": os.environ['token_uri'],
    "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url": os.environ['client_x509_cert_url']
}


class Config_firebase:
    def __init__(self, path_db, path_auth):
        self.path_db = path_db
        self.path_auth = credentials.Certificate(path_auth)
        firebase_admin.initialize_app(self.path_auth)

    def authentication(self):
        firebase = self.path_db
        pb = pyrebase.initialize_app(firebase).auth()
        return pb


config = Config_firebase(path_db=set_firebase, path_auth=set_authentication)
pb = config.authentication()


@manager.user_loader
async def load_user(email: Optional[str] = None, password: Optional[str] = None):
    user = pb.sign_in_with_email_and_password(email, password)
    return user


def response_cookies(user, response):
    auth_cookie = auth.create_session_cookie(id_token=user['idToken'], expires_in=timedelta(hours=1))
    check_verify = auth.get_user_by_email(email=user['email'])
    verify_email = check_verify.email_verified
    manager.set_cookie(response, str(auth_cookie))
    return verify_email


@router.post('/login')
async def login(
        response: Response,
        data: OAuth2PasswordRequestForm = Depends(),
        remember: list = Form(...)
):
    email = data.username
    password = data.password
    try:
        if remember == ['checked']:
            user = await load_user(email, password)
            response.set_cookie(key='email_login', value=email)
            response.set_cookie(key='password_login', value=password)
            verify_email = response_cookies(user, response)
            if verify_email:
                return {'message': user, 'status': True}
            pb.send_email_verification(user['idToken'])
            return {'message': 'please check your email to verify your account', 'fg': True}
        user = await load_user(email, password)
        verify_email = response_cookies(user, response)
        if verify_email:
            return {'message': user, 'status': True}
        pb.send_email_verification(user['idToken'])
        return {'message': 'please check your email to verify your account', 'fg': True}
    except:
        return {'message': 'Email or Password Invalid', 'status': False}


@router.post('/register')
async def register(
        request: Request,
        file: UploadFile = File(...),
        email: str = Form(...),
        password: str = Form(...),
        username: str = Form(...),
):
    # host = request.url.hostname
    # scheme = request.url.scheme
    uploads_dir = os.path.join('static', 'uploads')
    file_input = os.path.join(uploads_dir, file.filename)
    https_dir = os.path.join(f'https://game-card-watcharapon.herokuapp.com', file_input)
    # https_dir = os.path.join(f'{scheme}//:{host}', file_input)
    user = auth.create_user(
        email=email,
        password=password,
        display_name=username,
        photo_url=https_dir
    )
    data = {
        'email': email,
        'password': password,
        'username': username,
        'photo_url': file_input,
        'pwd_hash': ''
    }
    print(user.uid)
    db.insert_one(collection='register', data=data)
    with open(file_input, 'wb+') as uploads_file:
        uploads_file.write(file.file.read())
        uploads_file.close()
    return {'user': user}


@router.get('/socket_auth')
def socket_auth(request: Request):
    token = request.cookies.get('access-token')
    try:
        check_session = auth.verify_session_cookie(token)
        auth.revoke_refresh_tokens(check_session['sub'])
        return check_session
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=400, detail={'description': 'bad request'})


@router.get('/cookie_login')
async def cookies_login(request: Request):
    email = request.cookies.get('email_login')
    password = request.cookies.get('password_login')
    return {'email': email, 'password': password}


@router.post('/forgot_password')
async def forgot_password(email: str = Form(...)):
    pb.send_password_reset_email(email)
    return {'email': 'please check your email'}


@router.get('/cookie_clear')
async def cookie_clear(response: Response):
    response.delete_cookie('email_login')
    response.delete_cookie('password_login')
    return {'status': 'success'}


@router.get('/logout')
async def clean_session(response: Response, request: Request):
    token = request.cookies.get('access-token')
    if not token:
        return RedirectResponse(url='/root_login')
    try:
        decoded_claims = auth.verify_session_cookie(token, check_revoked=True)
        auth.revoke_refresh_tokens(decoded_claims['sub'])
        response.set_cookie('access-token', value='logout', expires=0)
        return RedirectResponse(url='/root_login')
    except auth.RevokedSessionCookieError:
        return RedirectResponse(url='/root_login')
    except auth.InvalidSessionCookieError:
        return RedirectResponse(url='/root_login')
