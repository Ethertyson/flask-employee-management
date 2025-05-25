# Created by Pritanshu on 2025-05-20

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)