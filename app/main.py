from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn



# get configured env values
from app.core.config import HOST_ID, PORT_ID, RELOAD_STATE, DEBUG
from app.db.mongodb import get_db

# include router here
from app.api.endpoints.users import router as UserRouter
from app.api.endpoints.chats import router as ChatRouter
from app.api.endpoints.foods import router as FoodRouter
from app.api.endpoints.food_histories import router as FoodHistoryRouter
from app.api.endpoints.temp_end import router as TempFoodRouter

# include middleware are herer
from app.api.middleware.rate_limiter import add_rate_limit

app = FastAPI()

# get database config method is here
db = get_db()

# for cors middleware /// aka default middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# include the middleware here
add_rate_limit(app) # this is the api call rate limiting middlewaer

# for routes from app.api.endpoints /// include the routes here
app.include_router(UserRouter, tags=["User"], prefix="/api/user") # user route
app.include_router(ChatRouter, tags=["Chat"], prefix="/api/ai") # chat route
app.include_router(FoodRouter, tags=["Food"], prefix="/api/food") # food router
app.include_router(FoodHistoryRouter, tags=["Food History"], prefix="/api/food-history") # food history route
app.include_router(TempFoodRouter, tags=["Temporary Foods"], prefix="/api/temp/food") # temp food router

# calling root directory
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to food recommendation app"}

    
# main method to run the application ///// run api with command
if __name__ == "__main__":
    uvicorn.run(app, host=HOST_ID, port=PORT_ID, reload=RELOAD_STATE, debug=DEBUG)