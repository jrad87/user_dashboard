from django.shortcuts import redirect

def user_redirect(user_session_key, named_route):
    def view_decorator(view):
        def view_wrapper(request, *args):
            if user_session_key in request.session.keys():
                return redirect(named_route)
            else:
                return view(request, *args)
        return view_wrapper
    return view_decorator

def no_user_redirect(user_session_key, named_route):
    def view_decorator(view):
        def view_wrapper(request, *args):
            if user_session_key not in request.session.keys():
                return redirect(named_route)
            else:
                return view(request, *args)
        return view_wrapper
    return view_decorator

def if_not_POST(redirect_to):
    def view_decorator(view):
        def view_wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                return view(request, *args, **kwargs)
            else:
                return redirect(redirect_to)
        return view_wrapper
    return view_decorator
