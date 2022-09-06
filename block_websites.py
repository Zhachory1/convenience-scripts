# Block Websites
# must be run with sudo

from absl import app
from absl import flags
import platform
import os
import sys

FLAGS = flags.FLAGS
flags.DEFINE_list("block", [], "Comma separated list of websites to block.")
flags.DEFINE_list("unblock", [], "Comma separated list of websites to unblock.")

class Blocker:
    def __init__(self):
        self.platform = platform.system()
        if self.platform == 'Windows':
            self.host = "C:\Windows\System32\drivers\etc\hosts"
        elif self.platform == "Linux":
            self.host = "/etc/hosts"
        elif self.platform == "Darwin":
            self.host = "/etc/hosts"
        else:
            raise RuntimeError(f"This Platform ({self.platform}) is not supported")

    def block_websites(self, websites):
        with open(self.host, "a") as f:
            f.write("\n127.0.0.1 " + " ".join(websites))
            f.close()

    def unblock_websites(self, website):
        with open(self.host, "r") as f:
            lines = f.readlines()
            f.close()
        with open(self.host, "w") as f:
            for line in lines:
                if website not in line:
                    f.write(line)
            f.close()

def main(argv):
    if not FLAGS.block and not FLAGS.unblock:
        raise ValueError("Ensure one of the flags is filled.")
    blocker = Blocker()
    if FLAGS.block:
        blocker.block_websites(FLAGS.block)
        print("Added sites to block list")
    if FLAGS.unblock:
        for site in FLAGS.unblock:
            blocker.unblock_websites(site)
        print("Unblocked sites")

if __name__ == "__main__":
    app.run(main)