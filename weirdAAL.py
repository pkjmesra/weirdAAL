# This file will help to serve as a starting point for using the rest of the tools
# Things we want to figure out
# 1) Is your key active?
# 2) If active, can you read monitoring configs, can you write?
# 3) Okay, you can read monitoring configs. We recommend things to avoid. Want to go further? Use write access to disable (if applicable)
# 4) Don't want to do anything with monitoring? That's fine, let's guide you through figuring out what your access looks like
# 5) Help with a printout of options from this point forward

import boto3
import argparse
import os
from botocore.exceptions import ClientError
from modules import *
import sys
import builtins

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.env'

# If you want to use a transparent + supports SSL proxy you can put it here
# os.environ['HTTPS_PROXY'] = 'https://127.0.0.1:3128'

sys.path.append("modules")
for module in all_modules:
    exec("from %s import *" % module)


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--module", help="list the module you would like to run", action="store", type=str, required=True)
parser.add_argument("-t", "--target", help="Give your target a name so we can track results", action="store", type=str, required=True)
parser.add_argument("-a", "--arguments", help="Provide a list of arguments, comma separated. Ex: arg1,arg2,arg3", action="store", type=str, required=False)
parser.add_argument("-l", "--list", help="list modules", action="store_true")
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
args = parser.parse_args()

# Provides us with a global var "db_name" we can access anywhere
builtins.db_name = "weirdAAL.db"

# Provides us with a global var "target" we can access anywhere
builtins.target = args.target

def perform_credential_check():
    '''
    Check that the AWS keys work before we go any further. It picks the keys up from the local .env file
    We are letting boto3 do all the work that way we can handle session tokens natively
    '''

    try:
        client = boto3.client("sts")
        account_id = client.get_caller_identity()["Account"]
    except botocore.exceptions.NoCredentialsError as e:
        print("Error: Unable to locate credentials")
        sys.exit("fix your credentials file -exiting...")
    except ClientError as e:
        print("The AWS Access Keys are not valid/active")
        sys.exit(1)

def method_create():
    try:
        arg = globals()["module_" + args.module]
        return arg
    except KeyError:
        print("That module does not exist")
        exit(1)


# Need to figure out if we have keys in the ENV or not
try:
    perform_credential_check()
except:
    print("Check the above error message and fix to use weirdAAL")
    sys.exit(1)

if (args.list):
    pass


# arg_list has to be defined otherwise will cause an exception
arg_list = None

if (args.arguments):
    arg_list = args.arguments.split(',')

# We need the user to tell us the module they want to proceed on
if (args.module):
    arg = method_create()
    if callable(arg):
        if arg_list:
            arg(arg_list)
        else:
            arg()


# Allow the user to specify verbosity for debugging
if (args.verbosity):
    print("Verbosity is enabled")
