from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from .models import Car, Model, Make, Review


class BaseAPITestCase(APITestCase):

    def setUp(self):
        makes = Make.objects.bulk_create([
            Make(title='BMW'),
        ])
        models = Model.objects.bulk_create([
            Model(make=makes[0], title='M3'),
            Model(make=makes[0], title='M4'),
            Model(make=makes[0], title='M5'),
            Model(make=makes[0], title='M6'),
        ])
        cars = Car.objects.bulk_create([
            Car(make=makes[0], model=models[0]),
            Car(make=makes[0], model=models[1]),
            Car(make=makes[0], model=models[2]),
            Car(make=makes[0], model=models[3]),
        ])

        # 4 reviews for M3
        # 5 reviews for M4
        # 1 review for M5
        # 2 reviews for M6
        Review.objects.bulk_create([
            Review(car=cars[0], rating=3),  # M3
            Review(car=cars[0], rating=3),  # M3
            Review(car=cars[0], rating=3),  # M3
            Review(car=cars[0], rating=3),  # M3
            Review(car=cars[1], rating=4),  # M4
            Review(car=cars[1], rating=5),  # M4
            Review(car=cars[1], rating=5),  # M4
            Review(car=cars[1], rating=4),  # M4
            Review(car=cars[1], rating=4),  # M4
            Review(car=cars[2], rating=5),  # M5
            Review(car=cars[3], rating=2),  # M6
            Review(car=cars[3], rating=2),  # M6
        ])


class CarAvgRatingCalculationTestCases(BaseAPITestCase):
    """ Test if car rating calculation functionality works correctly. """

    def test_avg_calculation(self):
        car_m4 = Car.objects.get(model__title='M4')
        car_m6 = Car.objects.get(model__title='M6')
        self.assertEqual(str(car_m4.avg_rating), '4.4')
        self.assertEqual(str(car_m6.avg_rating), '2.0')


class CarListAPITestCases(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.cars_url = reverse_lazy('cars')
        self.popular_cars_url = reverse_lazy('popular-cars')
        self.rate_url = reverse_lazy('rate')

    def test_cars_list(self):
        """ Test if cars API returns all 4 cars in the db """
        response = self.client.get(self.cars_url)
        self.assertEqual(len(response.data), 4)

    def test_cars_list_empty(self):
        """
            Test if cars list API doesn't crush if there's no car in the db.
        """
        Car.objects.all().delete()
        response = self.client.get(self.cars_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_popular_cars_list(self):
        """
            Test if popular car list API returns cars
            ordered by the number of rates.
        """
        response = self.client.get(self.popular_cars_url)

        # expected list of models
        expected_result = ['M4', 'M3', 'M6', 'M5']

        # actual list of models returned by the endpoint
        actual_result = [obj.get('model') for obj in response.data]

        self.assertEqual(expected_result, actual_result)
        self.assertEqual(response.data[0].get('rates_number'), 5)

    def test_popular_cars_list_empty(self):
        """
            Test if popular cars list API doesn't crush
            if there's no car in the db.
        """
        Car.objects.all().delete()
        response = self.client.get(self.popular_cars_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_create_car_invalid_make(self):
        data = {"make": "Testmake", "model": "Model 3"}
        response = self.client.post(self.cars_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('make')[0], 'No car found with given data'
        )

    def test_create_car_invalid_model(self):
        data = {"make": "Tesla", "model": "Model 33333"}
        response = self.client.post(self.cars_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('model')[0], 'No car found with given data'
        )

    def test_create_car_already_exists(self):
        data = {"make": "BMW", "model": "M3"}
        response = self.client.post(self.cars_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_create_car_successful(self):
        data = {"make": "Tesla", "model": "Model S"}
        response = self.client.post(self.cars_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_delete_car_invalid_id(self):
        """
            Test endpoint with non-existing car id.
        """
        delete_url = reverse_lazy('delete', kwargs={"id": 9999})
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data.get('error'), 'No car found with given ID'
        )

    def test_delete_car_successful(self):
        car = Car.objects.first()
        delete_url = reverse_lazy('delete', kwargs={'id': car.id})
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Car.objects.filter(id=car.id).exists())

    def test_rate_car_invalid_rating(self):
        car = Car.objects.first()
        response = self.client.post(
            self.rate_url, {"car_id": car.id, "rating": 6}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('rating')[0], 'Rating must be between 1 and 5'
        )

    def test_rate_car_invalid_rating_invalid_input_type(self):
        """
            If rating is not an integer,
            endpoint should return user-friendly error message.
        """
        car = Car.objects.first()
        response = self.client.post(
            self.rate_url, {"car_id": car.id, "rating": "test"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('rating')[0], 'A valid integer is required.'
        )

    def test_rate_car_invalid_car_id(self):
        """
            Test endpoint with non-existing car id.
        """
        response = self.client.post(
            self.rate_url, {"car_id": 9595, "rating": 3}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('car_id')[0], 'No car found with given ID'
        )

    def test_rate_car_invalid_car_id_invalid_input_type(self):
        """
            If car_id is not an integer,
            endpoint should return user-friendly error message.
        """
        response = self.client.post(
            self.rate_url, {"car_id": "hello world", "rating": 3}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('car_id')[0], 'A valid integer is required.'
        )

    def test_rate_car_successful(self):
        """
            Test endpoint with invalid rating score.
        """
        car = Car.objects.first()
        response = self.client.post(
            self.rate_url, {"car_id": car.id, "rating": 5}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('car_id'), car.id)
        self.assertEqual(response.data.get('rating'), 5)
