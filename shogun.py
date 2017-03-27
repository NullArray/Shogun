#!/usr/bin/env Python2.7

import sys
import os, os.path
import shodan
import pickle
import socket

from datetime import datetime
from blessings import Terminal

t = Terminal()
ts = datetime.now()

reset = False
logging = False
api = ""

print t.cyan("""

.d88888b  dP                                           
88.    "' 88                                           
`Y88888b. 88d888b. .d8888b. .d8888b. dP    dP 88d888b. 
      `8b 88'  `88 88'  `88 88'  `88 88    88 88'  `88 
d8'   .8P 88    88 88.  .88 88.  .88 88.  .88 88    88 
 Y88888P  dP    dP `88888P' `8888P88 `88888P' dP    dP 
                                 .88                   
                             d8888P          				  """)
print t.cyan("\n		SHOGUN - Shodan Command Line Interface\n")


def key():
	global api
	if reset == True:
		
		if os.path.isfile("api.p"):
			path = os.path.abspath("api.p")
		
		try:
			os.remove(path)
		except:
			print "\n[" + t.red("!") + "]Critical. Deleting old API key file failed"
			print "[" + t.magenta("?") + "]Continue with old APY key?\n"
			
			query = raw_input("[Y]es/[No]: ")
			if query == "y":
				main()
			elif query == "n":
				print "\n[" + t.red("!") + "]Aborted."
				sys.exit(1)
			else:
				print "\n[" + t.red("!") + "]Unhandled option. Defaulting to main menu."
				main()
				
			
	if not os.path.isfile("api.p"):
		print "[" + t.green("+") + "]Please provide your Shodan.io API key."
		
	
		SHODAN_API_KEY = raw_input("API key: ")
		pickle.dump(SHODAN_API_KEY, open( "api.p", "wb" ))
		
		print "\n[" + t.green("+") + "]Your API key has been saved to 'api.p' in the current directory.\n"
		
		print "[" + t.green("+") + "]Welcome to Shogun."
		print "[" + t.green("+") + "]This program serves as a simple CLI to the Shodan.io search engine." 
		print "[" + t.green("+") + "]Type the command 'help' to show which options are available to you.\n\n"
	
	else:
		path = os.path.abspath("api.p")
		SHODAN_API_KEY = pickle.load(open( "api.p", "rb" ))
		
		print "\n[" + t.green("+") + "]Your API key was loaded from " + path
		
		print "\n[" + t.green("+") + "]Welcome to Shogun."
		print "[" + t.green("+") + "]This program serves as a simple CLI to the Shodan.io search engine." 
		print "[" + t.green("+") + "]Type the command 'help' to show which options are available to you.\n\n"
		
	try:
		api = shodan.Shodan(SHODAN_API_KEY) 
	except Exception as e:
		print "\n[" + t.red("!") + "]Critical. API setup failed.\n"
		print e
		sys.exit(0)

	
	main()


def resolve():
	global logging
	print "\n[" + t.green("+") + "]Please provide the domain you wish to resolve. I.E. 'google.com'."
	
	query = raw_input("\n<" + t.cyan("RESOLVE") + ">$ ")
	
	try:
		
		data = socket.gethostbyname_ex(query)
	
		print "\n[" + t.green("+") + "]Domain resolves to: \n" + repr(data) + "\n"
	
	except socket.gaierror as e:
		print "[" + t.red("!") + "]Critical. A GAIerror was raised with the following error message."
		print e + "\n"
		
		print "[" + t.green("+") + "]Consider typing the domain without the protocol, I.E. 'google.com, instead of http://google.com"
		print "[" + t.green("+") + "]Defaulting to main menu."
	
	if logging == True:
		print "[" + t.green("+") + "]Results saved to shogun.log in the current directory"
		with open('shogun.log', 'ab') as log:
			log.write("Time: %s\n" % ts)
			log.write("Shogun Resolver Results Log. Query -> %s\n" % query)
			for items in data[2]:
				print items
				log.write("%s\n" % items)
		
	main()  


def ports():
	global api
	global logging
	print "\n[" + t.green("+") + "]Please provide a host IP."
	query = raw_input("\n<" + t.cyan("PORTS") + ">$ ")
	
	try:
		result = api.host(query)
		
		print
		print "[" + t.green("+") + "]Detail on %s:" % result['ip_str']

		for service in result['data']:
			print "\t- Running %s on port %d" % (service.get('product', 'unknown service'), service['port'])
		
	except Exception as e:
		print "[" + t.red("!") + "]Critical. An error was raised with the following error message.\n"
		print e 
		print "\n[" + t.green("+") + "]Defaulting to main menu."
		
		if logging == True:
			print "[" + t.green("+") + "]Results saved to shogun.log in the current directory"
			with open('shogun.log', 'ab') as log:
				log.write("Time: %s" % ts)
				log.write("Shogun Ports and Services Results Log. Query -> %s\n" % query)
				for service in result['data']:
					log.write("\t- Running %s on port %d" % (service.get('product', 'unknown service'), service['port']))
					log.write("\n")
			
	main()
		
		
def platform():
	global api
	global logging
	print "\n[" + t.green("+") + "]Please provide your search query."
	query = raw_input("\n<" + t.cyan("PLATFORM") + ">$ ")
	
	try:
		result = api.search(query)
		
		print
		for service in result['matches']:
			print service['ip_str']
		print
		
	except Exception as e:
		print "[" + t.red("!") + "]Critical. An error was raised with the following error message.\n"
		print e 
		print "\n[" + t.green("+") + "]Defaulting to main menu."
	
	if logging == True:
		print "[" + t.green("+") + "]Results saved to shogun.log in the current directory"
		with open('shogun.log', 'ab') as log:
			log.write("Time: %s\n" % ts)
			log.write("Shogun Platform Results Log. Query -> %s\n" % query)
			for service in result['matches']:
				log.write(service['ip_str'])
				log.write("\n")
		
	main()



def summary():
	global api
	global logging
	print "\n[" + t.magenta("?") + "]How many results would you like to display?"
	print "[" + t.green("+") + "]I.E. '10' shows top 10 results for search item."
	amount = raw_input("\n<" + t.cyan("SUMMARY") + ">$ ")
	
	if amount == "0":
		print "[" + t.red("!") + "]Amount must be greater than 0."
		print "\n[" + t.green("+") + "]Defaulting to main menu."
		main()
	
	print "\n[" + t.green("+") + "]Please enter your search query"
	query = raw_input("\n<" + t.cyan("SUMMARY") + ">$" )
	
	
	FACETS = [
	('org', amount),
	('domain', amount),
	('port', amount),
	('asn', amount),
	('country', amount),
	]

	FACET_TITLES = {
		'org': "Top" +repr(amount) + "Organizations",
		'domain': "Top" +repr(amount) + "Domains",
		'port': "Top" +repr(amount) + "Ports",
		'asn': "Top" +repr(amount) + "Autonomous Systems",
		'country': "Top" +repr(amount) + "Countries",
	}
	
	try:
		result = api.count(query, facets=FACETS)

		print "\n[" + t.green("+") + "]Summary information on item: [ %s ]" % (query)
		print "[" + t.green("+") + "]Total Results: %s\n" % result['total']

		print
		for facet in result['facets']:
			print FACET_TITLES[facet]

			for term in result['facets'][facet]:
				print "%s: %s" % (term['value'], term['count'])
			print

	except Exception as e:
		print "[" + t.red("!") + "]Critical. An error was raised with the following error message.\n"
		print e 
		print "\n[" + t.green("+") + "]Defaulting to main menu."

	if logging == True:
		print "[" + t.green("+") + "]Results saved to shogun.log in the current directory"
		with open('shogun.log', 'ab') as log:
			log.write("Time: %s\n" % ts)
			log.write("Shogun Summary Results Log. Query -> %s\n" % query)
			for facet in result['facets']:
				log.write(FACET_TITLES[facet])
				log.write("\n")
				for term in result['facets'][facet]:
					log.write("%s: %s" % (term['value'], term['count']))
					log.write("\n")

def commands():
	print
	print "[" + t.magenta("~") + "]Help    - Print usage information" 
	print "[" + t.magenta("~") + "]Resolve - Query DNS to retrieve a domain's associated IP address"
	print "[" + t.magenta("~") + "]Ports   - Retrieve ports/services associated with provided host IP"
	print "[" + t.magenta("~") + "]Platform- Retrieve IPs associated with platform. I.E. 'Routers' returns a list of IPs that are classified as part of such"
	print "[" + t.magenta("~") + "]Summary - Provide a summary of information on provided search item. I.E. 'IIS' will provide top results for 'IIS'"
	print "[" + t.magenta("~") + "]Logging - Enable or disable search result logging(Disabled by default)"
	print "[" + t.magenta("~") + "]Api     - Display API key info and/or change API key"
	print "[" + t.magenta("~") + "]Quit    - Exit Shogun"
	
		
def main():
	global api
	global reset
	global logging
	
	while True:
		query = raw_input("\n<" + t.cyan("SHOGUN") + ">$ ")
	
		if query == "help":
			commands()
		elif query == "resolve":
			resolve()
		elif query == "ports":
			ports()
		elif query == "platform":
			platform()
		elif query == "summary":
			summary()
		elif query == "logging":
			
			print "[" + t.magenta("?") + "]Enable logging?\n"
			logs = raw_input("[Y]es/[No]: ")
			
			if logs == "y":
				print "[" + t.green("+") + "]Logging enabled"
				logging = True
			elif logs == "n":
				print "[" + t.green("+") + "]Logging disabled"
				logging = False
			else:
				print "[" + t.red("!") + "]Unhandled option"
				logging = False
				
		elif query == "api":
			
			SHODAN_API_KEY = pickle.load(open( "api.p", "rb" ))
			
			print "\n[" + t.green("+") + "]Current API key: %s" % (SHODAN_API_KEY)
			print "\n[" + t.magenta("?") + "]Would you like to change your API key?"
			change = raw_input("[Y]es/[No]: ")
			
			if change == "y":
				reset = True
				key()
			elif change == "n":
				print "\n[" + t.green("+") + "]Aborted"
				reset = False
			else:
				print "[" + t.red("!") + "]Unhandled option"
				reet = False
				
				
		elif query == "quit":
			sys.exit(0)
		else:
			print "[" + t.red("!") + "]Unhandled option"

if __name__=="__main__":
	key()
