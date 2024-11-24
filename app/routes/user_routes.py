from fastapi import APIRouter
from controllers.user_controller import signup, login, logout
from schemas.schemas import User

router = APIRouter()

# Register the routes and map to the controller functions
router.post("/signup", response_model=User)(signup)
router.post("/login")(login)
router.post("/logout")(logout)