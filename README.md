# DjangoGramm
DjangoGramm is a web application similar to Instagram, enabling users to post, share, and comment on each other’s content. It offers a convenient user interface, enhancing the enjoyment of connecting with others.

This app has the following features:

- Users can sign up, log in via third-party service (GitHub) or using application forms
- There is opportunity to create posts on different topics
- Users can subscribe\unsubscribe to other people
- Clients can like\dislike and comment on posts

The application has been covered by unittests

## Requirements
- Python 3.9
- Django 4.2

## Installing
1. Clone the repository:
   ```bash
   git clone https://github.com/AlexShv/DjangoGramm.git
   ```
2. Create and activate your virtual environment:
   - for Linux\macOS
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
    - for Windows
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
3. Install packages from requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application:
```bash
python manage.py runserver
```
