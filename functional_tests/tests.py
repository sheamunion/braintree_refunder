from selenium import webdriver
import os
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        # A Braintreep visits the refunder homepage
        self.browser.get("http://localhost:8000")

    def tearDown(self):
        self.browser.quit()

    def test_anonymous_user_can_start_a_refund(self):
        # They notice the title and header mention refunding Braintree transactions
        self.assertIn("Refund", self.browser.title)

        # They are invited to choose for which environment they need to refund txns: "Sandbox" or "Production".
        production_button = self.browser.find_element_by_id("id_environment_0")
        sandbox_button = self.browser.find_element_by_id("id_environment_1")

        assert production_button
        assert sandbox_button

        # They choose sandbox.
        sandbox_button.click()
        
        # After they click their environment, they are invited to enter API keys for this account in a textbox.
        merchant_id_input = self.browser.find_element_by_id("id_merchant_id")
        public_key_input = self.browser.find_element_by_id("id_public_key")
        private_key_input = self.browser.find_element_by_id("id_private_key")

        merchant_id = "dummy_merchant_id"
        public_key  = "dummy_public_key" 
        private_key = "dummy_private_key" 

        merchant_id_input.send_keys(merchant_id)
        public_key_input.send_keys(public_key)
        private_key_input.send_keys(private_key)

        # When they submit their API keys, they are prompted to upload a CSV. They upload a CSV. 
        file_upload = self.browser.find_element_by_id("id_source_csv")
        dummy_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_source.csv")
        file_upload.send_keys(dummy_file)

# TODO: They are prompted with a message: "We noticed you provided transaction ids and no optional amounts to refund. We"ll refund the full amount."

        # They click "Start refunding!" They are directed to a page with a status bar showing the progress of the refund job.
        self.browser.find_element_by_id("start_refund").click()
        refunding_url = self.browser.current_url
        status_page_text = self.browser.find_element_by_tag_name("body").text
        status_bar = self.browser.find_element_by_id("status")
        self.assertRegex(refunding_url, '/refunding')
        self.assertIn("Refunding transactions...", status_page_text)
        assert status_bar
        

# The refund job completes and the "treep is directed to a summary page. The "treep downloads a log file in CSV format. The "treep also sees a helpful summary of the results of the job including total txns refunded, total txns voided, number of failures.





# They click "Nope. Let me upload a new CSV with amounts." and are redirected to the previous step.

# They upload the correct CSV

