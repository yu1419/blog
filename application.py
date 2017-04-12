from app import create_app

app = create_app(add_fake=False)
# fake user.password = user.email
app.run()
