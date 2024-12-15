from app.base.api.router import router

tags = ['register']
@router.post(
    '/register/create',
    tags=tags,
)
def register():
    return 'ok'