from flask import Flask, request, jsonify
from modules.endpoints import configure_routes

def test_delete_success():
	app=Flask(__name__)
	configure_routes(app)
	client=app.test_client()
	url='/create'

	mock_data={
	"name":"prod10",
	"price":"23.5",
	"expiry":"03/03/2026",
    "category_id":1
	}

	response=client.post(url,data=json.dump(mock_data))
	assert response.status_code == 200

