from django.contrib.auth.models import User

# context to provide user name globally to all templates
def user_name(request):
    user_name = None
    if request.session.get('user_id'):
        current_user = User.objects.get(id=request.session.get('user_id')) 
        user_name = f'{current_user.first_name} {current_user.last_name}' 
    return {'user_name': user_name}
