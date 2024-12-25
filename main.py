import time
from selenium.webdriver.common.by import By
import csv
from scrapper_ud import WebScraper
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import os


def main():
    """
    Main function to automate Instagram login and scrape follower data.

    The script logs into an Instagram account using credentials stored in environment variables,
    navigates to a specific profile, and retrieves follower data. The data is saved as a CSV file.

    Functions and Key Steps:
    - Uses the WebScraper class to interact with the web driver.
    - Automates login by sending username and password inputs.
    - Navigates to a specified Instagram profile.
    - Scrapes follower details, including name, username, and profile URL.
    - Saves the collected data into a CSV file.
    """
    driver = WebScraper()

    # Open Instagram login page
    driver.open_url('https://www.instagram.com')
    time.sleep(10)

    # Locate and input username
    userinput = driver.find_element_by(find_by="x_path", what_to_find="//input[@name='username']")
    time.sleep(5)
    userinput.send_keys(os.getenv('USER_NAME'))  # Username from environment variable

    # Locate and input password
    password = driver.find_element_by(find_by="x_path", what_to_find="//input[@name='password']")
    password.send_keys(os.getenv('PASSWORD'))  # Password from environment variable
    time.sleep(5)

    # Locate and click the login button
    login_button = driver.find_element_by(find_by="x_path",
                                          what_to_find="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/div/form/div[1]/div[3]/button")
    login_button.click()
    driver.execute_script(js="arguments[0].click();", element=login_button)
    time.sleep(5)

    # Handle "Not Now" prompt
    try:
        not_now = driver.find_element_by(find_by="x_path",
                                         what_to_find="/html/body/div[1]/section/main/div/div/div/div/button")
        time.sleep(5)
        not_now[0].click()
    except:
        pass

    # Open a new tab and navigate to the target profile
    driver.open_new_tab()
    time.sleep(10)
    driver.open_url(url="https://www.instagram.com/rizwan.ansari.183")

    # Retrieve the followers count and click to open the followers list
    followers = driver.find_element_by(find_by="x_path",
                                       what_to_find="/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span/span")
    nofollowers = followers.text.replace(" ", "")
    followers.click()
    time.sleep(10)

    # Initialize variables for scraping followers
    last_follower_link = ''
    counter = 0
    followers_list = []

    # Scroll and collect follower details
    while True:
        scr = driver.find_element_by(find_by="class_name", what_to_find="xyi19xy", multi=False)
        driver.scroll_by_height(scr)
        time.sleep(3)
        followers_find = scr.find_elements(By.CLASS_NAME, 'x1dm5mii')

        try:
            # Extract href from the last follower element
            anchor_element = followers_find[-1].find_element(By.CLASS_NAME, "x1i10hfl")
            href_value = anchor_element.get_attribute("href")

            if href_value == last_follower_link:
                if counter == 10:
                    break
                counter += 1

            last_follower_link = href_value
        except Exception as e:
            pass

    # Process follower data
    for follower in followers_find:
        anchor_element = follower.find_element(By.CLASS_NAME, "x1i10hfl")
        href_value = anchor_element.get_attribute("href")
        follower_name = follower.find_element(By.CSS_SELECTOR, "span.x1lliihq")
        user_name = follower.find_element(By.CSS_SELECTOR, "span._ap3a")

        followers_list.append({
            "name": follower_name.text,
            "user_name": user_name.text,
            "url": href_value
        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(followers_list)

    # Save the sorted DataFrame to a CSV file
    csv_file = "followers.csv"
    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    main()
