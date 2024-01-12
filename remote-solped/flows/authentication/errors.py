import time


def detect_reload_loop(driver, url,reload_threshold=3, time_threshold=10):

    # Initialize variables for reload tracking
    reload_count = 0
    start_time = time.time()

    # Main loop
    while True:
        # Perform your desired actions on the webpage
        # ...

        # Check if the page has reloaded
        if time.time() - start_time < time_threshold:
            # Wait for a brief moment to allow the page to reload
            time.sleep(1)

            # Check if the current URL is the same as the previous URL
            if driver.current_url == url:
                reload_count += 1
            else:
                # Reset the reload count if the URL has changed
                reload_count = 0
                start_time = time.time()
        else:
            # If the time threshold is exceeded, break the loop
            break

        # Check if the reload count exceeds the threshold
        if reload_count >= reload_threshold:
            print("Webpage is in a reload loop.")
            break

    # Close the browser
    driver.quit()