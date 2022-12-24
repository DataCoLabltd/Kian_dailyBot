def map_user_profile_items(request):
    try:
        response = {
            'RoleDescription': request['title'],
            'UserId': request['user_id'],
            'PhoneNumber': request['phone'],
            'FirstName': request['first_name'],
            'LastName': request['last_name'],
            'FullName': request['real_name'],
            'ImageURL': request['image_original'],
            'Email': request['email']
        }
        return response
    except:
        return False
