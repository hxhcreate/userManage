from api.user import app
from config.settings import SERVER_PORT

if __name__ == '__main__':
    app.run(host="localhost", port=SERVER_PORT, debug=True)
