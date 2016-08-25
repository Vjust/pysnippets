"""
    Purpose : Sample implementation of Gnu PG in python
    Usage : python gpg_sample.py -h

"""
import gnupg
import os
import argparse


parser = argparse.ArgumentParser(
    description="This is a sample gpg decrypter ", version="1.0"
)


group = parser.add_mutually_exclusive_group()
group.add_argument('-d', action="store_false", dest="enc_switch",
                   help="For decryption")
group.add_argument('-e', action="store_true", dest="enc_switch",
                   help="For encryption")
parser.add_argument('-r', dest="recipient_id", help="gpg recipient (keyID)",
                    default="")
parser.add_argument('-if', dest="infile", help="input file")
parser.add_argument('-of', dest="outfile", help="output file")
cmdargs = parser.parse_args()


def do_pgp_encrypt(infile, outfile, recipient_id):
    home = os.path.join(os.path.expanduser('~'), '.gnupg')
    gpg = gnupg.GPG(homedir=home)
    with open(infile, "rb") as f1:
        status = gpg.encrypt(f1, recipient_id)
        if status.ok:
            with open(outfile, "w") as f2:
                f2.write(status.data)
        return status.ok
    return False


def do_pgp_decrypt(infile, outfile, passphrase):
    home = os.path.join(os.path.expanduser('~'), '.gnupg')
    gpg = gnupg.GPG(homedir=home)
    with open(infile, "rb") as f1:
        status = gpg.decrypt_file(f1, always_trust=False, passphrase=passphrase,
                                  output=outfile)
        return status.ok
    return False

if cmdargs.enc_switch:
    ret = do_pgp_encrypt(cmdargs.infile, cmdargs.outfile, cmdargs.recipient_id)
else:
    ret = do_pgp_decrypt(cmdargs.infile, cmdargs.outfile, os.environ.get("GPG_PASSPHRASE"))

# print "encsw {}  recepient {} infile {} outfile {} ".format(
# results.enc_switch, results.recipient_id or "Nne", results.infile, results.outfile)
