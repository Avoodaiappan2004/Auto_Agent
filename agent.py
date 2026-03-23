import json
import os
import re
from dotenv import load_dotenv
from groq import Groq
from blockchain import record_transaction, update_trust
from tools import push_to_github, create_file, verify_file, send_email

# Load env
load_dotenv()

# API setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Compute budget
MAX_CALLS = 10
api_calls = 0


# 🔥 AI call
def ask_ai(prompt):
    global api_calls

    if api_calls >= MAX_CALLS:
        return "Error: Compute budget exceeded"

    try:
        api_calls += 1

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

def create_project_folder(task):
    name = task.lower()
    name = re.sub(r"[^a-z0-9 ]", "", name)
    name = "_".join(name.split())[:30]

    base_dir = os.path.abspath("projects")  # ✅ absolute path

    folder = os.path.join(base_dir, name)

    os.makedirs(folder, exist_ok=True)

    return folder


def generate_repo_name(task):
    name = task.lower()
    name = re.sub(r"[^a-z0-9 ]", "", name)

    # remove unwanted words
    remove_words = ["create", "the", "and", "push to github"]
    for word in remove_words:
        name = name.replace(word, "")

    name = "-".join(name.split())
    return name[:30]


# 🔥 Extract clean code
def extract_code(text):
    code_blocks = re.findall(r"```(.*?)```", text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return text.strip()

def clean_code(code):
    if not code:
        return ""

    # remove backticks and junk
    code = code.replace("```html", "")
    code = code.replace("```css", "")
    code = code.replace("```javascript", "")
    code = code.replace("```", "")

    return code.strip()


# 📧 Detect email task
def detect_email_task(task):
    pattern = r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+"
    found = re.findall(pattern, task)
    if found:
        return True, found[0]
    return False, None


# 📧 Email agent
def email_agent(task):
    is_email, email = detect_email_task(task)

    if not is_email:
        return None

    content = ask_ai(f"""
    Extract only the email message from:
    {task}
    """)

    subject = "Message from Auto Agent"

    result = send_email(email, subject, content)

    return {
        "to": email,
        "message": content,
        "status": result
    }

def safety_check(task):
    dangerous = ["delete", "rm -rf", "shutdown", "format", "drop database"]
    
    for word in dangerous:
        if word in task.lower():
            return False, f"Blocked unsafe action: {word}"
    
    return True, "safe"

# 🔍 Detect GitHub trigger
def detect_github_task(task):
    keywords = ["github", "push", "deploy"]
    return any(word in task.lower() for word in keywords)


# 🤖 Planner
def planner_agent(task):
    return ask_ai(f"Break this task into steps:\n{task}")


# 🤖 Coder
def coder_agent(task, feedback=None):
    prompt = f"""
    You are an expert full-stack developer.

    Create a COMPLETE working web app for:
    {task}

    STRICT RULES:
    - Output ONLY 3 files: index.html, style.css, script.js
    - NO explanations
    - NO extra text
    - HTML must link CSS and JS properly
    - CSS must match HTML
    - JS must interact with HTML elements
    - NO broken or partial code

    {f"Previous error: {feedback}" if feedback else ""}

    OUTPUT FORMAT STRICTLY:

    ```html
    ...HTML CODE...
    ```

    ```css
    ...CSS CODE...
    ```

    ```javascript
    ...JS CODE...
    ```
    """

    response = ask_ai(prompt)

    html_match = re.search(r"```html(.*?)```", response, re.DOTALL)
    css_match = re.search(r"```css(.*?)```", response, re.DOTALL)
    js_match = re.search(r"```javascript(.*?)```", response, re.DOTALL)

    html = clean_code(html_match.group(1)) if html_match else ""
    css = clean_code(css_match.group(1)) if css_match else ""
    js = clean_code(js_match.group(1)) if js_match else ""

    return html, css, js


# 🤖 Verifier
def verifier_agent(html, css, js):
    errors = []

    if "<html" not in html.lower():
        errors.append("HTML missing structure")

    if "<link" not in html.lower():
        errors.append("CSS not linked")

    if "<script" not in html.lower():
        errors.append("JS not linked")

    if "{" not in css:
        errors.append("Invalid CSS")

    if not ("function" in js or "=>" in js or "addEventListener" in js):
        errors.append("JS not functional")

    if errors:
        return False, ", ".join(errors)

    return True, "Valid"


# 🚀 MAIN AGENT

def run_agent(task):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    global api_calls
    api_calls = 0

    logs = []

    # 1️⃣ Discover
    logs.append({"step": "discover", "task": task})

    # 🛑 Safety Guardrail
    safe, msg = safety_check(task)
    if not safe:
        return {"status": msg}

    # 📧 EMAIL FIRST
    email_result = email_agent(task)

    if email_result:
        logs.append({
            "step": "execute",
            "agent": "email_agent",
            "details": email_result
        })
    if email_result:
        trust_score = update_trust("success" in email_result["status"].lower())

        logs.append({
            "step": "trust_update",
            "score": trust_score
        })

        with open("agent_log.json", "w") as f:
            json.dump({"logs": logs}, f, indent=2)

        return {"task": task, "status": email_result["status"]}

    # 2️⃣ Plan
    plan = planner_agent(task)
    logs.append({"step": "plan", "output": plan})

    # 3️⃣ Execute with retry
    # 3️⃣ Execute with intelligent retry
    feedback = None

    for attempt in range(3):
        html, css, js = coder_agent(task, feedback)

        if not html or not css or not js:
            feedback = "Missing code in one or more files"
            continue

        valid, msg = verifier_agent(html, css, js)

        if valid:
            break

        feedback = msg

        logs.append({
            "step": "retry",
            "attempt": attempt + 1,
            "reason": msg
        })
    

    # Save files
    project_folder = create_project_folder(task)

    create_file(f"{project_folder}/index.html", html)
    create_file(f"{project_folder}/style.css", css)
    create_file(f"{project_folder}/script.js", js)

    logs.append({
        "step": "execute",
        "files": ["index.html", "style.css", "script.js"]
    })

    # 🔥 GitHub conditional push
    github_link = None

    if detect_github_task(task):
        repo_name = generate_repo_name(task)
        github_result = push_to_github(project_folder, repo_name)

        github_link = f"https://github.com/{os.getenv('GITHUB_USERNAME')}/{repo_name}"

        logs.append({
            "step": "tool_use",
            "tool": "github",
            "repo": repo_name,
            "folder": project_folder,
            "result": github_result
        })

    # 4️⃣ Verify files
    files_ok = all([
    verify_file(f"{project_folder}/index.html"),
    verify_file(f"{project_folder}/style.css"),
    verify_file(f"{project_folder}/script.js")
])

    logs.append({
        "step": "verify",
        "files_exist": files_ok
    })

    # 5️⃣ Submit
    create_file("final_output.txt", f"Task '{task}' completed")

    logs.append({
        "step": "submit",
        "status": "done"
    })

    # 🔢 Compute tracking
    logs.append({
        "step": "compute",
        "api_calls": api_calls,
        "limit": MAX_CALLS
    })
   

    # Save logs
    with open("agent_log.json", "w") as f:
        json.dump({"logs": logs}, f, indent=2)

    # Default status
    final_status = "success" if files_ok else "failed"

    if detect_github_task(task):
        if "failed" in github_result.lower():
            final_status = "github_failed"


    # 🔗 Blockchain logging
    record_transaction("task_completed", {
        "task": task,
        "status": final_status
    })

    # ⭐ Trust update (ALWAYS RUN)
    try:
        trust_score = update_trust(final_status == "success")
    except:
        trust_score = 0

    logs.append({
        "step": "trust_update",
        "score": trust_score
    })

    return {
    "task": task,
    "status": final_status,
    "github": github_link if github_link else "",
    "logs": logs  
}


# ▶️ RUN
if __name__ == "__main__":
    task = input("Enter your task: ")
    print(run_agent(task))