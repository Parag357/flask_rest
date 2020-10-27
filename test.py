from modules import app
import unittest
import json
from mock import patch
from flask import jsonify

class InventoryTest(unittest.TestCase):

	@patch('modules.tables.Product.Query')
	def test_get_success_with_all_values(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1,
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		mock_get.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_get_success_with_id_and_sort(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1,
		"sort":"price"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		mock_get.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_get_success_with_sort_and_order(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		mock_get.assert_called_once()

	@patch('modules.tables.Product.Query')	
	def test_get_success_with_id_only(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		mock_get.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_get_success_with_sort_only(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"sort":"expiry"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		mock_get.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_get_success_with_no_value(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		response=tester.get(url)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		mock_get.assert_called_once()


	@patch('modules.tables.Product.Query',side_effect=AttributeError({"error":"unavailable category"}))
	def test_get_no_data_with_unavailable_category(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":20,
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,500)
		mock_get.assert_called_once()


	@patch('modules.tables.Product.delete')
	def test_delete_success_with_available_id(self,mock_delete):
		#mock_delete.return_value={"msg":"product is deleted"}
		url="/delete/55"
		tester=app.test_client(self)
		response=tester.delete(url)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response_data,[{'msg': 'product is deleted'}])
		mock_delete.assert_called_once_with(u'55') # u is for unicode 

	@patch('modules.tables.Product.delete')
	def test_delete_success_with_unavailable_id(self,mock_delete):
		#mock_delete.return_value={"msg":"product is deleted"}
		url="/delete/5500"
		tester=app.test_client(self)
		response=tester.delete(url)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response_data,[{'msg': 'product is deleted'}])
		mock_delete.assert_called_once_with(u'5500') # u is for unicode 

	# @patch('modules.tables.Product.new')
	# def test_create_success_with_all_values(self,mock_get):
	# 	url="/create"
	# 	tester=app.test_client(self)

	# 	mock_data = {
	# 	"id":1,
	# 	"name":"prod11",
	# 	"price":15,
	# 	"expiry":"09/09/2023"
	# 	}

	# 	response=tester.post(url,data=json.dumps(mock_data))
	# 	statuscode=response.status_code
	# 	self.assertEqual(statuscode,200)
	# 	mock_get.assert_called_once()

	def test_create_failure_with_missing_name(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1,
		"price":15,
		"expiry":"09/09/2023"
		}

		response=tester.post(url,data=json.dumps(mock_data))
		statuscode=response.status_code
		self.assertEqual(statuscode,500)

	def test_create_failure_with_missing_price(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1,
		"name":"prod11",
		"expiry":"09/09/2023"
		}

		response=tester.post(url,data=json.dumps(mock_data))
		statuscode=response.status_code
		self.assertEqual(statuscode,500)

	def test_create_failure_with_missing_expiry(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1,
		"name":"prod11",
		"price":15,
		}

		response=tester.post(url,data=json.dumps(mock_data))
		statuscode=response.status_code
		self.assertEqual(statuscode,500)

	def test_create_failure_with_missing_id(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"price":15,
		"expiry":"09/09/2023",
		"name":"prod11"
		}

		response=tester.post(url,data=json.dumps(mock_data))
		statuscode=response.status_code
		self.assertEqual(statuscode,500)


if __name__ == "__main__":
	unittest.main()

