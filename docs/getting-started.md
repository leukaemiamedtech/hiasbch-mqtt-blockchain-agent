# Getting Started

![HIASBCH MQTT Blockchain Agent](img/HIASBCH-MQTT-Blockchain-Agent.jpg)

# Table Of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Start the Agent](#start-the-agent)
- [Manage the Agent](#manage-the-agent)
- [Contributing](#contributing)
    - [Contributors](#contributors)
- [Versioning](#versioning)
- [License](#license)
- [Bugs/Issues](#bugs-issues)

&nbsp;

# Introduction
This guide will guide you through getting started with the HIASBCH MQTT Blockchain Agent.

&nbsp;

# Installation
First you need to install the required software. Below are the available installation guides:

- [Ubuntu installation guide](installation/ubuntu.md)

**PLEASE NOTE** At this point both **HIAS** and **HIASCDI** should be **running** and you should be able to log in to the HIAS UI.

&nbsp;

# Start the Agent

Now you are ready to fire up your HIASBCH MQTT Blockchain Agent, to do so use the following command:

``` bash
sudo systemctl start HIASBCH-MQTT-Blockchain-Agent.service
```

# Manage the Agent

To manage the agent you can use the following commands:

``` bash
sudo systemctl restart HIASBCH-MQTT-Blockchain-Agent.service
sudo systemctl stop HIASBCH-MQTT-Blockchain-Agent.service
```

&nbsp;

# Contributing
Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss encourages and welcomes code contributions, bug fixes and enhancements from the Github community.

Please read the [CONTRIBUTING](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/blob/main/CONTRIBUTING.md "CONTRIBUTING") document for a full guide to forking our repositories and submitting your pull requests. You will also find information about our code of conduct on this page.

## Contributors
- [Adam Milton-Barker](https://www.leukemiaairesearch.com/association/volunteers/adam-milton-barker "Adam Milton-Barker") - [Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss](https://www.leukemiaresearchassociation.ai "Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss") President/Founder & Lead Developer, Sabadell, Spain

&nbsp;

# Versioning
We use SemVer for versioning.

&nbsp;

# License
This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/blob/main/LICENSE "LICENSE") file for details.

&nbsp;

# Bugs/Issues
We use the [repo issues](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/issues "repo issues") to track bugs and general requests related to using this project. See [CONTRIBUTING](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/CONTRIBUTING.md "CONTRIBUTING") for more info on how to submit bugs, feature requests and proposals.