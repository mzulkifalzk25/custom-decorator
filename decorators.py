from bson import ObjectId
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

from app.scripts import mongodb_connection


def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            current_user = request.session.get('username')
            print(f"Current User: {current_user}")

            if current_user is not None:
                if request.session.get('username'):
                    user_role = request.session.get('user_role')
                    print(f"User Role: {user_role}")
                    if user_role == "employee":
                        if request.path.startswith('/employee/'):
                            print(f"{request.path.startswith('/employee/')}")
                            return view_func(request, *args, **kwargs)
                        else:
                            print("You don't have permission to access this page.")
                            return redirect('employee:attendance')

                    elif user_role == 'admin':
                        if not request.path.startswith('/employee/'):
                            print(f"{request.path.startswith('/employee/')}")
                            return view_func(request, *args, **kwargs)
                        else:
                            print("You don't have permission to access this page.")
                            return redirect('home')

                else:
                    try:
                        user_role = request.session.get('user_role')

                        if user_role == 'employee':
                            if request.path.startswith('/employee/'):
                                return view_func(request, *args, **kwargs)
                            else:
                                print("You don't have permission to access this page.")
                                return redirect('employee:attendance')

                        elif user_role == 'admin':
                            if not request.path.startswith('/employee/'):
                                return view_func(request, *args, **kwargs)
                            else:
                                print("You don't have permission to access this page.")
                                return redirect('home')

                        else:
                            print("Unauthorized access.")
                            return redirect('employee:attendance')

                    except Exception as e:
                        print(f"An error occurred: {e}")
                        return redirect('user_login')

            else:
                return redirect('user_login')

        except Exception as e:
            print(f"Exception: {e}")
            return redirect('user_login')

    return wrapper



def check_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('user_login')

        user_id = request.session['user_id']
        client = mongodb_connection.mongo_connection()
        db = client['zk']
        collection = db['user_auth']

        user_id = ObjectId(user_id)

        user_data = collection.find_one({'_id': user_id})

        if not user_data:
            return redirect('user_login')

        return func(request, *args, **kwargs)

    return wrapper
