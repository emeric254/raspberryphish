# RaspberryPhish
=================

## Disclaimer

This project is for education purposes only !

Unauthorized attempts to defeat or circumvent security features, to use the system for other than intended purposes, to deny service to authorized users, to access, obtain, alter, damage, or destroy information, or otherwise to interfere with the system or its operation are prohibited.
Evidence of such acts may be disclosed to law enforcement authorities and result in criminal prosecution.
By using this project you indicate your awareness of and consent to that.

I do not provide any warranty of this project whatsoever, whether express, implied, or statutory, including, but not limited to, any warranty of merchantability or fitness for a particular purpose or any warranty that its contents will be error-free.
I'm not responsible for direct, indirect, incidental or consequential damages resulting from any defect, error or failure to perform. 
This project could kill your cat, fire your house, start mayan apocalypse or a civil war.

Use it at your own risks !

-----

## Description

This project is used in a university security project.
Its purpose is to counterfeit wifi hotspots and collect credentials of careless students.

This project is divided in four main parts:
  * **scripts** and **conf** are used in OS integration and hotspot creation
  * **FishingServer** is the main phishing component
  * **Bot** can verify phishing credentials
  * **AdminServer** to administrate all other components

-----

## LOGS

The **logs** folder contains various server logs. It also contains a **dumps** folder.
This **dumps** folder is where credentials are saved, filtered by website name.

Each login request is saved to a file, which is named by it's datetime, and contains form data in _json_ format.

## Scripts

TBD

## FishingServer

This server is a fake website providing only two pages to visitors: an home page and an error page.

The home page contains a login form where the user will input its credentials.

The error page is provided when users have perform a login request.

## AdminServer

TBD

## Bot

This tool will test collected credentials by using them to connect to the real service.

It can also be used to collect some information about these accounts.
