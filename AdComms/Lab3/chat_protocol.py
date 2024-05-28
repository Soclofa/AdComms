'''
Abraham Soclof 
ID: 674098915
Lab3/chat_protocol.py
'''

CHAT_SERVICE_READY = "01 Welcome to the chat server\r\n"
NAME = "01 Client Name"
GET_NAMES = "02 Client request for "
MSG = "02 Client has sent a message"
EXIT = "00 Client has left the chat"

'''Message of Format: MSG ClientName Message'''

'''

PORT = 1025 # First available socket for MAC OS

SMTP_SERVICE_READY = "220 Welcome to the SMTP server\r\n"
REQUESTED_ACTION_COMPLETED = "250 OK\r\n"
COMMAND_SYNTAX_ERROR = "500 Syntax error, command unrecognized\r\n"
INCORRECT_AUTH = "535 Authentication failed\r\n"
ENTER_MESSAGE = "354 End data with <CR><LF>.<CR><LF>\r\n"
AUTH_INPUT = "334 {}\r\n"  # Use this with base64 encoded prompts
AUTH_SUCCESS = "235 Authentication successful\r\n"
EMAIL_END = ".\r\n"  # Indicates the end of the email body
GOODBYE = "221 Bye\r\n"

'''