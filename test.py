import unittest
import requests

HOST = "https://wcg-apis.herokuapp.com"
DATABASE = HOST + "/citizen"

class ReservationTest(unittest.TestCase):
    """
    Class for unit testing the Registration API
    @author Siravit Ruethaiwat
    """

    def create(self,citizen_id, firstname, lastname, birthdate ,occupation, address):
        return {
            'citizen_id': citizen_id,
            'name': firstname,
            'surname': lastname,
            'birth_date': birthdate,
            'occupation': occupation,
            'address': address
        }

    def setUp(self):
        requests.delete(DATABASE, data = self.create("1329901000000", "Benedict", "Tan", "2000-09-09", "Scammer", "Sakhon"))
        self.users= self.create(citizen_id="1329901000000", firstname="Benedict", lastname="Tan", birthdate="2000-09-09", occupation="Scammer", address="Sakhon")

    def test_register(self):
        response = requests.post("https://wcg-apis.herokuapp.com/registration", data=self.users)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['feedback'],"registration success!")
    
    def test_invalid_id(self):
        response = requests.post("https://wcg-apis.herokuapp.com/registration",self.create("1", "Benedict", "Tan", "2000-09-09", "Scammer", "Sakhon"))
        self.assertEqual(response.json()['feedback'],"registration failed: invalid citizen ID")

    def test_missing_name(self):
        response = requests.post("https://wcg-apis.herokuapp.com/registration",self.create("1329901000000", "", "000", "2000-09-09", "Scammer", "Sakhon"))
        self.assertEqual(response.json()['feedback'],"registration failed: missing some attribute")

    def test_invalid_birthday(self):
        response = requests.post("https://wcg-apis.herokuapp.com/registration",self.create("1329901000000", "Benedict", "Tan", "2000", "Scammer", "Sakhon"))
        self.assertEqual(response.json()['feedback'],"registration failed: invalid birth date format")

    def test_duplicate_data(self):
        response = requests.post("https://wcg-apis.herokuapp.com/registration",self.create("1329901000000", "Benedict", "Tan", "2000-09-09", "Scammer", "Sakhon"))
        response2 = requests.post("https://wcg-apis.herokuapp.com/registration",self.create("1329901000000", "Benedict", "Tan", "2000-09-09", "Scammer", "Sakhon"))
        self.assertEqual(response.json()['feedback'],"registration success!")
        self.assertEqual(response2.json()['feedback'],"registration failed: this person already registered")

    def test_invalid_age(self):
        """age<13"""
        response = requests.post("https://wcg-apis.herokuapp.com/registration",self.create("1329901000000", "Benedict", "Tan", "2019-09-09", "Scammer", "Sakhon"))
        self.assertEqual(response.json()['feedback'],"registration failed: not archived minimum age")

if __name__ == '__main__':
    unittest.main()