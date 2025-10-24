# github_polaris_application_name
Get Application name for Polaris from GitHub custom properties.

This Action will set the found application name as an GitHub environment variable with key **POLARIS_APPLICATION_NAME**.

Custom property keys can be given as a comma separated list. The first matching property will be set as an application_name env. parameter, so the order of the keys will matter.

## Available Options
| Option name | Description | Default value | Environment variable | Required |
|-------------|-------------|---------------|----------|----------|
| github_url | GitHub Url, must be given if GH Enterprise in use | - | GH_SERVER_URL | false |
| github_token | GitHub Access Token | - | GH_ACCESS_TOKEN | true |
| github_custom_property_keys | Comma separated list of GH custom property keys where application name could be given | application_name,mac_id,portfolio | - | false |
| github_repo | GitHub repository name which custom properties will be checked | - | - | true |
| use_repository_name | true, will use repository name as an application name, if custom property is not found | false | - | false |

## Usage examples
This example is using Black Duck official GitHub Action [Black Duck Security Scan](https://github.com/marketplace/actions/black-duck-security-scan) to run the actual Polaris scan.
```yaml
    - name: Get Application name for Polaris
      uses: blackduck-community/github_polaris_application_name@v1
      with:
        github_token: ${{secrets.GITHUB_TOKEN}}
        github_repo: ${{github.repository}}
    - name: Nextgen Polaris Analysis with black-duck-security-scan
      uses: blackduck-inc/black-duck-security-scan@v2
      with:
          polaris_server_url: ${{secrets.NEXTGEN_POLARIS_SERVER_URL}}
          polaris_access_token: ${{secrets.NEXTGEN_POLARIS_ACCESS_TOKEN}}
          polaris_application_name: ${{ env.POLARIS_APPLICATION_NAME }} # After running synopsys-sig-community/github_polaris_application_name -action the polaris
          polaris_project_name: ${{github.repository}}                  # application name is set as an environment variable with key POLARIS_APPLICATION_NAME   
          polaris_branch_name: ${{github.ref_name}}
          polaris_assessment_types: "SAST"
          polaris_reports_sarif_create: true  
          polaris_reports_sarif_file_path: '${{github.workspace}}/polaris-scan-results.sarif.json'
          polaris_reports_sarif_severities: "CRITICAL,HIGH,MEDIUM,LOW"
          polaris_reports_sarif_issue_types: 'SAST' 
          polaris_upload_sarif_report: true 
          github_token: ${{secrets.GITHUB_TOKEN}}
```
