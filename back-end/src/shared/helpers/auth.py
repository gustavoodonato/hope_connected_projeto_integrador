from src.shared.helpers.token_handler import TokenHandler


def auth(user_id) -> dict:
    return {"Authorization": f"Bearer {TokenHandler.generate(user_id)}"}