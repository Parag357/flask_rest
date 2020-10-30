from modules import app
import unittest
import json
from mock import patch
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from mock import Mock
from modules.tables import Category, Product


class InventoryTest(unittest.TestCase):

	@patch('modules.tables.Product.get_filtered_products')
	def test_get_success_with_all_values(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_get.return_value=[Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1),Product(name="prod2",price=5.0,expiry='03/01/2029',category_id=2)]

		mock_data = {
		"category_id":1,
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response.content_type,'application/json')
		mock_get.assert_called_once()

	@patch('modules.tables.Product.get_filtered_products')
	def test_get_success_with_id_and_sort(self,mock_get):
		url="/get"
		tester=app.test_client(self)
		mock_get.return_value=[Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1),Product(name="prod2",price=5.0,expiry='03/01/2029',category_id=2)]

		mock_data = {
		"category_id":1,
		"sort":"price"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response.content_type,'application/json')
		mock_get.assert_called_once()

	@patch('modules.tables.Product.get_filtered_products')
	def test_get_success_with_sort_and_order(self,mock_get):
		url="/get"
		tester=app.test_client(self)
		mock_get.return_value=[Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1),Product(name="prod2",price=5.0,expiry='03/01/2029',category_id=2)]

		mock_data = {
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response.content_type,'application/json')
		mock_get.assert_called_once()

	@patch('modules.tables.Product.get_filtered_products')	
	def test_get_success_with_id_only(self,mock_get):
		url="/get"
		tester=app.test_client(self)
		mock_get.return_value=[Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1),Product(name="prod2",price=5.0,expiry='03/01/2029',category_id=2)]

		mock_data = {
		"category_id":1
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response.content_type,'application/json')
		mock_get.assert_called_once()

	@patch('modules.tables.Product.get_filtered_products')
	def test_get_success_with_sort_only(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_get.return_value=[Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1),Product(name="prod2",price=5.0,expiry='03/01/2029',category_id=2)]

		mock_data = {
		"sort":"expiry"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response.content_type,'application/json')
		mock_get.assert_called_once()

	@patch('modules.tables.Product.get_filtered_products')
	def test_get_success_with_no_value(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_get.return_value=[Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1),Product(name="prod2",price=5.0,expiry='03/01/2029',category_id=2)]

		response=tester.get(url)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response.content_type,'application/json')
		mock_get.assert_called_once()

	@patch('modules.tables.Product.get_filtered_products')
	def test_get_no_data_with_unavailable_category(self,mock_get):
		url="/get"
		tester=app.test_client(self)

		mock_get.return_value=[]

		mock_data = {
		"category_id":20,
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,404)
		mock_get.assert_called_once()


	@patch('modules.tables.Product.delete')
	def test_delete_success_with_available_id(self,mock_delete):
		url="/delete/55"
		tester=app.test_client(self)
		response=tester.delete(url)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response_data,[{'msg': 'product is deleted'}])
		self.assertEqual(response.content_type,'application/json')
		mock_delete.assert_called_once_with(u'55') # u is for unicode 

	@patch('modules.tables.Product.delete')
	def test_delete_success_with_unavailable_id(self,mock_delete):
		url="/delete/5500"
		tester=app.test_client(self)
		response=tester.delete(url)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertEqual(response_data,[{'msg': 'product is deleted'}])
		self.assertEqual(response.content_type,'application/json')
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
		self.assertEqual(response.content_type,'application/json')
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
		self.assertEqual(response.content_type,'application/json')

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
		self.assertEqual(response.content_type,'application/json')

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
		self.assertEqual(response.content_type,'application/json')
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
		self.assertEqual(response.content_type,'application/json')
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
		self.assertEqual(response.content_type,'application/json')
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
		mock_create.side_effect = IntegrityError('violates unique constraint','mock','mock')
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,400)
		self.assertEqual(response.content_type,'application/json')
		mock_create.assert_called_once()

	@patch('modules.tables.Product.new')
	def test_create_failure_with_unavailable_category(self,mock_create):
		url="/create"
		tester=app.test_client(self)

		mock_data = {
		"name":"prod30",
		"price":15.0,
		"expiry":"09/09/2023",
		"category_id":111
		}
		mock_create.side_effect = IntegrityError('violates foreign key constraint','mock','mock')
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,404)
		self.assertEqual(response.content_type,'application/json')
		mock_create.assert_called_once()

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_success_with_name_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"name":"prod15"
		}
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_success_with_price_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"price":25
		}
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_failure_with_negative_price(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"price":-25.0
		}
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,400)
		self.assertEqual(response_data,{"error":"price must be > 0"})
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')


	@patch('modules.tables.Product.get_product_by_id')
	def test_update_success_with_expiry_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"expiry":"07/07/2023"
		}
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_success_with_category_only(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"category_id":1
		}
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg': 'product is updated'}])
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_success_with_all_values(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		mock_data={
		"name":"prod15",
		"price":07,
		"expiry":"07/07/2023",
		"category_id":1
		}
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,201)
		self.assertEqual(response_data,[{'msg':'product is updated'}])
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_with_no_values(self,mock_update):
		url="/update/79"
		tester=app.test_client(self)
		response=tester.post(url)
		mock_update.return_value=Product(name="prod1",price=15.0,expiry='03/01/2029',category_id=1)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,404)
		self.assertEqual(response_data,{'msg':'nothing to update'})
		self.assertEqual(response.content_type,'application/json')
		mock_update.assert_called_once_with(u'79')

	# @patch('modules.tables.Product.Query')
	# @patch('modules.tables.Product.save')
	# def test_update_failure_with_duplicate_name(self,mock_update_query,mock_update_save):
	# 	url="/update/79"
	# 	tester=app.test_client(self)
	# 	mock_data = {
	# 	"name":"prod1",
 # 	  	"price":15.0,
 # 	  	"expiry":"09/09/2023",
 # 	  	"category_id":2	
	# 	}
	# 	mock_update_save.side_effect = IntegrityError('violates unique constraint','mock','mock')
	# 	response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
	# 	statuscode=response.status_code
	# 	self.assertEqual(statuscode,404)
	# 	self.assertEqual(response.content_type,'application/json')
	# 	mock_update.assert_called_once()

	# @patch('modules.tables.Product.new')
	# def test_create_failure_with_unavailable_category(self,mock_update):
	# 	url="/update/79"
	# 	tester=app.test_client(self)

	# 	mock_data = {
	# 	"name":"prod30",
	# 	"price":15.0,
	# 	"expiry":"09/09/2023",
	# 	"category_id":111
	# 	}
	# 	mock_update.side_effect = IntegrityError('violates foreign key constraint','mock','mock')
	# 	response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
	# 	statuscode=response.status_code
	# 	self.assertEqual(statuscode,404)
	# 	self.assertEqual(response.content_type,'application/json')
	# 	mock_update.assert_called_once()

	@patch('modules.tables.Product.get_product_by_id')
	def test_update_with_wrong_id(self,mock_update):
		url="/update/790"
		tester=app.test_client(self)
		mock_update.return_value=[]
		mock_data={
		"name":"prod15",
		"price":07,
		"expiry":"07/07/2023",
		"category_id":1
		}
		response=tester.post(url,data=json.dumps(mock_data),content_type='application/json')
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,404)
		self.assertEqual(response_data,{"error":"product unavailable"})
		mock_update.assert_called_once_with(u'790')



if __name__ == "__main__":
	unittest.main()

