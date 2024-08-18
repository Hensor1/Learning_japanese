from app import create_app, create_admin_user

application = create_app()
with application.app_context():
    create_admin_user()


if __name__ == "__main__":
    application.run(debug=True)
