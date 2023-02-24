## What is Open Assistant?

<p align="center">
    Open Assistant is a project meant to give everyone access to a great chat based large language model.
</p>

We believe that by doing this we will create a revolution in innovation in
language. In the same way that stable-diffusion helped the world make art and
images in new ways we hope Open Assistant can help improve the world by
improving language itself.

## Do you want to try it out?

### Contributing to Data Collection

The data collection frontend is now live [here](https://open-assistant.io/). Log
in and start taking on tasks! We want to collect a high volume of quality data.
By submitting, ranking, and labelling model prompts and responses you will be
directly helping to improve the capabilities of Open Assistant.

### Running Locally

**You do not need to run the project locally unless you are contributing to the
development process. The website link above will take you to the public website
where you can use the data collection app.**

If you would like to run the data collection app locally for development, you
can set up an entire stack needed to run **Open-Assistant**, including the
website, backend, and associated dependent services, with Docker.

To start the demo, run this in the root directory of the repository (check
[this FAQ](https://projects.laion.ai/Open-Assistant/docs/faq#docker-compose-instead-of-docker-compose)
if you have problems):

```sh
docker compose --profile ci up --build --attach-dependencies
```

Then, navigate to `http://localhost:3000` (It may take some time to boot up) and
interact with the website.

> **Note:** If an issue occurs with the build, please head to the
> [FAQ](https://projects.laion.ai/Open-Assistant/docs/faq) and check out the
> entries about Docker.

> **Note:** When logging in via email, navigate to `http://localhost:1080` to
> get the magic email login link.

> **Note:** If you would like to run this in a standardized development
> environment (a
> ["devcontainer"](https://code.visualstudio.com/docs/devcontainers/containers))
> using
> [vscode locally](https://code.visualstudio.com/docs/devcontainers/create-dev-container#_create-a-devcontainerjson-file)
> or in a web browser using
> [GitHub Codespaces](https://github.com/features/codespaces), you can use the
> provided [`.devcontainer`](.devcontainer/) folder.
