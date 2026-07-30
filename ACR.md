#azure 
Azure Container Registry is a managed, private Docker registry service that stores and distributes container images and related artifacts.

ACR supports Basic, Standard, and Premium service tiers.

ACR uses a **three-level hierarchy** to organize content.
### Registry

The registry is the top-level resource that hosts all container content. Each registry has a unique login server URL in the format `<registry-name>.azurecr.io`. When you create a registry, you choose a name that becomes part of this URL.

A registry contains multiple repositories and provides authentication, access control, and management capabilities. You can configure who has access to push and pull images, set retention policies, and enable features like geo-replication at the registry level.
### Repository

A repository is a collection of container images with the same name but different tags.
Repositories support namespaces using forward slashes for organization. This feature lets you group related images logically:

- `production/inference-api` for production-ready images
- `staging/inference-api` for images under validation
- `ml-team/model-server` for team-specific images

Namespaces help with access control. You can grant a team permission to push images only to their namespace while restricting access to production images.
### Artifact

An artifact is the actual container image or other content stored in a repository. Each artifact has tags that identify it, layers that make up its content, and a manifest that describes its structure. Artifacts can include Docker images, Helm charts, or any OCI-compliant content.
	#### Tags
		Tags identify specific versions of an artifact within a repository. The format `repository:tag` provides a human-readable reference.
		A single artifact can have multiple tags pointing to it. You might tag an image as both `inference-api:v1.2.0` and `inference-api:stable` to indicate it's the current stable release. Both tags reference the same underlying image.
		Tags are mutable. When you push a new image with an existing tag, the tag moves to point to the new image.
	#### Layers
		Container images consist of one or more layers. Each layer corresponds to an instruction in the Dockerfile that modifies the filesystem.  For example, installing a package or copying files creates a new layer. Layers are content-addressable, meaning you can identify them by a hash of their content.
		ACR shares common layers across images, reducing storage costs and speeding up pulls. When multiple images share a base layer such as `python:3.11`, only one copy exists in the registry. This deduplication is valuable for AI applications where many images might share common ML framework layers.
	#### Manifests
		Every artifact has a manifest that lists its layers and configuration. The manifest is identified by a SHA-256 digest in the format `sha256:abc123...`. Unlike tags, digests are immutable. Once an image is pushed, its digest never changes.
		Pulling by digest guarantees you get the exact image you expect, even if someone pushes a new image with the same tag. This immutability is critical for production AI deployments where you need consistency across all nodes.
	
## Address artifacts for push and pull operations
	ACR supports two addressing formats for pushing and pulling images. Each approach has different use cases.
	### By tag
		Tag-based addressing uses the format `registry/repository:tag`. This approach provides human-readable references that are easy to remember and use in deployment configurations.
		Azure CLI
			Pull an image by tag
			docker pull myregistry.azurecr.io/inference-api:v1.2.0
			Push an image with a tag
			docker push myregistry.azurecr.io/inference-api:v1.2.0
		Tag-based addressing works well during development and for images where you want to receive automatic updates. However, tags can change, so deployments using tags might not be perfectly reproducible.
	### By digest
		Digest-based addressing uses the format `registry/repository@sha256:hash`. This approach guarantees you reference a specific, immutable image regardless of tag changes.
		Azure CLI
			# Pull an image by digest
			docker pull myregistry.azurecr.io/inference-api@sha256:0a2e01852872580b2c2fea9380ff8d7b637d3928783c55beb3f21a6e58d5d108
		Pull by digest when you need guaranteed reproducibility. Production deployments where consistency across nodes is critical should use digests. You can find an image's digest in the Azure portal, through the Azure CLI, or in the output when pushing an image.

## Best practices for organizing registries

Following these practices helps you maintain an organized and efficient registry:

- **Use namespaces:** Organize repositories by team, environment, or project using forward-slash notation. This structure simplifies access control and makes it easier to find related images.
- **Plan repository structure:** Group related images logically. Consider whether images belong together based on deployment patterns, team ownership, or lifecycle management needs.
- **Enable geo-replication:** For global AI deployments, replicate images to regions where your services run. This reduces pull latency and improves deployment reliability.
- **Monitor storage:** Track storage consumption and implement retention policies to remove untagged manifests. Container images accumulate over time, and cleanup policies prevent unnecessary storage costs.

## Additional resources

- [About registries, repositories, and artifacts](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-concepts)
- [Azure Container Registry service tiers](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-skus)
- [Best practices for Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-best-practices)

## Build and run images with ACR Tasks
	ACR Tasks provide cloud-based container image building without requiring a local Docker installation. This capability addresses common challenges for AI development teams, including inconsistent builds across developer machines and the need for automated continuous integration. 
	

## ACR Tasks

ACR Tasks is a suite of features that offload container image builds to Azure. Instead of building images locally and pushing them to the registry, you send your source code to Azure Container Registry and let the cloud handle the build process. This approach provides several benefits for AI application development:

- **Consistent builds:** Eliminate "works on my machine" problems by building in a controlled cloud environment. Every build uses the same infrastructure regardless of which developer initiates it.
- **No local Docker required:** Build images from source code without installing Docker on developer workstations. This simplifies development setup and enables builds from environments where Docker isn't available.
- **CI/CD integration:** Trigger builds automatically from source code commits or base image updates. ACR Tasks integrates with GitHub and Azure DevOps for automated pipelines.
- **Multi-platform support:** Build images for Linux and Windows, including ARM processor architectures (such as ARM64) for edge AI deployments. ACR handles cross-platform builds without requiring you to maintain different build environments.


## ACR Tasks supports three main scenarios: 
quick tasks for on-demand builds, automatically triggered tasks for continuous integration, and multi-step tasks for complex workflows.
## Quick tasks for on-demand builds

Quick tasks provide the fastest way to build and push a single container image. The `az acr build` command sends your source code context to ACR, builds the image in the cloud, and pushes it to your registry. The process mirrors running `docker build` followed by `docker push`, but everything happens in Azure.

The following command builds an image from a local Dockerfile and pushes it to the registry:

Azure CLI

```
az acr build --registry myregistry --image inference-api:v1.0.0 .
```

The command accepts a build context, which is the location of your source files. ACR uploads the context, runs the Docker build using your Dockerfile, and pushes the resulting image. The period (`.`) at the end specifies the current directory as the build context.

#### Context locations

The build context determines where ACR retrieves your source files. Choosing the right context location affects your workflow efficiency and integration with existing tools. ACR Tasks accepts build contexts from multiple locations:

- **Local directory:** Files on your local file system. ACR compresses and uploads the directory contents.
- **Git repository:** Public or private GitHub or Azure DevOps repositories. Specify the repository URL directly.
- **Remote tarball:** Compressed archives on a remote web server accessible via URL.

Building from a Git repository enables builds without cloning the repository locally:

Azure CLI

```
az acr build --registry myregistry \
  --image inference-api:v1.0.0 \
  https://github.com/myorg/inference-api.git
```

#### When to use quick tasks

Quick tasks work best when you need immediate, one-time builds without setting up persistent automation. They bridge the gap between local development and full CI/CD pipelines. Quick tasks are ideal for:

- Validating Dockerfile changes before committing to source control
- Building images during development without installing Docker locally
- One-off builds in CI/CD pipelines where you need a simple build step
- Testing new base images or dependency updates

## Automatically triggered tasks

ACR Tasks support automatic triggers that rebuild images when conditions change. These triggers enable continuous integration workflows where images stay current without manual intervention.

### Source code triggers

Source code triggers initiate builds when code is committed or pull requests are created in GitHub or Azure DevOps. ACR creates a webhook in your repository that fires on commits, automatically starting a build.

The following command creates a task that triggers on commits to the main branch:

Azure CLI

```
az acr task create \
  --registry myregistry \
  --name build-inference-api \
  --image inference-api:{{.Run.ID}} \
  --context https://github.com/myorg/inference-api.git#main \
  --file Dockerfile \
  --git-access-token $PAT
```

The `{{.Run.ID}}` syntax creates a unique tag for each build using the ACR task run identifier. This ensures each triggered build produces a distinctly tagged image.

The personal access token (PAT) grants ACR permission to access your repository and create webhooks. Store tokens securely using Azure Key Vault rather than hardcoding them in scripts.

### Base image triggers

Base image triggers automatically rebuild application images when their base image updates. This capability is critical for AI applications that depend on base images containing ML frameworks, CUDA drivers, or other runtime components.

When you update a base image like `python:3.11` or a custom PyTorch image in your registry, ACR detects the change and rebuilds all images that specify that base image in their Dockerfile `FROM` statement. This automation ensures your application images receive security patches and updates from base images without manual intervention.

Base image triggers work for base images stored in the same ACR registry or in Docker Hub and other public registries. For private base images, both the base and application images should be in the same registry for automatic trigger detection.

### Scheduled triggers

Scheduled triggers run tasks on a defined schedule using cron expressions. Use scheduled triggers for:

- Nightly builds that incorporate the latest dependencies
- Periodic rebuilds to pick up base image patches even when detection doesn't trigger automatically
- Regular security scans of images
- Cleanup tasks that remove old untagged images

The following command creates a task that runs daily at midnight UTC:

Azure CLI

```
az acr task create \
  --registry myregistry \
  --name nightly-build \
  --image inference-api:nightly \
  --context https://github.com/myorg/inference-api.git \
  --schedule "0 0 * * *" \
  --file Dockerfile \
  --git-access-token $PAT
```

## Multi-step tasks

Multi-step tasks extend quick tasks with sequential workflows defined in YAML. Each step can build images, run containers, or execute commands, with dependencies between steps. This capability enables build-test-push workflows entirely within ACR.

A multi-step task uses a YAML file that defines the workflow:

YAML

```
version: v1.1.0
steps:
  - build: -t {{.Run.Registry}}/inference-api:{{.Run.ID}} .
  - push:
    - {{.Run.Registry}}/inference-api:{{.Run.ID}}
  - cmd: {{.Run.Registry}}/inference-api:{{.Run.ID}} python -m pytest tests/
```

This task builds the image, pushes it to the registry, then runs the container to execute tests. If the tests fail, you know before the image is used in deployment.

Multi-step tasks support:

- Build and test workflows that validate images before pushing
- Sequential operations with dependencies between steps
- Parallel execution of independent steps
- Conditional logic based on previous step results

Create the task from your YAML file:

Azure CLI

```
az acr task create \
  --registry myregistry \
  --name build-test-push \
  --context https://github.com/myorg/inference-api.git \
  --file acr-task.yaml \
  --git-access-token $PAT
```

## Run a container image for testing

ACR Tasks can run a built image to validate it works correctly. This capability helps catch configuration issues before deployment. The `az acr run` command executes a command in a container using an image from your registry.

Azure CLI

```
az acr run --registry myregistry \
  --cmd 'inference-api:v1.0.0 python --version' \
  /dev/null
```

The `/dev/null` context indicates no source files are needed since you're running an existing image. Use this approach to:

- Verify an image starts correctly
- Check that required tools and frameworks are available
- Run smoke tests against the container
- Execute health check commands

## Best practices for ACR Tasks

Follow these practices to get the most from ACR Tasks:

- **Use run variables:** Incorporate `{{.Run.ID}}` or `{{.Run.Date}}` in tags for unique, traceable builds. These variables create distinct tags that link images to specific task runs.
- **Secure access tokens:** Store personal access tokens for Git triggers in Azure Key Vault. Avoid committing tokens to repositories or including them in scripts.
- **Monitor task logs:** Review task output to diagnose build failures using `az acr task logs`. Logs show the complete build process including any errors.
- **Optimize build context:** Use `.dockerignore` to exclude unnecessary files from the context upload. Large contexts slow down builds and consume bandwidth.
- **Layer caching:** ACR Tasks cache layers between builds. Order Dockerfile instructions to maximize cache hits by placing frequently changing instructions late in the file.

## Additional resources

- [ACR Tasks overview](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tasks-overview)
- [Build and deploy container images with ACR Tasks](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tutorial-quick-task)
- [Run multi-step build, test, and patch tasks](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tasks-multi-step)

# Tag and version images

The tagging strategy you choose affects deployment reliability, rollback capabilities, and image maintenance. This unit covers tagging approaches, versioning schemes, and lifecycle management practices that support production AI deployments.

## Understand tagging strategies

Tags provide human-readable references to container images. The choice between stable and unique tags determines how deployments behave when images update and whether you can reliably roll back to previous versions.

### Stable tags

Stable tags like `v1`, `v1.2`, or `latest` are reused across multiple image pushes. When you push a new image with an existing tag, the tag moves to point to the new image. The previous image remains in the registry but loses that tag reference.

Stable tags work well in specific scenarios:

- **Base images receiving security updates:** When you patch a base image and want dependent builds to pick up changes automatically
- **Development environments:** When you want the latest changes without updating deployment configurations
- **Continuous delivery:** When consumers should always receive the most current version

The tradeoff with stable tags is predictability. Different nodes might pull the same tag at different times and receive different images. For AI applications serving inference requests, this inconsistency can cause unexpected behavior when nodes run different model versions.

### Unique tags

Unique tags like `v1.2.0-build456` or `20260102-abc123` are never reused. Each image push creates a new tag, preserving all previous versions in the registry.

Unique tags work well for:

- **Production deployments:** Every node in your cluster pulls the exact same image
- **Audit trails:** You can trace exactly which image was deployed at any point in time
- **Rollback scenarios:** Reference any previous build to restore a known-good state
- **Compliance requirements:** Demonstrate which specific image version was running during an incident

The tradeoff is that unique tags require updating deployment configurations when you release new versions. This explicit update process is considered a benefit for production environments where changes should be intentional.

## Implement semantic versioning

Semantic versioning uses the `MAJOR.MINOR.PATCH` format to communicate the nature of changes to image consumers. This convention provides a clear contract about compatibility.

- **MAJOR:** Increment for breaking changes that require consumer updates, such as API changes or removed features
- **MINOR:** Increment for new features that are backward compatible
- **PATCH:** Increment for bug fixes and security patches that don't change the API

For an AI inference API, version tags might follow this progression:

text

```
inference-api:1.0.0    # Initial release
inference-api:1.0.1    # Bug fix in preprocessing
inference-api:1.1.0    # Added new model endpoint
inference-api:2.0.0    # Breaking API change
```

Combine semantic versions with stable tags for flexibility. The following approach lets consumers choose their update strategy:

text

```
inference-api:1        # Points to latest 1.x.x (stable tag)
inference-api:1.1      # Points to latest 1.1.x (stable tag)
inference-api:1.1.0    # Specific patch version (unique tag)
```

Consumers who reference `inference-api:1` receive automatic updates within the major version. Those referencing `inference-api:1.1.0` receive only the specific patch version they specify.

## Generate unique tags for deployments

Production deployments benefit from unique tags that guarantee consistency. Several patterns provide traceability to your build and source code.

### Build ID tags

Build IDs from your CI/CD system create a direct link between container images and the pipeline runs that produced them. When you need to investigate an issue or audit a deployment, the build ID points you to the exact pipeline execution with its logs, test results, and artifacts. Use your CI/CD system's build identifier to link images to specific pipeline runs.

text

```
inference-api:build-4567
```

### Git commit SHA tags

Git commit hashes provide the most direct connection between a container image and its source code. Unlike build IDs that require access to your CI/CD system, anyone with repository access can look up the exact code state that produced the image. Tag with the short or full Git commit hash to link the image directly to source code.

text

```
inference-api:abc123f
```

### Timestamp tags

Timestamps provide immediate visual context about image age without requiring lookups in external systems. When reviewing a list of images, you can quickly identify the build sequence and spot outdated versions. Include the build date and time for chronological ordering.

text

```
inference-api:20260102-143022
```

### Combined approach

For production systems where traceability is critical, combining multiple identifiers in a single tag provides comprehensive information at a glance. This approach is valuable during incident response when you need to quickly determine the semantic version, locate the build pipeline, and find the source code. Combine multiple identifiers for maximum traceability.

text

```
inference-api:v1.2.0-build4567-abc123f
```

When using ACR Tasks, the `{{.Run.ID}}` variable automatically generates unique identifiers for each build:

Azure CLI

```
az acr build --registry myregistry \
  --image inference-api:v1.2.0-{{.Run.ID}} .
```

## Manage the latest tag

The `latest` tag has special behavior in Docker. When you push or pull without specifying a tag, Docker uses `latest` by default. This convenience can cause problems in production environments.

Consider these issues with `latest`:

- **Inconsistent deployments:** Different nodes might pull `latest` at different times and receive different images
- **Unpredictable updates:** Deployments change when someone pushes a new image, even without intentional deployment
- **Difficult troubleshooting:** When investigating issues, you don't know which version is running

For production deployments, specify explicit tags in Kubernetes manifests and deployment configurations:

YAML

```
# Avoid this in production
image: myregistry.azurecr.io/inference-api:latest

# Use explicit versions instead
image: myregistry.azurecr.io/inference-api:v1.2.0
```

If your workflow requires `latest`, consider using it only in development environments where the convenience outweighs the consistency concerns.

## Lock deployed images

ACR allows you to lock images to prevent accidental deletion or modification. Locking is a best practice for production images actively serving traffic.

The following command locks an image by disabling write operations:

Azure CLI

```
az acr repository update \
  --name myregistry \
  --image inference-api:v1.2.0 \
  --write-enabled false
```

Locked images have these characteristics:

- **Cannot be deleted:** Even administrators can't accidentally remove them
- **Cannot be overwritten:** Pushing a new image with the same tag fails
- **Survive retention policies:** Automatic cleanup rules don't remove locked images
- **Provide deployment assurance:** Production workloads remain stable because the image stays available

Unlock an image when you're ready to retire it:

Azure CLI

```
az acr repository update \
  --name myregistry \
  --image inference-api:v1.2.0 \
  --write-enabled true
```

## Clean up untagged images

When you push a new image with an existing stable tag, the previous image becomes untagged. These "orphan" images consume storage, and no tag references them. Over time, untagged images accumulate and increase storage costs.

### Auto-purge untagged images

The `acr purge` command runs as a container within ACR Tasks, allowing you to clean up images on demand or as part of automated workflows. You specify filters to target specific repositories and age thresholds to protect recent images. Use the `acr purge` command to delete untagged manifests older than a specified duration:

Azure CLI

```
az acr run --registry myregistry \
  --cmd "acr purge --filter 'inference-api:.*' --untagged --ago 30d" \
  /dev/null
```

This command removes untagged images in the `inference-api` repository that are older than 30 days. The filter uses a regular expression to match repository names.

### Schedule automatic cleanup

Automating cleanup through scheduled tasks ensures consistent registry maintenance without manual intervention. By running purge operations on a regular schedule, you prevent storage accumulation and keep costs predictable. Create a scheduled ACR Task to run cleanup automatically:

Azure CLI

```
az acr task create \
  --registry myregistry \
  --name cleanup-untagged \
  --cmd "acr purge --filter '.*:.*' --untagged --ago 7d" \
  --schedule "0 0 * * 0" \
  --context /dev/null
```

This task runs weekly and removes untagged images older than seven days across all repositories.

### Retention policies

Retention policies offer a simpler alternative to scheduled purge tasks for Premium tier registries. Instead of managing task schedules and filters, you configure a single policy that applies registry-wide. For Premium tier registries, you can set retention policies at the registry level. These policies automatically remove untagged manifests after a specified number of days without requiring scheduled tasks.

## Best practices for tagging and versioning

Follow these practices to maintain a reliable container image strategy:

- **Use unique tags for production:** Guarantee consistency across all nodes in your deployment. Unique tags prevent surprises when images update.
- **Reserve stable tags for base images:** Allow security updates to flow automatically to dependent images through base image triggers.
- **Lock production images:** Prevent accidental deletion of images actively serving traffic. Unlock only when retiring versions.
- **Implement retention policies:** Clean up orphaned images to control storage costs. Schedule regular purge tasks.
- **Include build metadata:** Add traceability information to tags for debugging and auditing. Link images to builds and source commits.
- **Document your tagging scheme:** Ensure your team follows consistent conventions. Document which tags are stable versus unique and when to use each.

## Additional resources

- [Recommendations for tagging and versioning container images](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-image-tag-version)
- [Lock a container image in Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-image-lock)
- [Automatically purge images from an Azure container registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-auto-purge)

## Troubleshooting

If you encounter issues try the following troubleshooting steps:

**Verify Azure authentication and environment variables**

- Run **az account show** to confirm you're logged in to the correct Azure subscription.
- Verify your environment variables are set by running **echo $ACR_NAME** (Bash) or **$env:ACR_NAME** (PowerShell).
- If variables are empty, re-run **source .env** (Bash) or **. ..env.ps1** (PowerShell).

**Verify ACR deployment**

- Navigate to the [Azure portal](https://portal.azure.com/) and locate your resource group.
- Confirm that the Azure Container Registry exists and shows a **Provisioning State** of **Succeeded**.
- Run **az acr list --output table** to verify your registry is accessible.

**Troubleshoot build failures**

- Check the build output for error messages - common issues include missing Dockerfile or incorrect file paths.
- Verify you're running commands from the project root directory (where the _api_ folder is located).
- Run **az acr task list-runs --registry $ACR_NAME --output table** to see the status of recent builds.


## Additional resources

- [Azure Container Registry documentation](https://learn.microsoft.com/en-us/azure/container-registry/)
- [Tutorial: Build and deploy container images in the cloud with ACR Tasks](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tutorial-quick-task)
- [Best practices for Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-best-practices)
- [Recommendations for tagging and versioning container images](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-image-tag-version)
