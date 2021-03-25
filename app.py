from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import uvicorn
import time
from routers import secure, card
from routers.secure import auth
from pusher import Pusher

app = FastAPI()

app.include_router(
    secure.router,
    prefix='/secure',
    tags=['secure'],
    responses={418: {'description': "I'm a teapot"}},
)

app.include_router(
    card.router,
    prefix='/card',
    tags=['card'],
    responses={418: {'description': "I'm a teapot"}}
)

app.mount('/static', StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory='templates')

pusher_client = Pusher(
    app_id='1109558',
    key='0e4e34e901bbfddd5557',
    secret='b672e605bf72fbd0ec03',
    cluster='us2',
    ssl=True
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    process_time = str('{}'.format(round(process_time, 5)))
    response.headers["X-Process-Time"] = process_time
    return response


@app.get('/')
@app.get('/root_login')
async def root_login(request: Request):
    return template.TemplateResponse('login.vue', context={'request': request})


@app.get('/root_register')
async def root_login(request: Request):
    return template.TemplateResponse('register.vue', context={'request': request})


@app.get('/card')
async def card(request: Request):
    token = request.cookies.get('access-token')
    if not token:
        return RedirectResponse(url='/root_login')
    if token:
        try:
            check_session = auth.verify_session_cookie(token)
            auth.revoke_refresh_tokens(check_session['sub'])
            pusher_client.trigger('secure', 'session', check_session)
            return template.TemplateResponse('card.vue', context={'request': request})
        except auth.RevokedSessionCookieError:
            return RedirectResponse(url='/root_login')
        except auth.InvalidSessionCookieError:
            return RedirectResponse(url='/root_login')
    return template.TemplateResponse('card.vue', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app:app', port=8080, host='0.0.0.0', debug=True)
