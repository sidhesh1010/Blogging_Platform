import os
from app import create_app, db

# Create the application instance using the factory function
app = create_app()

# Ensure database tables exist in the instance folder
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Run the local development server with auto-reloading enabled
    port = int(os.environ.get('PORT', 5000))
    print(f" * BlogSphere server running at: http://127.0.0.1:{port}/")
    app.run(debug=True, host='127.0.0.1', port=port)
