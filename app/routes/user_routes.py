from fastapi import APIRouter
from app.controllers.user_controller import signup, login, logout
from app.schemas.schemas import User

router = APIRouter()

# Register the routes and map to the controller functions
router.post("/signup", response_model=User)(signup)
router.post("/login")(login)
router.post("/logout")(logout)