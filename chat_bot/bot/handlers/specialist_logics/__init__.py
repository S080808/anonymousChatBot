from aiogram import Router


def specialist_logics_handlers():
    router = Router()
    from . import register_specialist, specialist_available

    router.include_router(register_specialist.router)
    router.include_router(specialist_available.router)
    return router
