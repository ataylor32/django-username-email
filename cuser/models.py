from cuser.abstract import AbstractCUser


class CUser(AbstractCUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Password and email are required. Other fields are optional.
    """
    # class Meta(AbstractCUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'
