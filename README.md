# D7032E-Exam
This is my home exam for the course D7032E at LTU. The goal of this project is to implement a version 
of the game Boggle with a good software architecture.

## Running the program
This program is implemented in Python for a UNIX based operating system. It needs a python interpreter to function, which can be found 
at `https://www.python.org/downloads/`. The root folder of the project is the D7032E-Exam folder, which 
mean that the program should be ran from there and not the src folder. To run the host application, make
sure you stand in the D7032E-Exam directory in the command line, and run the following command (for UNIX 
based operating systems).

```sudo python3 src/host.py```

The program needs sudo permissions to be able to bind to sockets. 

The client is started in the same manner, does not need sudo permission.

```python3 src/client.py```

The client can also be reached using telnet, logging in to localhost on port 666 (Just make sure not to 
play DOOM at the same time)

```telnet localhost 666```

The unit test is started in the same manner.

```python3 src/unit_test.py```

## Development
The development of this software was a part of the course D7032E at LTU, and was done solely by me, 
Josef Utbult. This code is open source and I invite you to use and to study it, if needed for example 
for this course. I do not though take any responsibility if you copy parts of it for this course (if the 
examinator doesn't change assignments for next year), as this is clearly stated as against the rules.
