#!/usr/bin/env python
"""This module downloads all of the charts requirements locally."""
import argparse
import logging

from common_functions import run_cmd, read_yaml

KI_URL="arm.rnd.ki.sw.ericsson.se"

LOG = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


def main():
    """This is the main function that does all of the work."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--appChartDir',
        help="""Full path to the application chart directory
        """,
        required=True
    )
    parser.add_argument(
        '--helmCommand',
        help="""The helm command to use
        """,
        required=True
    )
    parser.add_argument(
        '--dryRun',
        help="""Do a dry run of the commands
        """,
        action="store_true",
        required=False
    )
    parser.add_argument(
        "--armUserName",
        help="User name in ARM [OPTIONAL]",
        required=False
    )
    parser.add_argument(
        "--armUserToken",
        help="User token in ARM [OPTIONAL]",
        required=False
    )
    parser.add_argument(
        "--armSekiUser",
        help="User name in ARM [OPTIONAL]",
        required=False
    )
    parser.add_argument(
        "--armSekiToken",
        help="User token in ARM [OPTIONAL]",
        required=False
    )
    args = parser.parse_args()

    requirements_yaml_file = "%s/requirements.yaml" % args.appChartDir
    requirements = read_yaml(requirements_yaml_file)

    # Add dependency repos
    for dependency in requirements['dependencies']:
        LOG.info(dependency)
        reponame = dependency['repository'].split('/')[2]
        if reponame == KI_URL:
            run_cmd(args.appChartDir, "%s repo add %s %s --username %s --password %s" % (args.helmCommand, dependency['name'], dependency['repository'], args.armSekiUser, args.armSekiToken), args.dryRun)
        else:
            run_cmd(args.appChartDir, "%s repo add %s %s --username %s --password %s" % (args.helmCommand, dependency['name'], dependency['repository'], args.armUserName, args.armUserToken), args.dryRun)
    run_cmd(args.appChartDir, "%s dependency update %s" % (args.helmCommand, args.appChartDir), args.dryRun)


if __name__ == "__main__":
    main()