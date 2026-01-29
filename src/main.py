from di.container import Container
from web.module.app import create_app


def main():
    container = Container()
    app = create_app(container)
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
