from fastapi import APIRouter
from app.controllers.user_controllers import signup, login, logout
from app.schemas.schemas import UserOut

router = APIRouter()

# Register the routes and map to the controller functions
router.post("/user/signup", response_model=UserOut)(signup)
router.post("/user/login", response_model=UserOut)(login)
router.post("/user/logout")(logout)