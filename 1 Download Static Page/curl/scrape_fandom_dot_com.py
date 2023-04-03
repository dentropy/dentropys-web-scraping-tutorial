from subprocess import PIPE, Popen

command = "curl https://www.fandom.com/ > python_out.html"
with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
    output = process.communicate()[0].decode("utf-8")
    print(output)
