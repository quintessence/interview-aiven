# Aiven GitHub Organization

The purpose of this write up is to provide feedback on the repositories in the GitHub organization, either as constructive praise or criticism.

### Constraints

The main constraint here is I'm unsure of the finer details of the business strategy for the GitHub organization. For example, is there a goal to increase usage of certain integrations, or to encourage certain adoption patterns? I mention this a bit in the feedback section itself. In a different situation I'd follow up and ask for clarification, but since I had initially interpreted the instructions to mean the GitHub feedback would be verbal in an interview loop I wanted to mention this explicitly so you would know that I would ask for clarification rather than trying to move forward without it in general.

# The Feedback Itself

My thoughts are that, overall, Aiven has done an amazing job at providing engineers with tools to improve their ability to interact with the Aiven platform overall. The main areas to improve currently are around how those tools are surfaced to make it easier for engineers to find what they need.

## First Impressions

Building on that, my first impression when opening the organization landing page is that there are a _lot_ of repositories and none of the pinned repositories are general information such as user documentation or a README for the organization itself. That said, the search function that GitHub provides makes it easy to find an individual repository if you already know mostly what you're looking for, e.g. searching `terraform` successfully finds the Terraform provider.

## Tool Availability

The tools, integrations, services, etc. that are available in the GitHub organization match what I'd expect to see based on the advertised services available on aiven.io. Specifically when I look at the main (aiven.io) page, what I see are the advertised supported cloud platforms, databases, document stores, and so on. I then verified I could find corresponding tools in the GitHub organization and was able to do so by searching the individual service names.

## Improvements

As mentioned, most of the areas of improvement that I found are around how we present the material rather than material that is missing. 

### A README

Just like an individual code repository, the Aiven GitHub organization should have a README file. This file shows on the Overview tab, such as shown for the [Aurae Runtime project](https://github.com/aurae-runtime). The Aiven org-level README should focus on succinctly providing users the ability to quickly find:

* A few tools or sources of information that would be common to all Aiven users. Two good examples would be a link to the user docs (whether they live in the GitHub organization or aiven.io) and the Aiven command line tool.
* The top level categories for the types of tools provided and then a bulleted list of tools in that category, appropriately linked. If the setup documentation for the provider / tool is not in the repository itself, it should be linked as well.

For the latter: a great example would be what I mentioned earlier like Terraform. If I am already in a company that is committed to using / already using Terraform, then I would just search for Terraform in the GitHub org and find the appropriate repository. On the other hand, if my company or project is still in the discovery phase and is building the toolchain, what would help me the most is seeing _all_ supported providers in a category.

An example draft for subset of the tools:

```
# Welcome

Welcome to Aiven's GitHub! Here you'll find a collection of tools and integrations to fine-tune how you interact with our platform.

# Getting Started and Common Tools

* [Our User Documentation](link)
* [Aiven CLI](link)
* [Code Samples](link)

# Providers 

## Infrastructure as Code/Software

* [Terraform](link)
* [Pulumi](link)

## RDBMS

* [postgres](link)
* [MySQL](link)

## Visualization

* [Grafana Integration](link), [Grafana Setup Documentation](link)
```

For the last service, I showed one way to quickly link separate GitHub and documentation links.

### Pinned Repositories

Choosing which repositories are pinned should be a combination of common needs and business strategy around the GitHub organization. The common needs, same as before, would be user docs (if they were in the GitHub organization) and code samples.

For business strategy there are a few different goals that would inform what repositories to pin:

* Are we looking to drive contributions or consumption of the tools?
* Are we looking to attract attention to specific repositories over others?
* Are we broadcasting this strategy in the org-level README?

For example, if we want to drive contributions we should have a repository that hosts the README or documentation that explains how to be a contributor. That repository should then be pinned, as well as highlighting the repositories that we want to drive contributions in. We should also put a "call for contributors" short description on the org-level README.

As a second example, if we are more interested in driving usage of some integrations over others, for example if we want to highlight our RDBMS providers, then those should be pinned. In this case we do not need to have additional information in the org-level README. This might be the situation if we have recent partnerships that we want to draw attention to or if we have toolchain opinions we wanted to gently encourage.

### Setup READMEs

Some of the projects have more thorough READMEs than others. The main improvement here would be to ensure that all READMEs are written so that someone new to the code has their expectations set on what it should and should not provide as well as set up instructions. Two examples I'd like to focus on to highlight this are the Aiven Client and the Aiven Go Client.

For the Aiven Client, written in Python, the README is very thorough and an excellent standard of what to include. Users know how to install and set up the tool, how to get help if they're trying to figure out what commands are available and the associated syntax, as well as thorough usage information including login and how to interact with services. As a first time user or new user I could use this README to become familiar with the client quickly.

The Aiven Go Client by contrast is incredibly sparse. The README _does_ set the expectation that the Go client is not the command line interface and to use the Python client if that's what the user is looking for. What it doesn't do is provide information that would help with a first time user trying to use the SDK. In order to understand what is provided, the user would need to start reading the code or have pre-existing knowledge. As a quick example, there is a `Makefile` in the repository - a handy pattern. This should be called out in the README as well as the syntax of the options and a description of what they do. The `README` should also call out any dependencies that need to be installed as well as versioning limitations either directly of Go itself (e.g. go1.16+), the API(s) the SDK interacts with, and any deprecations (e.g. ElasticSearch).

My recommendation here would be to review the repositories and rank which ones need additional love. Litmus testing on a few for the purposes of this feedback I found that the Terraform provider and pghoard both have very well laid out READMEs whereas the Opensearch Connector for Kafka and pgtracer could use some additional attention.

### Example Data


The final bit of feedback is something I encountered while building the data loader for the coding part of my assignment: there should be a way to quickly set up a demo environment if that is what the user is looking for. This would be analogous to the example data that is provided in the web interface, but would allow potential users to bulk upload their own data to quickly assess if our platform is a good fit for their use case using their own data if/when available. This would especially help in situations where there is a gap in expertise between decision makers and implementers: engineers using the tooling that is in the GitHub repository would also benefit from being able to make their trial fit their exact use case as precisely as possible, but the person or people making the purchasing decisions would primarily interact with the WYSIWYG setup in the web UI.