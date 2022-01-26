# Mail - sender

Mail-sender is a simple utility for sending program output to mail

- 1 config file
- Any utilities, programs, binaries
- All popular mail services
   
### How it use:

  - git clone https://github.com/Volkov-R-Net/Mail-sender.git
  - chmod +x mail_sender.py
  - Edit the config file (Uncomment the options you want)
 
    ```
    [ssl] #If using ssl
    [tls] #If using tls
    [port] #If using custom port (or ssl, default = 25)
    [debug] #I recommend to enable this mode for the first letter
    [recips] #If you plan to send to multiple recipients
    [timeout] #include this block if the command output is expected after more than 2000 seconds
    seconds = 20201 #Enter the time in seconds (20201 - for example)
    [smtp] #This block contains data for interaction with the smtp server
    server = smtp.mail.ru
    user = example@mail.ru #user = from
    pass = example
    port = 465 #Use, if uncomment [port] (specify the port of your smtp)
    [TO] #Specify one or more (see [recips]) addresses (separated as in the example)
    emails = example.test@mail.ru, example@gmail.com
    [SUBJECT] #It is subject 
    subject = Mail-sender returns the result output of the utility
    ```
    ### Everything is ready to use!
    - If use one utility:  
    ```
    ./mail_sender.py utility -utility_options    
    ```    
    - If use bash-pipline:
    ```
    ./mail_sender.py "cat supertext | grep '#'"
    ```
    - If use other sripts or binaries
    ```
    ./mail_sender.py ./path/to/program
    ```
    
***P.S:***
***If desired, you can use mail-sender as a regular utility, installing it as well as programs from the source code :)***


***    
  
License
----

MIT©
