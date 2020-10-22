from modules import app
from modules.endpoints import configure_routes


configure_routes(app)

if __name__ == '__main__':
	app.run()