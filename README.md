# ChatGPT

ChatGPT is a web application that implements a chatbot using OpenAI technology. The chatbot is trained to respond to user queries using the GPT-3.5 Turbo model. Additionally, the project features speech recognition functionality using the OpenAI API.

## Installation

1. Install the required libraries by running:
    ```
    pip install -r requirements.txt
    ```

2. Obtain your OpenAI API key and specify it in the `openai_api_key` variable in the `views.py` file.

3. Run migrations to create the database:
    ```
    python manage.py migrate
    ```

4. Start the server by running:
    ```
    python manage.py runserver
    ```

## Usage

Once the project is installed and running, you can:

- Register a new account or log in with an existing one.
- Interact with the chatbot by sending it queries through the web application interface.
- For text recognition, navigate to the `/whisper` page, upload an audio file, and receive its transcription.

## Contribution

If you'd like to contribute to the development of the project, you can:

- Propose improvements or new features by creating an issue.
- Create a pull request with fixes or enhancements.

## Authors

Project Author: [Dk]  

