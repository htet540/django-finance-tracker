from django.contrib.auth.models import Group

ADMIN = "Admin"
MANAGER = "Manager"
USER = "User"

def user_in_group(user, group_name: str) -> bool:
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name=group_name).exists()

def is_admin(user): return user_in_group(user, ADMIN)
def is_manager(user): return user_in_group(user, MANAGER)
def is_user(user): return user_in_group(user, USER)