from app import create_app

# first use create_mysql_dabatase to create a blog dabatase in my_sql
# mysql user name and password are stored in environment variables
# set add_fake true to add data
# user password is equal to user email
application = create_app(add_fake=False)

if __name__ == '__main__':
    # fake user.password = user.email
    application.run(host='0.0.0.0')
