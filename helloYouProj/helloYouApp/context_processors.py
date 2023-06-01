from .models import Profile, Relationship

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.profile_pic
        return {'picture':pic}
    return {}

def user_name(request):
    if request.user.is_authenticated:
        user_name = Profile.objects.get(user=request.user)
        user_firstname = user_name.first_name
        user_lastname = user_name.last_name
        return {'user_firstname': user_firstname, 'user_lastname': user_lastname}
    return {}

