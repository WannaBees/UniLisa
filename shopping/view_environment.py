from shopping.cart import userCartItemCount
from shopping.notifications import notifications


def environment(request,site_env):
    notification = None
    notificationKey = request.GET.get("notification")
    if notificationKey is not None:
        notification = notifications[notificationKey]


    loggedIn = request.user.is_authenticated
    username = request.user.username

    result = {}
    if loggedIn:
        shoppingCartItemCount = userCartItemCount(username)
        result =   {'username': username,
                       'loggedIn': True, 'shoppingCartItemCount': shoppingCartItemCount, 'notification': notification}
    else:
        result =  { 'username': username,
                       'loggedIn': False, 'notification': notification }

    merged_result = z = {**result, **site_env}

    return merged_result
