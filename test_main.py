import requests
import unittest
import pytest
import json


def sum(arg):
    total = 0
    for val in arg:
        total += val
    return total


class TestAuthentication(unittest.TestCase):
    baseUrl = "http://localhost:8000/apis"

    """ Test that it can delete all users """
    @pytest.mark.order(2)
    def test_delete_all_users(self):
        response = requests.delete(self.baseUrl + "/auth/")
        output = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200, "Should be OK")
        self.assertEqual(output['message'], "ok", "Should be OK")

    """ Test that it can sign up a user """
    @pytest.mark.order(3)
    def test_sign_up_user(self):
        signUpUserInput = {
            "email": "test@gmail.com",
            "password": "test",
            "name": "test",
            "uctId": "test001",
            "role": "Convener"
        }
        signUpResponse = requests.post(
            self.baseUrl + "/auth/sign-up", json=signUpUserInput)
        signUpOutput = json.loads(signUpResponse.content.decode("utf-8"))

        self.assertEqual(signUpResponse.status_code, 200, "Should be OK")
        self.assertEqual(signUpUserInput['email'],
                         signUpOutput['email'], "Should be OK")
        self.assertEqual(signUpUserInput['name'],
                         signUpOutput['name'], "Should be OK")
        self.assertEqual(signUpUserInput['role'],
                         signUpOutput['role'], "Should be OK")
        self.assertEqual(signUpUserInput['uctId'],
                         signUpOutput['uctId'], "Should be OK")

    """ Test that it can sign in a user """
    @pytest.mark.order(4)
    def test_sign_in_user(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        self.assertEqual(signInResponse.status_code, 200, "Should be OK")
        self.assertEqual(
            signInUserinput['email'], signInOutput['user']['email'], "Should be OK")

    """ Test that it thows error on invalid user data """
    @pytest.mark.order(5)
    def test_sign_in_using_invalid_credentials(self):
        signInUserinput = {
            "email": "testInvalid@gmail.com",
            "password": "testInvalid"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        self.assertEqual(signInResponse.status_code, 404, "Should be OK")
        self.assertEqual("User record doesn't exist",
                         signInOutput['detail'], "Should be OK")

    """ Test that it can get the currently logged in user """
    @pytest.mark.order(6)
    def test_get_current_logged_user(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        accessToken = signInOutput['token']

        getUserResponse = requests.get(
            self.baseUrl + "/auth/user", headers={'Authorization': 'Bearer ' + accessToken})
        getUserOutput = json.loads(getUserResponse.content.decode("utf-8"))

        self.assertEqual(getUserResponse.status_code, 200, "Should be 6")
        self.assertEqual(
            getUserOutput['id'], signInOutput['user']['id'], "Should be OK")
        self.assertEqual(
            getUserOutput['email'], signInOutput['user']['email'], "Should be OK")
        self.assertEqual(
            getUserOutput['name'], signInOutput['user']['name'], "Should be OK")
        self.assertEqual(
            getUserOutput['uctId'], signInOutput['user']['uctId'], "Should be OK")
        self.assertEqual(
            getUserOutput['role'], signInOutput['user']['role'], "Should be OK")


class TestEnquiries(unittest.TestCase):
    baseUrl = "http://localhost:8000/apis"

    """ Test that it can delete all enquiries """
    @pytest.mark.order(1)
    def test_delete_all_enquires(self):
        response = requests.delete(self.baseUrl + "/enquiries/")
        output = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200, "Should be OK")
        self.assertEqual(output['message'], "ok", "Should be OK")

    """ Test that it can create an enquiry """
    @pytest.mark.order(7)
    def test_create_enquiry(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        createEnqinput = {
            "userId": signInOutput['user']['id'],
            "type": "TestConcession",
            "courseCode": "CSC2001F",
            "testNo": "2"
        }
        createEnqResponse = requests.post(
            self.baseUrl + "/enquiry/", json=createEnqinput)
        createEnqOutput = json.loads(createEnqResponse.content.decode("utf-8"))

        self.assertEqual(createEnqResponse.status_code, 200, "Should be OK")
        self.assertEqual(createEnqinput['userId'],
                         createEnqOutput['userId'], "Should be OK")
        self.assertEqual(createEnqinput['type'],
                         createEnqOutput['type'], "Should be OK")
        self.assertEqual(
            createEnqinput['courseCode'], createEnqOutput['courseCode'], "Should be OK")
        self.assertEqual(createEnqinput['testNo'],
                         createEnqOutput['testNo'], "Should be OK")

    """ Test that it can delete an enquiry """
    @pytest.mark.order(8)
    def test_delete_enquiry(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        createEnqinput = {
            "userId": signInOutput['user']['id'],
            "type": "TestConcession",
            "courseCode": "CSC2001F",
            "testNo": "2"
        }
        createEnqResponse = requests.post(
            self.baseUrl + "/enquiry/", json=createEnqinput)
        createEnqOutput = json.loads(createEnqResponse.content.decode("utf-8"))

        deleteEnqResponse = requests.delete(
            self.baseUrl + "/enquiry/" + createEnqOutput['id'],)
        deleteEnqOutput = json.loads(deleteEnqResponse.content.decode("utf-8"))

        self.assertEqual(createEnqResponse.status_code, 200, "Should be OK")
        self.assertEqual(createEnqinput['userId'],
                         deleteEnqOutput['userId'], "Should be OK")
        self.assertEqual(createEnqinput['type'],
                         deleteEnqOutput['type'], "Should be OK")
        self.assertEqual(
            createEnqinput['courseCode'], deleteEnqOutput['courseCode'], "Should be OK")
        self.assertEqual(createEnqinput['testNo'],
                         deleteEnqOutput['testNo'], "Should be OK")

    """ Test that it can update an enquiry """
    @pytest.mark.order(9)
    def test_update_enquiry(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        createEnqinput = {
            "userId": signInOutput['user']['id'],
            "type": "AssignmentExtension",
            "courseCode": "CSC2001F",
            "assignmentNo": "2",
            "extensionDuration": "5"
        }
        createEnqResponse = requests.post(
            self.baseUrl + "/enquiry/", json=createEnqinput)
        createEnqOutput = json.loads(createEnqResponse.content.decode("utf-8"))

        updateEnqinput = {
            "extensionDuration": "8",
            "status": "Rejected"
        }
        updateEnqResponse = requests.put(
            self.baseUrl + "/enquiry/" + createEnqOutput['id'], json=updateEnqinput)
        updateEnqOutput = json.loads(updateEnqResponse.content.decode("utf-8"))

        self.assertEqual(updateEnqResponse.status_code, 200, "Should be OK")
        self.assertEqual(createEnqinput['userId'],
                         updateEnqOutput['userId'], "Should be OK")
        self.assertEqual(updateEnqinput['status'],
                         updateEnqOutput['status'], "Should be OK")
        self.assertEqual(updateEnqinput['extensionDuration'],
                         updateEnqOutput['extensionDuration'], "Should be OK")

    """ Test that it can upload file for an enquiry """
    @pytest.mark.order(10)
    def test_upload_file_for_enquiry(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        createEnqinput = {
            "userId": signInOutput['user']['id'],
            "type": "AssignmentExtension",
            "courseCode": "CSC2001F",
            "assignmentNo": "2",
            "extensionDuration": "5"
        }
        createEnqResponse = requests.post(
            self.baseUrl + "/enquiry/", json=createEnqinput)
        createEnqOutput = json.loads(createEnqResponse.content.decode("utf-8"))

        fileName ='file.txt'
        files = {'fileUpload': open(fileName, 'rb')}
        uploadFileResponse = requests.post(
            self.baseUrl + '/file/' + createEnqOutput['id'], files=files)
        uploadFileOutput = json.loads(
            uploadFileResponse.content.decode("utf-8"))

        uploadedFileName = str(uploadFileOutput['attatchmentLink']).split('/')[-1]

        self.assertEqual(uploadFileResponse.status_code, 200, "Should be OK")
        self.assertEqual(fileName, uploadedFileName, "Should be OK")

    """ Test that it can fetch all enquiries by user """
    @pytest.mark.order(11)
    def test_get_enquiries_by_user(self):
        signInUserinput = {
            "email": "test@gmail.com",
            "password": "test"
        }
        signInResponse = requests.post(
            self.baseUrl + "/auth/sign-in", json=signInUserinput)
        signInOutput = json.loads(signInResponse.content.decode("utf-8"))

        enquiriesByUserResponse = requests.get(
            self.baseUrl + "/enquiries/" + signInOutput['user']['id'])
        enquiriesByUserOutput = json.loads(
            enquiriesByUserResponse.content.decode("utf-8"))

        self.assertEqual(enquiriesByUserResponse.status_code,
                         200, "Should be OK")

        for enquiry in enquiriesByUserOutput:
            self.assertEqual(enquiry['user']['id'],
                             signInOutput['user']['id'], "Should be OK")


if __name__ == '__main__':
    unittest.main()
