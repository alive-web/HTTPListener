from fabric.api import put, run
from fabvenv import Venv

ROOT = "/opt/lv128/HTTPListener/"

def deploy():
    venv = Venv(ROOT, "requirements.txt")
    if not venv.exists():
        venv.create()
    venv.install()
    put("http_listener.py", ROOT)
    put("http_listener.service", ROOT)
    run("sudo mv %s/http_listener.service /etc/systemd/system/" % ROOT)
    run("sudo systemctl enable httplistener")
    run("sudo systemctl restart httplistener")
