# Code Runner Plugin
![cover_logo](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/logo.png?raw=true "")</br>
[![Plugin](https://img.shields.io/badge/Code%20Runner-Plugin-blue)](https://code-runner-plugin.vercel.app/)
[![Plugin - Manifest](https://img.shields.io/badge/Code%20Runner-Manifest-blue)](https://code-runner-plugin.vercel.app/.well-known/ai-plugin.json)
[![Plugin](https://img.shields.io/badge/Paypal-Support-blue)]([https://code-runner-plugin.vercel.app](https://www.paypal.com/paypalme/EpicProTeam?country.x=IN&locale.x=en_GB))</br>
<a href="https://www.buymeacoffee.com/haseebheaven"><img src="https://img.buymeacoffee.com/button-api/?text=Support Code Runner&emoji=&slug=haseebheaven&button_colour=40DCA5&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>


## Introduction
Check out my first awesome plugin for **ChatGPT** that lets you Run code in 70+ languages! 🙌👩‍💻👨‍💻 </br>
This code will run this Plugin on your local machine with localhost:8000 as the URL. </br>
If you want to use Hosted one then check The Website is hosted on [Vercel](https://code-runner.heavenplugins.com)</br>
Checkout new designed website for [Code Runner](https://code-runner-plugin.b12sites.com) </br>

## Information
💻 **Run And Save Code** in over 70 programming languages with ease! **Chat-GPT Code Runner** offers a *versatile* and *flexible* coding experience for developers of all levels.</br>
💾 Download Chat-GPT **Code Runner** today and start coding like a pro!</br>
Ready to supercharge your coding experience? Check out Code Runner Plugin, the ultimate Chat-GPT plugin for running and saving code in over 70 programming languages!</br>

This uses JDoodle compiler API to execute your code and provide you with the output.
Checkout JDoole API [here](https://www.jdoodle.com/compiler-api/).
The API Keys are embeded in the code and you get _200_ free API calls per day. Make sure to call Get Credits Spend API to check your remaining credits.

# Version and Update.
The current version is *Code Runner 1.3* and important notice.
### UPDATE:

New **Free Plans** and **Premium Plan** are available for **Code Runner**. This plan includes the following features:</br>
![plugin_pricing](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/server/resources/code-runner-pricing.png?raw=true "")</br>

To unlock these features, checkout the below links:</br>

[Pricing Plans](https://code-runner-plugin.b12sites.com/pricing)</br>
[Support](https://www.paypal.com/paypalme/EpicProTeam)</br>

### Features:
- **Save Snippets:** Save your code snippets for future reference and easy access in image format with color syntax highlighting powered by [Kod.so](https://kod.so).</br>
![carbon_cpp_output](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/server/resources/carbon_cpp_output.png?raw=true "")</br>
[Code Snippets Share Code - ChatGPT](https://chat.openai.com/share/1b61bc05-067b-4779-b208-a297534cba2b)</br>

For questions:

- Discord: [Discord](https://discord.gg/BCRUpv4d6H)
- Github: [Github](https://github.com/haseeb-heaven/CodeRunner-Plugin)

Thank you for your support!

### UPDATE:
- **No Internet Access:** For **privacy** and **security** reasons, the **Python** environment does not have internet access. This means that **Python** libraries that require internet access to fetch data (like requests) won't work in this environment.
- **Framwork updated:** For this version we have migrated to the *Quart* framework because of limitation of size on *Vercel Serverless functions*.

# Installation.
To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements.txt
```

To run the plugin, enter the following command:

```bash
python main.py or  uvicorn main:app --reload
```

1. Navigate to https://chat.openai.com. </br>
2. In the Model drop down, select "Plugins" (note, if you don't see it there, you don't have access yet).</br>
3. Select "Plugin store"</br>
4. Search for "Code Runner" </br>
5. Authenticate the Plugin with your account with authenticaion code recieved in email by PluginLab Support.</br>
6. Install and Run the plugin and ask ChatGPT to generate some code you and run them.</br>
![search_plugin](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/server/resources/plugin_search_result.png?raw=true "")</br>

## General Information

- Plugin uses the JDoodle Compiler API to execute your code and provide you with the output.
- Plugin lets you customize your coding environment with different themes and output types.
- Plugin helps you debug your code with syntax highlighting and error messages.
- Plugin allows you to save your code locally for future reference and easy access.

## Usage

To use Code Runner Plugin, follow these steps:

- Load the plugin in Chat-GPT by selecting "Plugins" from the Model drop down menu and then choosing "Code Runner" from the list of available plugins.
- Use one of the following prompts in the chat box and press enter:

### Running your code.
  - Write me a C++ program for factorial of a number and Run the program: This prompt will write a C++ program for the factorial of a number and then run the program.
  - Given the program [YOUR_CODE] and only compile the program: This prompt will compile the program [YOUR_CODE]. Please replace [YOUR_CODE] with your specific code when using this prompt.
  ![run_code](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_output.png?raw=true "")</br>

### Saving your code.
- To save your code, use the following prompt in the chat box and press enter:

  - Save the program [YOUR_CODE] with filename [YOUR_FILENAME]: This prompt will save the program [YOUR_CODE] with filename [YOUR_FILENAME]. Please replace [YOUR_CODE] and [YOUR_FILENAME] with your specific code and filename respectively when using this prompt.
![save_code](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_output_save.png?raw=true "")</br>

### Downloading your code.
- To download your code, use the following prompt in the chat box and press enter:

  - Download the code filename [YOUR_FILENAME]: This prompt will download the code with filename [YOUR_FILENAME]. Please replace [YOUR_FILENAME] with your specific filename when using this prompt.
![download_code](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_output_download.png?raw=true "")</br>

## Features

Some of the features of Code Runner Plugin are:

- Support for over 70 programming languages, including Python, Java, C++, Ruby, PHP, JavaScript, and more.
- Syntax highlighting and auto-completion for better coding experience.
- Ability to run and save code locally with a single click.
- Ability to customize themes and output types for your coding environment.
- Fast and reliable execution of code using the JDoodle Compiler API.

## Localhost & Server Files.
The localhost and server files are located in the following directories:
- local: `main.py`
- Server: `server/main.py`

For demo purpose i also created this in Quart framework. The files are located in the following directories:
- Quart Main: `server/main_quart.py`

## Showcase - Demo of Plugin.</br>
[![code_plugin_demo](https://img.youtube.com/vi/Ahko7E2S1R8/0.jpg)](https://www.youtube.com/watch?v=Ahko7E2S1R8)</br>

## Join Community.
Join the community of Code-Runner on Discord [here](https://discord.gg/BCRUpv4d6H).

## Help
To get help with Code Runner Plugin, use the following prompt in the chat box and press enter: </br>
![help](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_help_url.png?raw=true "")</br>

## License and Author
Code Runner Plugin is licensed under the [Proprietary License](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/main/LICENSE).</br> make sure you read and understands everything written in license and agree to them before using the plugin.

## Privacy Policy.
The privacy policy for Plugin and Website could be found here [Privacy Policy](https://code-runner-plugin.vercel.app/privacy)
make sure you read them carefully before executing them.

Code Runner Plugin is developed by [Haseeb Heaven](https://github.com/haseeb-heaven), a software engineer and AI enthusiast.</br>
If you have any feedback or suggestions for Code Runner Plugin, feel free to contact me at [Email](haseebmir.hm@gmail.com) or open an issue on GitHub.</br>
