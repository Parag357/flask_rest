from modules import app
import unittest
import json
from mock import patch

class InventoryTest(unittest.TestCase):

	def test_get_success_with_all_values(self):
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

	def test_get_success_with_id_and_sort(self):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1,
		"sort":"price"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)

	def test_get_success_with_sort_and_order(self):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)

	def test_get_success_with_id_only(self):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":1
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)

	def test_get_success_with_sort_only(self):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"sort":"expiry"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,200)

	def test_get_success_with_no_value(self):
		url="/get"
		tester=app.test_client(self)

		response=tester.get(url)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)




	def test_get_failure(self):
		url="/get"
		tester=app.test_client(self)

		mock_data = {
		"category_id":20,
		"sort":"price",
		"order":"desc"
		}

		response=tester.get(url,data=json.dumps(mock_data),content_type='application/json')
		statuscode=response.status_code
		self.assertEqual(statuscode,404)


	@patch('modules.endpoints.delete')
	def test_delete_success(self,mock_delete):
		mock_delete.return_value={"msg":"product is deleted"}
		url="/delete/75"
		tester=app.test_client(self)

		response=tester.delete(url)
		response_data = json.loads(response.data)
		statuscode=response.status_code
		self.assertEqual(statuscode,200)
		self.assertTrue(response.data,b'product is deletedhghv')
		

	# def test_create(self):
 # 		url="/create"
 # 		tester=app.test_client(self)
 # 		app.config['TESTING'] = True
 # 		mock_data = {
 # 		"name":"prod1",
 # 		"category_id":1,
 # 		"sort":"price",
 # 		"order":"desc"
 # 		}

 # 		response=tester.get(url,data=jsonify(mock_data),content_type='application/json')
 # 		statuscode=response.status_code
 # 		self.assertEqual(statuscode,200)
if __name__ == "__main__":
	unittest.main()

