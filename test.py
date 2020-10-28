from modules import app
import unittest
import json
from mock import patch
from flask import jsonify
from sqlalchemy.exc import IntegrityError

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


	# @patch('modules.tables.Product.Query')
	# def test_get_no_data_with_unavailable_category(self,mock_get):
	# 	url="/get"
	# 	tester=app.test_client(self)

	# 	mock_data = {
	# 	"category_id":20,
	# 	"sort":"price",
	# 	"order":"desc"
	# 	}

	# 	response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
	# 	statuscode=response.status_code
	# 	self.assertEqual(statuscode,200)
	# 	mock_get.assert_called_once()


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

	@patch('modules.tables.Product.new')
	def test_create_success_with_all_values(self,mock_create):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod21",
		"price":15.0,
		"expiry":"09/09/2023",
		"category_id":1
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		mock_create.assert_called_once()

	def test_create_failure_with_negative_price(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod11",
		"price":-15.0,
		"expiry":"09/09/2023",
		"category_id":1
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,400)

	def test_create_failure_with_missing_name(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"price":15,
		"expiry":"09/09/2023",
		"category_id":1
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,400)

	def test_create_failure_with_missing_price(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod11",
		"expiry":"09/09/2023",
		"category_id":1,
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,400)

	def test_create_failure_with_missing_expiry(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod11",
		"price":15,
		"category_id":1
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,400)

	def test_create_failure_with_missing_id(self):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod11",
		"price":15,
		"expiry":"09/09/2023"
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,400)

	@patch('modules.tables.Product.new')
	def test_create_failure_with_duplicate_name(self,mock_create):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod1",
 	  	"price":15.0,
 	  	"expiry":"09/09/2023",
 	  	"category_id":2	
		}

		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		mock_create.assert_called_once()

	# @patch('modules.tables.Product.new')
	# def test_create_failure_with_unavailable_category(self,mock_create):
	# 	url="/create"
	# 	tester=app.test_client(self)

	# 	mock_data = {
	# 	"name":"prod11",
	# 	"price":15.0,
	# 	"expiry":"09/09/2023",
	# 	"category_id":111
	# 	}

	# 	response=tester.post(url,data=json.dumps(mock_data))
	# 	statuscode=response.status_code
	# 	self.assertEqual(statuscode,500)
	# 	mock_create.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_update_success_with_name_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"name":"prod15"
		}
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		mock_update.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_update_success_with_price_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"price":25
		}
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		mock_update.assert_called_once() 

	@patch('modules.tables.Product.Query')
	def test_update_success_with_expiry_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"expiry":"07/07/2023"
		}
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		mock_update.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_update_success_with_category_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"name":"prod15"
		}
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		mock_update.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_update_success_with_all_values(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"name":"prod15",
		"price":07,
		"expiry":"07/07/2023",
		"category_id":1
		}
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		mock_update.assert_called_once()

	@patch('modules.tables.Product.Query')
	def test_update_with_no_values(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		response=tester.post(url)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,404)
		self.assertEqual(response_data,{'msg':'nothing to update'})
		mock_update.assert_called_once()

	# @patch('modules.tables.Product.Query')
	# def test_update_with_wrong_id(self,mock_update):
	# 	url="/update/790"
	# 	tester=app.test_client(self)
	# 	mock_data={
	# 	"name":"prod15",
	# 	"price":07,
	# 	"expiry":"07/07/2023",
	# 	"category_id":1
	# 	}
	# 	response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
	# 	print(response)
	# 	response_data = json.loads(response.data)
	# 	statuscode=response.status_code
	# 	self.assertEqual(statuscode,201)
	# 	self.assertEqual(response_data,{"error":"product unavailable"})
	# 	mock_update.assert_called_once()



if __name__ == "__main__":
	unittest.main()

