def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', 'login')
    config.add_route('register', 'register')
    config.add_route('logout', 'logout')
    config.add_route('my_photos', 'my')
    config.add_route('manage', 'manage')

    config.add_route('like', 'like/{photo_id}')
    config.add_route('unlike', 'unlike/{photo_id}')
    config.add_route('approve', 'approve/{photo_id}')
    config.add_route('decline', 'decline/{photo_id}')
