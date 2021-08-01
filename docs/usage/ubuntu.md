# Ubuntu Usage

![HIASBCH MQTT Blockchain Agent](../img/project-banner.jpg)

# Introduction
This guide will take you through using the **HIASBCH MQTT Blockchain Agent**.

&nbsp;

# Prerequisites

- You must have completed the [HIASBCH MQTT Blockchain Agent installation guide](../installation/installation.md).

- Ensure **HIAS**, **HIASBCH**, **HIASHDI** and **HIASCDI** are **running**.

&nbsp;

# Start the Agents

Now you are ready to fire up your HIASBCH MQTT Blockchain Agents, to do so use the following command:

``` bash
sudo systemctl start HIASBCH-MQTT-Blockchain-Agent.service
sudo systemctl start HIASBCH-MQTT-Blockchain-Agent-Replenish.service
```

# Manage the Agent

To manage the agents you can use the following commands:

``` bash
sudo systemctl restart HIASBCH-MQTT-Blockchain-Agent.service
sudo systemctl stop HIASBCH-MQTT-Blockchain-Agent.service

sudo systemctl restart HIASBCH-MQTT-Blockchain-Agent-Replenish.service
sudo systemctl stop HIASBCH-MQTT-Blockchain-Agent-Replenish.service
```

&nbsp;

# Contributing
Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss encourages and welcomes code contributions, bug fixes and enhancements from the Github community.

Please read the [CONTRIBUTING](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/blob/main/CONTRIBUTING.md "CONTRIBUTING") document for a full guide to forking our repositories and submitting your pull requests. You will also find our code of conduct in the [Code of Conduct](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/blob/main/CODE-OF-CONDUCT.md) document.

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