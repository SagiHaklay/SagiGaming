from dataclasses import dataclass

@dataclass
class MessageResponse:
    message: str
    is_success: bool
    def __init__(self, message: str, is_success=True):
        self.message = message
        self.is_success = is_success

@dataclass
class CartResponse:
    cart_id: int
    user_id: int | None
    def __init__(self, cart_id: int, user_id=None):
        self.cart_id = cart_id
        self.user_id = user_id

@dataclass
class RatingResponse:
    avg_rating: float
    def __init__(self, avg_rating: float):
        self.avg_rating = avg_rating