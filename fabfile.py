from fabric.api import put, run ,env
from fabvenv import Venv

ROOT = "/opt/lv128/HTTPListener/"
env.disable_known_hosts = True

def deploy():
    venv = Venv(ROOT, "requirements.txt")
    if not venv.exists():
        venv.create()
    venv.install()
    put("http_listener.py", ROOT)
    put("http_listener.service", ROOT)
    run("sudo mv %s/http_listener.service /etc/systemd/system/" % ROOT)
    run("sudo systemctl enable http_listener")
    run("sudo systemctl restart http_listener")
