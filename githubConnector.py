import github
import argparse
import os

__version__ = "0.0.1"

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
        try:
            custom_properties = self.__get_all_custom_properties(repo)
            for app_key in self.app_keys:
                if app_key in custom_properties:
                    return custom_properties[app_key]
        except github.GithubException as e:
            print(e)
            return None
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


#Main for example how to run the script
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description="")
        parser.add_argument('--github_url', default=os.getenv('GH_SERVER_URL'), help='GitHub URL')
        parser.add_argument('--github_token', default=os.getenv('GH_ACCESS_TOKEN'), help='GitHub Access Token')
        parser.add_argument('--github_application_keys', help='GitHub custom property keys for application.', default="application_name,mac_id,portfolio" , required=False)
        parser.add_argument('--repository', help='Repository name which name you want to export', required=True)
        args = parser.parse_args()
        gitConnector = GitHubConnector(giturl=args.github_url, gittoken=args.github_token, application_keys=args.github_application_keys)
        appname = gitConnector.get_application_name(args.repository)
        print(appname)
    except Exception as e:
        print(e)
        exit(-1)
