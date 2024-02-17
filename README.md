# custom-decorator


Cusom decorator for employee role and type using mongodb. 

It will check for username in he session, if it gets one ( then will check whether the role of logged in user is (admin or employee). And addition to that also checks that the url if it starts with **/employee/** then it means it is for employee and if doesn't starts with **employee** then it is for admin(couldn't use admin/ => url cuz of built-in admin.urls).
