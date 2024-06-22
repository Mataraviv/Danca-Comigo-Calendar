# Studio Availability Checker

![Studio Availability Checker](./Current%20Logo.png)

Welcome to the Studio Availability Checker! This Streamlit web application helps you check the availability of our studio and book it for specific time slots.

## Features

- **Check Availability**: Select a date and time range to see if the studio is available.
- **Book Studio**: Book the studio by providing your email, booking request, and event description upon availability confirmation.
- **Upcoming Events**: Displays upcoming events in the studio calendar if it's unavailable for the selected time.

## How to Use:

### Installation

1. Clone the repository to your local machine:
   ```
   git clone <https://github.com/Mataraviv/Danca-Comigo-Calendar>
2. Install Python 3.11:

    You can download Python from [python.org](https://www.python.org/) and follow the installation instructions for your operating system.

3. Install dependencies:

    We recommend using Poetry for managing dependencies. If you don't have Poetry installed, you can install it using the instructions [here](https://python-poetry.org/docs/#installation).
    There is also a requirements.txt in the Repository

    ```
    poetry install
## Running the App

### Run the Streamlit app in your terminal:

   
    streamlit run main.py

### OR Run the Streamlit app in streamlit online using this [link](https://danca-comigo-calendar-akveqkdjv5kbhtms4dahxy.streamlit.app/)

## Usage

### Check Availability:

- Select a date using the date picker.
- Choose a start and end time for your studio session using the time inputs.
- Click on "Check Availability" to see if the studio is available for the selected time range.

### Book Studio:

- If the studio is available, you can proceed to book it by providing:
  - Your email address.
  - A summary of your booking request.
  - A detailed description of your event.
- Click on "Book Studio" to submit your booking request.

### View Upcoming Events:

- If the studio is unavailable, upcoming events during the selected time range will be displayed.
- You can view details such as event titles, dates, times, and durations.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
