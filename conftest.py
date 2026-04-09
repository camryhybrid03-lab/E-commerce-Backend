import pytest
from catalog.models import Product
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product(db):
    return Product.objects.create(
        name="iPhone 15",
        sku="IP15-001",
        price=1000.00,
        stock_qty=10,
        is_active=True
    )

@pytest.fixture
def auth_client(api_client, db):
    """Tạo client đã đăng nhập vì View của bạn yêu cầu IsAuthenticated"""
    from django.contrib.auth.models import User
    user = User.objects.create_user(username="testuser", password="password123")
    api_client.force_authenticate(user=user)
    return api_client