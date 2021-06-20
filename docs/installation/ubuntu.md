# Ubuntu Installation

![HIASBCH MQTT Blockchain Agent](../img/HIASBCH-MQTT-Blockchain-Agent.jpg)

# Table Of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
	- [HIAS Server](#hias-server)
- [Installation](#installation)
	- [Clone the repository](#clone-the-repository)
		- [Developer forks](#developer-forks)
	- [Installation Script](#installation-script)
- [HIAS](#hias)
	- [HIAS IoT Agent](#hias-iot-agent)
- [Service](#service)
- [Continue](#continue)
- [Contributing](#contributing)
  - [Contributors](#contributors)
- [Versioning](#versioning)
- [License](#license)
- [Bugs/Issues](#bugs-issues)

# Introduction
This guide will guide you through the installation process for the HIASBCH MQTT Blockchain Agent.

&nbsp;

# Prerequisites
You will need to ensure you have the following prerequisites installed and setup.

## HIAS Server

The HIASBCH MQTT Blockchain Agent is a core component of the [HIAS - Hospital Intelligent Automation Server](https://github.com/AIIAL/HIAS-Server). Before beginning this tutorial you should complete the HIAS installation guide and have a HIAS server online.

&nbsp;

# Installation
You are now ready to install the HIASBCH MQTT Blockchain Agent software.

## Clone the repository

Clone the [HIASBCH MQTT Blockchain Agent](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent " HIASBCH MQTT Blockchain Agent") repository from the [Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss](https://github.com/AIIAL "Asociación de Investigacion en Inteligencia Artificial Para la Leucemia Peter Moss") Github Organization.

To clone the repository and install the project, make sure you have Git installed. Now navigate to your HIAS installation project root and then use the following command.

``` bash
 git clone https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent.git
 mv HIASBCH-MQTT-Blockchain-Agent components/agents/hiasbcha
```

This will clone the HIASBCH MQTT Blockchain Agent repository and move the cloned repository to the agents directory in the HIAS project (components/agents/hiasbcha/).

``` bash
 cd components/agents/
 ls
```

Using the ls command in your home directory should show you the following.

``` bash
 hiasbcha
```

Navigate to the **components/agents/hiasbcha/** directory in your HIAS project root, this is your project root directory for this tutorial.

### Developer forks

Developers from the Github community that would like to contribute to the development of this project should first create a fork, and clone that repository. For detailed information please view the [CONTRIBUTING](https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent/blob/main/CONTRIBUTING.md "CONTRIBUTING") guide. You should pull the latest code from the development branch.

``` bash
 git clone -b "2.0.0" https://github.com/AIIAL/HIASBCH-MQTT-Blockchain-Agent.git
```

The **-b "2.0.0"** parameter ensures you get the code from the latest master branch. Before using the below command please check our latest master branch in the button at the top of the project README.

## Installation script

All other software requirements are included in **scripts/install.sh**. You can run this file on your machine from the HIAS project root in terminal. Use the following command from the HIAS project root:

``` bash
 sh components/agents/hiasbcha/scripts/install.sh
```

&nbsp;

# HIAS

This device is a HIAS IoT Agent and uses the HIAS MQTT Broker to communicate with the HIAS network. To setup an IoT Agent on the HIAS network, head to the HIAS UI.

The HIAS network is powered by a context broker that stores contextual data and exposes the data securely to authenticated HIAS applications and devices.

Each HIAS IoT Agent has a JSON representation stored in the HIASCDI Context Broker that holds their contextual information.

## HIAS IoT Agent

A HIAS IoT Agent is a bridge between HIAS devices and applications, and the HIASCDI Context Broker. The IoT Agents process incoming data using a specific machine to machine communication protocol and then converting into a format compatible with HIASCDI, before sending the data to HIASCDI to update the contextual information.

![HIAS IoT Agents](../img/hias-iotjumpway-agents.jpg)

You will now need to create your HIASC IoT Agent and retrieve the agent credentials. Navigate to **IoT->Entities->Agents** and click on the **+** next to the **Network Agents** title to create a HIAS IoT Agent.

![HIAS IoT Agent](../img/create-hias-iotjumpway-agent.jpg)

Make sure to select **MQTT** as the protocol for your Agent. Once you have completed the form and submitted it, you can find the newly created AI Agent by navigating to **IoT->Entities->Agents** and clicking on the relevant Agent.

On the HIAS IoT Agent page you will be able to update the contextual data for the agent, and also find the JSON representation.

![HIAS IoT Agent](../img/edit-hias-iotjumpway-agent.jpg)

You now need to download the credentials required to connect the Acute Lymphoblastic Leukemia oneAPI Classifier to the HIAS network.

Click on the **Agent Credentials** section to download the credentials file. This should open your file browser, navigate to the **HIAS/components/agents/hiasbcha/configuration/** directory and save the file as **credentials.json**.

&nbsp;

# Service
You will now create a service that will run your IoT Agent. Making sure you are in the HIAS project root, use the following command:

``` bash
sh components/agents/hiasbcha/scripts/service.sh
```

&nbsp;

# Continue
Now you can continue with the HIAS [getting started guide](../getting-started.md)

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