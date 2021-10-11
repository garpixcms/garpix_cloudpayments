import calendar
import datetime
import json

from django.urls import reverse

from garpix_cloudpayments.models import Payment
from garpix_cloudpayments.models.choices import (
    PAYMENT_STATUS_AUTHORIZED, PAYMENT_STATUS_COMPLETED, PAYMENT_STATUS_AWAITING_AUTHENTICATION)
from rest_framework import status
from rest_framework.test import APITestCase
from garpix_cloudpayments.tests.mock_order import EnumStatusOrder, MockOrder
from user.models import User


class CloudpaymentsTests(APITestCase):

    def setUp(self) -> None:
        user = User.objects.create_superuser('mmc_test', 'mmc_test@email.com', 'MmcTest123')
        self.client.force_authenticate(user=user)

    def test_pay_order(self):
        order = self.create_test_order()
        self.assertEqual(order.status, EnumStatusOrder.CONFIRMED.value)

        payment = self.get_payment(order)

        path = reverse('cloudpayments_pay')
        payload = {
            "InvoiceId": payment.order_number,
            "Amount": payment.price,
            "Status": PAYMENT_STATUS_AUTHORIZED
        }
        response = self.client.post(path, payload, format='json')

        response_content = json.loads(response.content.decode('utf8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Example: Check (get) DB order instance after CloudPayments processing again
        # # order = Order.objects.get(id=response_content.get('order_number'))

        # Simulate getting order from DB after CloudPayments processing again
        order.status = EnumStatusOrder.PAID_UP.value
        payment = Payment.objects.get(order_number=response_content.get('order_number'))

        self.assertEqual(order.status, EnumStatusOrder.PAID_UP.value)
        self.assertEqual(payment.status, PAYMENT_STATUS_COMPLETED)

    def test_confirm_order(self):
        # Simulate order payment. Example: order.paid() order.save()
        order = self.create_test_order()
        order.status = EnumStatusOrder.PAID_UP.value

        payment = self.get_payment(order)

        now = datetime.datetime.now()

        path = reverse('cloudpayments_confirm')
        payload = {
            "TransactionId": 'TrAnSaCtIoN',
            "InvoiceId": payment.order_number,
            "Amount": payment.price,
            "Status": PAYMENT_STATUS_COMPLETED,
            "Currency": 'RUB',
            "DateTime": now.now(),
            "CardFirstSix": '4111',
            "CardLastFour": '1111',
            "CartType": 'Visa',
            "CardExpDate": add_months(now.now(), 1),
            "TestMode": 1
        }
        response = self.client.post(path, payload,  format='json')

        response_content = json.loads(response.content.decode('utf8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payment = Payment.objects.get(order_number=response_content.get('order_number'))

        self.assertEqual(order.status, EnumStatusOrder.PAID_UP.value)
        self.assertEqual(payment.status, PAYMENT_STATUS_COMPLETED)

    def test_fail_order(self):
        order = self.create_test_order()
        payment = self.get_payment(order)

        path = reverse('cloudpayments_fail')
        payload = {
            "InvoiceId": payment.order_number,
            "Amount": payment.price,
            "Status": PAYMENT_STATUS_AWAITING_AUTHENTICATION
        }
        response = self.client.post(path, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_data(self):
        path = reverse('cloudpayments_payment_data')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_path(self):
        response = self.client.get('/cloudpayments/not_so_path/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @classmethod
    def get_payment(cls, order: MockOrder) -> Payment:
        return Payment.objects.get_or_create(order_number=order.pk, price=order.total_price, is_test=True)[0]

    @classmethod
    def create_test_order(cls):
        order = MockOrder()
        return order


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
