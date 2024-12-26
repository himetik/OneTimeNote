import sys
from web.app.factory import make_app


app = make_app()


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8000)
    except Exception as error:
        sys.exit(1)
