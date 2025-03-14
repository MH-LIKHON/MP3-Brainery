# =======================================================
# Entry Point for the Flask Application
# =======================================================

from brainery_data import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True, host="0.0.0.0", port=5000)
