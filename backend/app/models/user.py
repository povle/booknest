from odmantic import Model, Field


class User(Model):
    username: str
    password: str  # FIXME: this should be a hashed password
    email: str = Field(primary_field=True, unique=True)
