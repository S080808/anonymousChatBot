from aiogram import Router


def admin_handlers():
    router = Router()
    from . import admin_menu, callback_handlers, pagination

    router.include_router(admin_menu.router)
    router.include_router(callback_handlers.router)
    router.include_router(pagination.router)
    return router
