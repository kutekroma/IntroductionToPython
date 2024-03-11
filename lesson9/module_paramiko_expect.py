import paramiko
import logging
from paramiko_expect import SSHClientInteraction


logging.basicConfig(
    handlers=(logging.FileHandler("log.txt"), logging.StreamHandler()),
    format=u"%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)-15s %(message)s",
    level=logging.INFO,
)


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to the host
client.connect(hostname="0.0.0.0", username="eugene", password="1")

# Create a client interaction class which will interact with the host
with SSHClientInteraction(client, timeout=10, display=True) as interact:
    # interact = SSHClientInteraction(client, timeout=10, display=True)
    interact.expect("[~]")

    interact.send('sh')
    interact.expect("[$]")
    # Run the first command and capture the cleaned output, if you want the output
    # without cleaning, simply grab current_output instead.
    interact.send('uname -a')
    interact.expect("[~]")
    cmd_output_uname = interact.current_output_clean
    logging.info(cmd_output_uname)

    # Now let's do the same for the ls command but also set a timeout for this
    # specific expect (overriding the default timeout)
    interact.send('ls -l /')
    interact.expect("[~]", timeout=5)
    cmd_output_ls = interact.current_output_clean

if __name__ == '__main__':
    logging.info("Start")
    logging.info(cmd_output_ls)
