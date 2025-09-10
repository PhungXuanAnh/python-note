import traceback
import subprocess
import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException


import traceback
import subprocess
import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException


def _rename_existing_chrome_streams():
    """Renames all existing 'Google Chrome input' streams to a random name and returns their indices."""
    renamed_indices = []
    processes = []
    try:
        cmd_get_indices = "pacmd list-source-outputs | awk '/index:/{idx=$2} /application.name = \"Google Chrome input\"/{print idx}'"
        indices_result = subprocess.run(cmd_get_indices, shell=True, capture_output=True, text=True)
        indices = [idx for idx in indices_result.stdout.strip().split('\n') if idx]

        for index in indices:
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            new_name = f"Chrome_{random_suffix}"
            
            cmd_rename = f"""
            pacmd update-source-output-proplist {index} \\
                application.name="{new_name}" \\
                media.name="{new_name}" \\
                module-stream-restore.id="source-output-by-application-name:{new_name}"
            """
            p = subprocess.Popen(cmd_rename, shell=True)
            processes.append(p)
            print(f"Started renaming existing stream {index} to {new_name}")
            renamed_indices.append(index)

        for p in processes:
            p.wait() # Wait for each subprocess to finish

    except subprocess.CalledProcessError as e:
        print(f"Error renaming existing chrome streams: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while renaming streams: {e}")
        traceback.print_exc()
    return renamed_indices


def _rename_recording_stream(recording_stream_name, existing_indices):
    """Renames the last two created PulseAudio recording streams from Google Chrome."""
    if not recording_stream_name:
        return

    try:
        new_indices = []
        # Increased attempts to make it more robust
        for i in range(10):
            # Find all "Google Chrome input" streams
            cmd_get_index = "pacmd list-source-outputs | awk '/index:/{idx=$2} /application.name = \"Google Chrome input\"/{print idx}'"
            index_result = subprocess.run(cmd_get_index, shell=True, capture_output=True, text=True)
            all_chrome_indices = [idx for idx in index_result.stdout.strip().split('\n') if idx]
            
            # Filter out the ones that were already renamed
            candidate_indices = [idx for idx in all_chrome_indices if idx not in existing_indices]
            
            # Take the last two
            new_indices = candidate_indices[-2:]

            if len(new_indices) >= 2:
                break
            
            print(f"Attempt {i + 1} to find 2 new recording streams failed. Found {len(new_indices)}. Retrying...")
            time.sleep(0.5)

        if len(new_indices) >= 2:
            for index in new_indices:
                # Rename the stream using the found index, with the same name
                cmd_rename = f"""
                pacmd update-source-output-proplist {index} \\
                    application.name="{recording_stream_name}" \\
                    media.name="{recording_stream_name}" \\
                    module-stream-restore.id="source-output-by-application-name:{recording_stream_name}"
                """
                subprocess.run(cmd_rename, shell=True, check=True)
                print(f"Renamed recording stream {index} to {recording_stream_name}")
        else:
            # Updated the print message to reflect the number of attempts
            print(f"Could not find 2 new recording streams from 'Google Chrome input' after 10 attempts.")
    except subprocess.CalledProcessError as e:
        print(f"Error renaming recording stream: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()


def click_button_translate_by_voice(driver, recording_stream_name=None):
    buttons = driver.find_elements(By.XPATH, '//button[@aria-label="Translate by voice"]')
    
    clicked = False
    existing_indices = []
    if len(buttons) == 2:
        print("clicking button Translate by voice......")
        existing_indices = _rename_existing_chrome_streams()
        try:
            buttons[0].click()
            clicked = True
        except ElementNotInteractableException:
            buttons[1].click()
            clicked = True
        except ElementClickInterceptedException:
            buttons[1].click()
            clicked = True
        except NoSuchElementException:
            print("no button Translate by voice")
        except:
            traceback.print_exc()
    elif len(buttons) == 1:
        print("google translate is listening...")
        # Assuming this state means a stream is already active, so we don't click but might need to rename.
        # This part of the logic is ambiguous based on the original code.
        # For now, we do nothing, but if a rename is needed, we'd call it here.
        existing_indices = [] # No streams renamed on click
    else:
        return "button element has changed, please update xpath"

    if clicked:
        # Add a delay to give Chrome time to create the new audio streams
        print("Waiting for new recording streams to be created...")
        # time.sleep(1)
        _rename_recording_stream(recording_stream_name, existing_indices)
