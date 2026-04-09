
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestProductAPI:
    # 1. Test lấy danh sách (GET)
    def test_get_product_list(self, auth_client, product):
        url = reverse('product-list') 
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == product.name

    # 2. Test bảo mật (Chưa đăng nhập)
    def test_unauthenticated_get_list(self, api_client):
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code in [401, 403] 

    # 3. THÊM VÀO ĐÂY: Test tạo mới sản phẩm (POST)
    def test_create_product(self, auth_client):
        url = reverse('product-list')
        data = {
            "name": "Samsung S24",
            "sku": "SS24-001",
            "price": "900.00",
            "stock_qty": 5,
            "is_active": True
        }
        response = auth_client.post(url, data)
        assert response.status_code == 201  # 201 là Created
        assert response.data['sku'] == "SS24-001"