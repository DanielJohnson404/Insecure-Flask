# Vulnerable Flask App

This is a intentionally vulnerable Flask web application designed for educational purposes to demonstrate common web security flaws.

**WARNING:** DO NOT deploy this application in a production environment or expose it to the public internet. It contains critical security vulnerabilities.

## Vulnerabilities Included

1.  **SQL Injection**: The login page (`/login`) is vulnerable to SQL injection. Try `' OR '1'='1` as the username.
2.  **Cross-Site Scripting (XSS)**: The comments section on the index page is vulnerable to stored XSS. Try submitting `<script>alert(1)</script>`.
3.  **Hardcoded Secrets**: AWS keys and API tokens are hardcoded in `config.py`.
4.  **Missing Input Validation**: The file upload functionality (`/upload`) allows uploading any file type, including malicious scripts (e.g., .php, .py).
5.  **Insecure Deserialization**: The application unsafely unpickles the `prefs` cookie on the index page.
6.  **Path Traversal**: The file download endpoint (`/download?file=...`) allows accessing arbitrary files on the system (e.g., `../../etc/passwd` or `../../app.py`).
7.  **Authentication Bypass**: The admin panel (`/admin`) is accessible without authentication.
8.  **Weak Password Hashing**: Passwords are stored using MD5.
9.  **Command Injection**: The Network Tools on the dashboard (`/ping`) passes user input directly to the system shell. Try `127.0.0.1; ls`.
10. **IDOR (Insecure Direct Object Reference)**: The API endpoint `/api/message/1` allows viewing sensitive messages belonging to other users.
11. **XXE (XML External Entity)**: The endpoint `/xml/process_xml_unsafe` parses XML in a way that allows external entity expansion.

## Project Structure

- `run.py`: Entry point for the application.
- `config.py`: Main configuration (vulnerable).
- `app/`: Main application package.
    - `__init__.py`: App factory and blueprint registration.
    - `routes/`: Contains all route modules (auth, main, admin, files, network, api, xml).
    - `utils/`: Helper modules (db, cmd, config).

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    ```bash
    python run.py
    ```

3.  **Access the App**:
    Open your browser and navigate to `http://localhost:5000`.

## Quick Exploits

*   **Command Injection**: Go to `http://localhost:5000`, under "Network Tools" enter: `8.8.8.8; cat /etc/passwd` (or equivalent file on your OS).
*   **IDOR**: Login, then visit `http://localhost:5000/api/message/1`. You can see a message not addressed to you.
*   **XXE**: Send a POST request to `/xml/process_xml_unsafe` with an XXE payload.

## Disclaimer

This project is for educational purposes only. The author is not responsible for any misuse of this code.
