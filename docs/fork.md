# Forking the Repository

1. Set up publishing.
    1. Create a [Docker Hub account](https://hub.docker.com/signup?next=%2F%3Fref%3Dlogin).
    1. Go to your [Security settings](https://hub.docker.com/settings/security).
    1. Click **New Access Token**.
    1. Enter an **Access Token Description**.
    1. Click **Create**.
    1. Note down your access token for later.
1. Set up CI/CD.
    1. Create a [GitLab](https://gitlab.com/users/sign_in#register-pane) account.
    1. [Connect](https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html) the GitHub repo to a GitLab repo.
    1. In the GitLab repo, create the following environment variables [via the UI](https://docs.gitlab.com/ee/ci/variables/#via-the-ui).
    
        |Key|Value|Masked|
        |---|---|---|
        |`DOCKER_HUB_USER`|Your Docker Hub username|No|
        |`DOCKER_HUB_PASSWORD`|The Docker Hub access token you noted down|Yes|