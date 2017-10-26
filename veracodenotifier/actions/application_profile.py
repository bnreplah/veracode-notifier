from veracodenotifier.helpers.exceptions import VeracodeAPIError


def pre_action(api):
    pass


def action(api):
    return {"type": "create", "message": "application profile created"}


def post_action(api):
    pass
