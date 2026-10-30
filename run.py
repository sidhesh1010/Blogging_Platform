import os
from app import create_app, db

# Create the application instance using the factory function
# Reads FLASK_ENV or falls back to 'development'
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Ensure database tables exist for standalone local execution
    with app.app_context():
        db.create_all()

    # Run the local development server with auto-reloading enabled in development
    port = int(os.environ.get('PORT', 5000))
    print(f" * BlogSphere server [{env}] running at: http://127.0.0.1:{port}/")
    app.run(debug=(env == 'development'), host='127.0.0.1', port=port)
