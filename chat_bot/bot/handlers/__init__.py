from aiogram import Router


def setup_handlers() -> Router:
    from . import (ai_reference, main_menu)
    from .mediator import mediator_handlers
    from .admin_panel import admin_handlers
    from .specialist_logics import specialist_logics_handlers

    router = Router()
    mediator_routers = mediator_handlers()
    specialist_logics_routers = specialist_logics_handlers()
    admin_routers = admin_handlers()

    router.include_router(admin_routers)
    router.include_router(mediator_routers)
    router.include_router(specialist_logics_routers)
    router.include_router(ai_reference.router)
    router.include_router(main_menu.router)
    return router
