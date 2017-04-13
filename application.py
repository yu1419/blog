from app import create_app
application = create_app(add_fake=False)
if __name__ == '__main__':
    # fake user.password = user.email
    application.run(host='0.0.0.0')
