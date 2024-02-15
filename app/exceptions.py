class InternalAPIError(Exception):
    def __init__(self, message="Bad API usage"):
        super().__init__(message)


class TotpError(ValueError):
    def __init__(self, message="Bad TOTP code"):
        super().__init__(message)


class BadDataFormat(ValueError):
    def __init__(self, message="Bad data format"):
        super().__init__(message)


class NotEnoughFunds(BadDataFormat):
    def __init__(self, message="There is not enough funds to process the transaction"):
        super().__init__(message)


class ContentNotFound(Exception):
    def __init__(self, message="There is no content"):
        super().__init__(message)


class UserNotFound(ContentNotFound):
    def __init__(self, message="User not found"):
        super().__init__(message)


class ItemNotFound(ContentNotFound):
    def __init__(self):
        super().__init__("There is no item with given id")


class NftNotFound(ContentNotFound):
    def __init__(self):
        super().__init__("There is no NFT with given id")


class OfferNotFound(ContentNotFound):
    def __init__(self):
        super().__init__("There is no offer with given id")


class AuctionNotFound(ContentNotFound):
    def __init__(self, message="There is no auction with given id"):
        super().__init__(message)


class NoAvailableNft(BadDataFormat):
    def __init__(self):
        super().__init__("No available NFTs")


class BadPriceData(TypeError):
    def __init__(self, message="Bad price data"):
        super().__init__(message)


class CirclePaymentError(BadDataFormat):
    def __init__(self, message="The payment through Circle is failed"):
        super().__init__(message)


class CircleHistoryNotFound(ContentNotFound):
    def __init__(self, message="There is no data for this transaction. Please, try again later"):
        super().__init__(message)


class NoOnfidoAccount(BadDataFormat):
    def __init__(self, message="There is no Onfido account associated with user"):
        super().__init__(message)


class DoNotHaveAccess(Exception):
    def __init__(self, message="You do not have access to this page"):
        super().__init__(message)


class PhoneNotVerified(DoNotHaveAccess):
    def __init__(self):
        super().__init__("User has not verified the phone")


class BadRequest(Exception):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message)
