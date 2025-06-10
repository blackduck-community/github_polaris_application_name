'''
This Script will set found application name as GitHub environment variable with key POLARIS_APPLICATION_NAME.
Custom property keys can be given as a comma separated list. This script will print out
the first matching property, so the order of the keys will matter.

usage: githubConnector.py [-h] [--github_url GITHUB_URL] [--github_token GITHUB_TOKEN] [--github_application_keys GITHUB_APPLICATION_KEYS] --repository REPOSITORY

Environment parameters
----------------------
GH_SERVER_URL - GitHub Server URL. GitHub Server URL must be given if you are using GH Enterprise version. Otherwise, will use GitHub.com
GH_ACCESS_TOKEN - GitHub Access Token.

'''
import github
import argparse
import os

__version__ = "0.0.1"
__author__ = "Jouni Lehto"

class GitHubConnector:

    def __init__(self, giturl:str, gittoken:str, application_keys:str) -> None:
        self.app_keys = application_keys.split(",")
        if not gittoken:
            print("GitHub Access Token is not given. You need to give it with --gittoken")
            exit()
        self.token = gittoken
        auth = github.Auth.Token(token=gittoken)
        if giturl:
            # Github Enterprise with custom hostname
            self.giturl = giturl if not giturl.endswith("/") else giturl[:-1]
            self.github = github.Github(auth=auth, base_url=f"{giturl}/api/v3")
        else:
            # Public Web Github
            self.github = github.Github(auth=auth)

    def get_application_name(self, repo:str) -> str:
        '''
        Try to find application name from custom properties of the given repostitory.
        If use_repository_name = True, then if application name hasn't been solved with 
        custom properties, the given repository name is returned.
        :param repo: GitHub repository name
        '''
        try:
            application_name = None
            custom_properties = self.__get_all_custom_properties(repo)
            for app_key in self.app_keys:
                if app_key in custom_properties:
                    if custom_properties[app_key]:
                        application_name = custom_properties[app_key]
            if not application_name and args.use_repository_name:
                application_name = repo
            return application_name
        except github.GithubException as e:
            print(e)
            return None
    
    def __get_all_custom_properties(self, repo:str) -> dict:
        try:
            repo = self.github.get_repo(repo)
            custom_properties = repo.get_custom_properties()
            if custom_properties:
                return custom_properties
        except github.GithubException as e:
            print(e)
            return []
        return []

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

#Main for example how to run the script
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description="")
        parser.add_argument('--github_url', default=os.getenv('GH_SERVER_URL'), help='GitHub URL')
        parser.add_argument('--github_token', default=os.getenv('GH_ACCESS_TOKEN'), help='GitHub Access Token')
        parser.add_argument('--github_application_keys', help='GitHub custom property keys for application.', default="application_name,mac_id,portfolio" , required=False)
        parser.add_argument('--repository', help='Repository name which name you want to export', required=True)
        parser.add_argument('--use_repository_name', help="true, will use repository name as an application name, if custom property is not found", default=False, type=str2bool)
        args = parser.parse_args()
        gitConnector = GitHubConnector(giturl=args.github_url, gittoken=args.github_token, application_keys=args.github_application_keys)
        appname = gitConnector.get_application_name(args.repository)
        if appname:
            os.system(f"echo \"POLARIS_APPLICATION_NAME={appname}\" >> $GITHUB_ENV")
        else:
            print(f"Polaris application name not found for repository: {args.repository} with custom keys: {args.github_application_keys}")
            exit(-1)
    except Exception as e:
        print(e)
        exit(-1)
