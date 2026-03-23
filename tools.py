import os
import smtplib

import subprocess
import shutil
from email.mime.text import MIMEText

def create_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"{filename} created"

def verify_file(filename):
    return os.path.exists(filename)

# 📧 Email sender
def send_email(to_email, subject, message):
    try:
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()

        return "Email sent successfully"

    except Exception as e:
        return f"Email failed: {str(e)}"
    

import os
import requests

def create_github_repo(repo_name):
    try:
        token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Authorization": f"token {token}"
        }

        data = {
            "name": repo_name,
            "private": False
        }

        response = requests.post(
            "https://api.github.com/user/repos",
            json=data,
            headers=headers
        )

        if response.status_code == 201:
            return True, response.json()["clone_url"]
        elif response.status_code == 422:
            # Repo already exists
            username = os.getenv("GITHUB_USERNAME")
            url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
            print("Using GitHub:", username)
            return True, url
        else:
            return False, response.text

    except Exception as e:
        return False, str(e)


def push_to_github(project_folder, repo_name):
    try:
        original_dir = os.getcwd()
        success, repo_url = create_github_repo(repo_name)

        if not success:
            return f"Repo creation failed: {repo_url}"

        # Move into project folder
        os.chdir(project_folder)
        # before git init
        if os.path.exists(f"{project_folder}/.git"):
            shutil.rmtree(f"{project_folder}/.git")

        os.system("git init")
        os.system("git add .")
        os.system('git commit -m "Auto Agent Commit"')

        os.system(f"git remote add origin {repo_url}")
        os.system("git branch -M main")
        os.system("git push -u origin main")
        os.chdir(original_dir)
        

        return f"✅ Repo created & pushed: {repo_url}"

    except Exception as e:
        return f"GitHub push failed: {str(e)}"