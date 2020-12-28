from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from keyboards.inline.base_callback_data import links_callback

links_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Аккаунты",
                callback_data="links:author"
            ),
            InlineKeyboardButton(
                text="Приложения",
                callback_data="links:apps"
            )
        ],
        [
            InlineKeyboardButton(
                text="Другие ссылки",
                callback_data="links:other"
            )
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel"
            )
        ]
    ])

author_links = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Telegram",
                url="t.me"
            ),
            InlineKeyboardButton(
                text="Facebook",
                url="f.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Twitter",
                url="t.com"
            ),
            InlineKeyboardButton(
                text="VK.com",
                url="t.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Instagram",
                url="instagram.com"
            ),
            InlineKeyboardButton(
                text="Google Play",
                url="instagram.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back:back_to_links_menu"
            )
        ]
    ]
)

apps_links = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Knowledge Book",
                url="kb.com"
            ),
            InlineKeyboardButton(
                text="Banners Editor",
                url="be.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Ciphers",
                url="c.com"
            ),
            InlineKeyboardButton(
                text="Deviations",
                url="d.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="MGL",
                url="mgl.com"
            ),
            InlineKeyboardButton(
                text="Guess The Block",
                url="gtb.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back:back_to_links_menu"
            )
        ]
    ]
)

other_links = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="GeekStand.top",
                url="geekstand.top"
            ),
            InlineKeyboardButton(
                text="Other Link 2",
                url="tt.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back:back_to_links_menu"
            )
        ]
    ]
)

secret_links = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="GeekStand.top",
                url="geekstand.top"
            ),
            InlineKeyboardButton(
                text="Other Link 2",
                url="tt.com"
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back:back_to_links_menu"
            )
        ]
    ]
)
