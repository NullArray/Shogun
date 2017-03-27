# Shogun
Shodan.io Command Line Interface

Shogun is a custom CLI for the Shodan.io search engine. It is designed to look and act like a "shell" to the Shodan database and 
aims to be a comprehensive assistant in the gathering of open source intelligence.

Features include the ability to resolve domains, check if a host IP has any ports with certain services running and attempts to enumerate these services. It can also provide a summary of all the information Shodan has on platforms such as 'IIS' or Apache etc and includes the possibility to log all information gathered in this manner. 


## Usage

Cloning the repo.
``
git clone https://github.com/NullArray/Shogun.git
cd Shogun
python shogun.py
``

The commands for Shogun are as follows.
```
Help    - Print usage information" 
Resolve - Query DNS to retrieve a domain's associated IP address
Ports   - Retrieve ports/services associated with provided host IP
Platform- Retrieve IPs associated with platform. I.E. 'Routers' returns a list of IPs that are classified as part of such
Summary - Provide a summary of information on provided search item. I.E. 'IIS' will provide top results for 'IIS'
Logging - Enable or disable search result logging(Disabled by default)
Api     - Display API key info and/or change API key
Quit    - Exit Shogun
```

## Dependencies

Besides the Shodan module Shogun makes use of Blessings as well for formatting purposes. Should you find you do not have these installed please use `pip` to get them like so.
```
pip install shodan
pip install blessings
```
Or feel free to use the requirements file i have made for this program.

`pip install -r requirements.txt`
