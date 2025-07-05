from fastapi import APIRouter
from .endpoints import wordpress_automation, prompt, user ,auth
route_v1 = APIRouter()
route_v1.include_router((auth.router), prefix='/auth', tags=['auth'])

route_v1.include_router((user.router), prefix='/user', tags=['User Management'])
route_v1.include_router((wordpress_automation.router), prefix='/wordpress-ai', tags=['WordPress Automation'])
route_v1.include_router((prompt.router), prefix='/prompt', tags=['AI Prompt'])