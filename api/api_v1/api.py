from fastapi import APIRouter, Depends

from api.api_v1.endpoints import auth, user, wordpress_automation, prompt

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["User Management"],
                          dependencies=[Depends(user.reusable_oauth2)])

api_router.include_router(wordpress_automation.router, prefix="/wordpress-ai"
                          , tags=["WordPress Automation"],
                          dependencies=[Depends(wordpress_automation.reusable_oauth2)])  
api_router.include_router(prompt.router, prefix="/prompt",
                          tags=["AI Prompt"],
                          dependencies=[Depends(prompt.reusable_oauth2)])
