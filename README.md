# Server_administrating_clients
Application Server using sockets and Kivy graphic library for python. Used to make a client-server interaction, in wich the clients sends it's system information to the server that then show's it graphically to the administrator

This application supports encryption using the AES algorithm.

# Install using PIP
2.2 Using Pip
  2.2.1 Install virtual environments
    $ python3 -m pip install --upgrade pip setuptools virtualenv
    $ python3 -m virtualenv kivy_venv
  2.2.2 Activate virtual environments
    2.2.2.1 Windows
      $ kivy_venv\Scripts\activate
    2.2.2.2 Bash
      $ source kivy_venv/Scripts/activate
    2.2.2.3 Linux
      $ source kivy_venv/bin/activate
  2.2.3 Install kivi
    $ python3 -m pip install kivy[full] kivy_examples -> for full dependencies
    $ pip install kivy[sdl2]
  Check the installation
    Windows:
      $ python3 kivy_venv\share\kivy-examples\demo\showcase\main.py
    Linux:
      $ python3 kivy_venv/share/kivy-examples/demo/showcase/main.py
      
# Operation
1. Start the server (navigate to the directory):
  $ python3 main.py
  -> Create the server according to your preferences and options
2. Start the client:
  $ python3 clientTCP.py
