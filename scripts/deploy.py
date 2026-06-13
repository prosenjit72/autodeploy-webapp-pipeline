import subprocess
# Stop and remove old container
#subprocess.run(["docker","stop","taskmanager_container"])
#subprocess.run(["docker","rm","taskmanager_container"])
subprocess.run(["docker","rm","-f","taskmanager_new_container"])
# create new image
subprocess.run(["docker","build","-t","taskmanager-image","../app"])
# create container with define cpu and memory
subprocess.run([
    "docker","run","-d","-p","5000:5000",
    "--name","taskmanager_new_container",
    "--cpus","0.5","--memory","256m",
    "taskmanager-image"
])
# show status
subprocess.run(["docker","ps"])