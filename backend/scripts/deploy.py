import subprocess


def deploy():
    try:
        subprocess.check_call("gcloud app deploy", shell=True)
    except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
        try:
            print("return error code:", e.returncode)
        except Exception:
            pass


if __name__ == '__main__':
    deploy()
