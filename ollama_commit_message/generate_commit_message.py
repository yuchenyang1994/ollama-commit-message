from ollama import Client
import subprocess
import os
import argparse


def get_staged_diff() -> str:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--no-color", "--text", "--diff-filter=AMCR"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error while getting staged diff: {e.stderr}")
        return ""


def get_staged_commit_message():
    git_dir = os.path.join(os.getcwd(), ".git")
    commit_msg_path = os.path.join(git_dir, "COMMIT_EDITMSG")

    try:
        with open(commit_msg_path, "r") as f:
            commit_message = f.read()
        return commit_message
    except FileNotFoundError:
        print("No staged commit message found.")
        return ""
    except Exception as e:
        print(f"Error reading commit message: {e}")
        raise e


def write_commit_message(commit_message):
    git_dir = os.path.join(os.getcwd(), ".git")
    commit_msg_path = os.path.join(git_dir, "COMMIT_EDITMSG")

    try:
        # 写入 commit message
        with open(commit_msg_path, "w") as f:
            f.write(commit_message)
        print("Commit message written successfully.")
    except Exception as e:
        print(f"Error writing commit message: {e}")
        raise e


def generate_commit_message(host: str, model: str):
    client = Client(host=host)
    diff_file = get_staged_diff()
    user_commit_message = get_staged_commit_message()
    prompt = f"""
    You are a good git commit message writer! commit messages based on the following diff:

    {diff_file}

    You need to write a git commit message based on the diff file.
    Output only the Git commit message. Do not output any other content.
    """
    resp = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{user_commit_message}"},
        ],
    )
    print("msg!!!", user_commit_message)
    msg = user_commit_message + " " + resp["message"]["content"].strip()
    write_commit_message(msg)


def main():
    parser = argparse.ArgumentParser(description="use ollama write git commit message")

    parser.add_argument(
        "--model", "-m", type=str, default="", help="ollama model name", required=True
    )
    parser.add_argument(
        "--host",
        type=str,
        default="http://localhost:11434",
        help="ollama host address",
    )

    parser.add_argument("filenames", nargs="*")

    args = parser.parse_args()

    generate_commit_message(args.host, args.model)


if __name__ == "__main__":
    main()
