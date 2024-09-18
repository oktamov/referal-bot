from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .groups import add_new_member
    from .users import admin, money, start, help, echo
    from .errors import error_handler

    router = Router()

    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

    router.include_routers(admin.router, money.router, start.router, help.router, error_handler.router,
                           add_new_member.router, echo.router)

    return router
