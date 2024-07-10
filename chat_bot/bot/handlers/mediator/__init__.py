from aiogram import Router


def mediator_handlers():
    router = Router()
    from . import in_chat, start_search

    router.include_router(in_chat.router)
    router.include_router(start_search.router)
    return router
