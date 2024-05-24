import typing

from pydantic import BaseModel


class User(BaseModel):
    id: typing.Optional[int] = None
    name: typing.Optional[str]
    surname: typing.Optional[str]
    role: typing.Optional[str]
    info: typing.Optional[str] = None


class CraneBrand(BaseModel):
    id: typing.Optional[int] = None
    brand: typing.Optional[str] = None
    info: typing.Optional[str] = None


class CraneBrandSelect(BaseModel):
    id: int = None
    brand: str
    info: str = None


class CraneModelSelect(BaseModel):
    """
    Model for selecting CraneModel
    Args:
        model: str
        id: int
        brand_id: int
        crane_brand: str
        crane_type: str
    """

    model: typing.Optional[str] = None
    id: typing.Optional[int] = 0
    brand_id: typing.Optional[int] = 0
    crane_brand: typing.Optional[str] = ''
    crane_type: typing.Optional[str] = ''


class CraneModelDelete(BaseModel):
    model: typing.Optional[str] = None


class CraneModel(BaseModel):
    id: typing.Optional[int] = None
    brand_id: typing.Optional[int]
    model: str
    description: typing.Optional[str] = None
    crane_type: typing.Optional[str] = None
    load_moment: typing.Optional[float] = None
    boom_length: typing.Optional[float] = None
    lifting_capacity_max: typing.Optional[float] = None
    lifting_capacity_end: typing.Optional[float] = None
    height_anker: typing.Optional[float] = None
    height_anker_support: typing.Optional[float] = None
    height_anker_C38: typing.Optional[float] = None
    height_anker_C45: typing.Optional[float] = None
    height_anker_C60: typing.Optional[float] = None


class CraneModelUpdate(BaseModel):
    id: typing.Optional[int] = None
    brand_id: typing.Optional[int] = None
    model: typing.Optional[str] = None
    description: typing.Optional[str] = None
    crane_type: typing.Optional[str] = None
    load_moment: typing.Optional[float] = None
    boom_length: typing.Optional[float] = None
    lifting_capacity_max: typing.Optional[float] = None
    lifting_capacity_end: typing.Optional[float] = None
    height_anker: typing.Optional[float] = None
    height_anker_support: typing.Optional[float] = None
    height_anker_C38: typing.Optional[float] = None
    height_anker_C45: typing.Optional[float] = None
    height_anker_C60: typing.Optional[float] = None


class CranStockModel(BaseModel):
    id: typing.Optional[int] = None
    model_id: typing.Optional[int] = None
    coordinates: typing.Optional[str] = None
    on_the_go: typing.Optional[bool] = None
    info: typing.Optional[str] = None


class MailingList(BaseModel):
    id: typing.Optional[int] = None
    company_name: typing.Optional[str]
    email: typing.Optional[str] = None
    comp_info: typing.Optional[str] = None
    comments: typing.Optional[str] = None


class RentalApplication(BaseModel):
    id: typing.Optional[int] = None
    name: str | None
    email: str | None
    phone: typing.Optional[str] = None
    machinery_id: int | None
    user_msg: typing.Optional[str] = None
    status: typing.Optional[bool] = None


class UserLoginForm(BaseModel):
    username: str
    password: str


class SelectUser(BaseModel):
    id: typing.Optional[int] = None
    username: typing.Optional[str] = None


class UpdtUser(BaseModel):
    username: typing.Optional[str] = None
    passw: typing.Optional[str] = None
