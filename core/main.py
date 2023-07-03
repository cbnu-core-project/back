from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 라우터
from routers import clubs, notices, promotions, users, images, schedules
from fastapi.staticfiles import StaticFiles

app = FastAPI()

##########################################################
# CORS 설정 #
origins = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)
##########################################################


@app.get("/")
async def home():
	return {"message": "hello world !"}

# 이미지 staticFiles 마운트
app.mount("/images", StaticFiles(directory="images"), name="images")

# 라우터 사용 설정
app.include_router(clubs.router)
app.include_router(notices.router)
app.include_router(promotions.router)
app.include_router(users.router)
app.include_router(images.router)
app.include_router(schedules.router)