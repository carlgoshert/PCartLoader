# Contributing

Thank you for taking the time to read this before contributing to my small project! All human-made contributions to PCartLoader are very welcomed. I started this project as a means to avoid using an AI generated alternative. As such, AI generated commits and PRs are disallowed in this repository. Please refrain from submitting such.

Before contributing to this project, please star the project on Github and read the entirety of this page. If you are a first-time contributor to an open-source project, I recommend reading [How to Contribute to Open Source](https://contributing.md/how-to-contribute-to-open-source/) to better understand the ethos of open-source contributions. Thank you.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Contributing Code](#contributing-code)
  - [Styleguide](#styleguide)
  - [Claiming Issues](#claiming-issues)
  - [PR Requirements](#pr-requirements)

## Code of Conduct

Please refer to the [Contributor Covenant 3.0 Code of Conduct](https://www.contributor-covenant.org/version/3/0/code_of_conduct/) for expected behavior within this project. We currently do not have a pipeline for reporting violations, but know that I, the repository owner, will be monitoring all communication in Issue and PR threads on Github and will personally enforce the CoC with bans from the project.

## I Have a Question

Before you ask a question, it is best to search for existing [Issues](https://github.com/carlgoshert/PCartLoader/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- [Open an Issue](https://github.com/carlgoshert/PCartLoader/issues/new).
- Provide as much context as you can about what you're running into.
- Provide additional information that seems relevant, such as operating system and hardware information, or project branch/release version used.

We will then address the issue as soon as possible.

## Reporting Bugs

### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/carlgoshert/PCartLoader/issues?q=label%3Abug).
- Collect information about the bug:
  - Contents of your PCartLoader.log file during the time the error occured.
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of PCartLoader used.
- Can you reliably reproduce the issue? Include a list of the steps you took to produce the issue.

### How Do I Submit a Good Bug Report?

We use [GitHub issues](https://github.com/carlgoshert/PCartLoader/issues) to track bugs and errors. If you run into an issue with the project:

- [Open an Issue](https://github.com/carlgoshert/PCartLoader/issues/new).
- Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own.
- Provide the information you collected in the previous section.

### Once the Report is Filed:

- A project Maintainer will label the issue accordingly.
- A project Maintainer will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
  - If a Maintainer is able to reproduce or verify the issue, the issue will be marked with a `needs-fixed` tag. Other tags may be used depending on the severity of the issue.
  - A Maintainer will then assign themselves or another Contributor to the issue. (**Contributors:** Please see [this section](#claiming-issues) to learn how to request assignment to an issue before beggining work on your PR.)

## Suggesting Enhancements

The following guidelines should be used when suggesting new features to the project, or suggesting a change to how a problem or issue was previously resolved.

### Before Suggesting an Enchancement

- Make sure you are using the latest version.
- Ensure the functionality is not already covered.
- Search the [issue tracker](https://github.com/carlgoshert/PCartLoader/issues) to ensure the enhancement has not already been suggested.
- Consider whether your idea fits the scope and vision of the project. You must make your case to convince the Maintainers the feature is useful to a significant number of users and warrants development time.

### How Do I Submit a Good Enhancement Suggestion?

We will be using [Github Issues](https://github.com/carlgoshert/PCartLoader/issues) to track enhancement and feature requests.

- [Open an Issue](https://github.com/carlgoshert/PCartLoader/issues/new).
- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- Include screenshots or mockup drawings to help visualize the feature request.
- **Explain why this enhancement would be useful** to most users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

## Contributing Code

Please refer to the subsections below before submitting any Pull Requests or commenting on open Issues.

### Styleguide

Please follow the [PEP 8 Style Guide for Python](https://peps.python.org/pep-0008/) as closely as possible in order to maintain "pythonic" code. This guideline is a suggestion to help other Maintainers read and understand your code, not a hard rule. PRs that fail to maintain this standard perfectly may not be subject to closure unless the code written falls well outside the norm for the existing codebase or is considered unreadable by the PR reviewer.

### Claiming Issues

As a Contributor, if there are open issues on the [bug tracker](https://github.com/carlgoshert/PCartLoader/issues?q=label%3Abug) that you wish to claim and attempt a solution for, please kindly leave a comment in the issue thread declaring your intent to address the issue. A Maintainer may then assign you to the issue. 

Failure to claim an issue before submitting a Pull Request may result in closure if another Contributor is already at work on the issue. Failure to submit a PR within a timely manner after being assigned to an issue may result in another Contributor moving forward with the work instead.

### PR Requirements

If you fail to adhere to the following guidelines, a Maintainer may point to this document and request an update to your Pull Request, or close the PR outright as the Maintainer deems neccessary.

#### Merge Workflow 

This project is maintained with [the Gitflow method](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow), not a trunk-based workflow. This is not a Dev-Ops environment. Please submit all Pull Requests to the `dev` branch. Any PRs that request a merge into the `main` branch will be immediately closed for failing to meet this standard. The `main` branch is reserved for release-ready code and will only be updated by the owner of the repository.

#### PR Messages

All Pull Requests must contain the following information in their initial comment:

- **Issue** - Include a link to the [open issue](https://github.com/carlgoshert/PCartLoader/issues) this PR addresses.
- **Problem** - Include a *brief* description of the problem space introduced by the issue. For bugs, do not regurgitate the description from the tracked issue. Instead, explain the root cause of the problem addressed.
- **Changes** - Include a *brief* summary of the changes made to address the issue. It is not required for you to give a line-by-line explanation of all code additions/changes. Simply list the libraries, classes, or functions at the root of the solution and summarize their changes.
