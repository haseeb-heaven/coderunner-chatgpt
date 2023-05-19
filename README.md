# Code Runner Plugin
![cover_logo](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/logo.png?raw=true "")</br>
[![Plugin](https://img.shields.io/badge/Code%20Runner-Plugin-blue)](https://coderunner-plugin.haseebmir.repl.co)
[![Plugin - Manifest](https://img.shields.io/badge/Code%20Runner-Manifest-blue)](https://coderunner-plugin.haseebmir.repl.co/.well-known/ai-plugin.json)
[![Plugin](https://img.shields.io/badge/Code%20Runner-Hosted-blue)](https://replit.com/@HaseebMir/CodeRunner-Plugin)

## Introduction
Check out my first awesome plugin for **ChatGPT** that lets you Run code in 70+ languages! 🙌👩‍💻👨‍💻 </br>
This code will run this Plugin on your local machine with localhost:8000 as the URL. </br>
If you want to use Hosted one then check The repo is hosted on [ReplIt](https://replit.com/@HaseebMir/CodeRunner-Plugin)

## Information
💻 **Run And Save Code** in over 70 programming languages with ease! **Chat-GPT Code Runner** offers a *versatile* and *flexible* coding experience for developers of all levels.</br>
💾 Download Chat-GPT **Code Runner** today and start coding like a pro!</br>
Ready to supercharge your coding experience? Check out Code Runner Plugin, the ultimate Chat-GPT plugin for running and saving code in over 70 programming languages!</br>

This uses JDoodle compiler API to execute your code and provide you with the output.
Checkout JDoole API [here](https://www.jdoodle.com/compiler-api/).
The API Keys are embeded in the code and you get _200_ free API calls per day. Make sure to call Get Credits Spend API to check your remaining credits.

# Installation.
To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements.txt
```

To run the plugin, enter the following command:

```bash
python main.py or  uvicorn main:app --reload
```

Once the local server is running:

1. Navigate to https://chat.openai.com. </br>
2. In the Model drop down, select "Plugins" (note, if you don't see it there, you don't have access yet).</br>
3. Select "Plugin store"</br>
4. Select "Develop your own plugin"</br>
5. Enter in `localhost:8000` since this is the URL the server is running on locally, then select "Find manifest file".</br>
- ### Finding the plugin.
- Use **localhost:8000** to find the loccal version of plugin</br></br>
- ![finding_plugin](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_find_local_plugin.png?raw=true "")</br></br>
- Use **https://coderunner-plugin.haseebmir.repl.co** to find the hosted version of plugin</br></br>
- ![finding_plugin](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_find_hosted_plugin.png?raw=true "")</br></br>
- ### Installing the plugin
- Installing the loccal version of plugin</br></br>
- ![finding_plugin](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_install_local_plugin.png?raw=true "")</br></br>
- Installing the hosted version of plugin</br></br>
- ![finding_plugin](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_install_hosted_plugin.png?raw=true "")</br></br>

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

## Help
To get help with Code Runner Plugin, use the following prompt in the chat box and press enter: </br>
![help](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/master/resources/coderunner_help_url.png?raw=true "")</br>

## License and Author
Code Runner Plugin is licensed under the [MIT License](https://github.com/haseeb-heaven/CodeRunner-Plugin/blob/main/LICENSE).</br>
Code Runner Plugin is developed by [Haseeb Heaven](https://github.com/haseeb-heaven), a software engineer and AI enthusiast.</br>
If you have any feedback or suggestions for Code Runner Plugin, feel free to contact me at [Email](haseebmir.hm@gmail.com) or open an issue on GitHub.</br>
