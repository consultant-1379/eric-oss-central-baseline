#!/usr/bin/python
from optparse import OptionParser

from common_functions import *

DEFAULT_APP_HELM_REPO = "https://arm.epk.ericsson.se/artifactory/proj-ec-son-drop-helm"
DEFAULT_ARMUSER = "ejenksonom"
DEFAULT_ARMTOKEN = "AKCp5aUQb5BsGtp2mFpCvHCXZ6aFKXXm9t3tBqKiarcRY36PSRZJxHYoHBpisLJAv1Tzb62k6"
DEFAULT_APP_NAME = "DEFAULT_APP_NAME"

if __name__ == '__main__':
    """
    Creates a OptionParser with all necessary options.
    """
    parser = OptionParser()
    parser.add_option("-w", "--workspace", dest="workspace",
                      help="Path to workspace [MANDATORY]")
    parser.add_option("--appChartDir", dest="appChartDir",
                      help="Relative path to application chart directory in git repository (--gitRepoRoot) [MANDATORY]")
    parser.add_option("--repoRoot", dest="gitRepoRoot",
                      help="Path to test-app chart directory [MANDATORY]")
    parser.add_option("--appHelmRepo", dest="appHelmRepo", default=DEFAULT_APP_HELM_REPO,
                      help="Path to test-app chart directory [OPTIONAL]")
    parser.add_option("--armUserName", dest="armUserName", default=DEFAULT_ARMUSER,
                      help="User name in ARM [OPTIONAL]")
    parser.add_option("--armUserToken", dest="armUserToken", default=DEFAULT_ARMTOKEN,
                      help="User token in ARM [OPTIONAL]")
    parser.add_option("--chartName", dest="chartName", default=DEFAULT_APP_NAME,
                      help="Chart name [OPTIONAL]")
    parser.add_option("-d", "--dryRun", action="store_true", default=False, dest="dryRun",
                      help="DryRun [OPTIONAL]")
    parser.add_option("--helm", dest="helmCommand",
                      help="Helm command [MANDATORY]")
    (options, args) = parser.parse_args()
    if not options.workspace:
        parser.print_help()
        exit_and_fail("The -w, --workspace parameter is not set")
    else:
        if not os.path.exists(options.workspace) or not os.path.isdir(options.workspace):
            exit_and_fail("Workspace directory %s does not exists" % options.workspace)
    if not options.appChartDir or not options.gitRepoRoot:
        parser.print_help()
        exit_and_fail("The --appChartDir or --gitRepoRoot parameter is not set. Both are mandatory")
    else:
        if not os.path.exists(options.gitRepoRoot) or not os.path.isdir(options.gitRepoRoot):
            exit_and_fail("repoRoot directory %s does not exists" % options.gitRepoRoot)
        if not os.path.exists(options.gitRepoRoot + "/" + options.appChartDir) or not os.path.isdir(
                options.gitRepoRoot + "/" + options.appChartDir):
            exit_and_fail("appChartDir directory %s/%s does not exists" % (options.gitRepoRoot, options.appChartDir))
    if not options.helmCommand:
        exit_and_fail("The --helm parameter is not set.")

    # Initialize variables
    appChartDir = options.gitRepoRoot + "/" + options.appChartDir
    chartYaml = "%s/Chart.yaml" % options.appChartDir;

    testAppChartYaml = "%s/%s" % (options.gitRepoRoot, chartYaml);

    # Read Chart.yaml
    chart = read_yaml(testAppChartYaml)

    # Create chart package
    chartPackageName = "%s-%s.tgz" % (chart["name"], chart["version"]);
    chartPackagePath = "%s/%s" % (options.workspace, chartPackageName);
    if os.path.exists(chartPackagePath):
        os.remove(chartPackagePath)

    # Create helm package
    run_cmd(options.workspace,
            "%s package --destination %s %s" % (options.helmCommand, options.workspace, appChartDir));

    # Upload new chart package to helm repository
    run_cmd(options.workspace, "curl -k -u %s:%s -X PUT \"%s/%s/%s\" -T %s" % (
        options.armUserName, options.armUserToken, options.appHelmRepo, options.chartName, chartPackageName,
        chartPackagePath), options.dryRun)
