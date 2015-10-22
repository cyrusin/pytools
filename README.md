PyTools
================
Include some useful tools implemented by Python. 


Details
----------------------------
- trans_to_flash.py: 

    >transfer *.txt, *.doc, *.pdf, *.odt to .swf whether the document is encoding in UTF-8 or GB18030.
    >Install openoffice\unoconv\swftools on your *nix first.

- url_fetch.py & url_fetch_mq.py:

    >tool used to fetch web page.   
    >Using multi-threading.

- file_processing.py:

    >Module used to process file fast.
    >Implemented with coroutine and yield expression.

- oop_utils.py:

    >Module used to implement your idea in OOP.

- iter_tools.py:
    >some useful tools based on python's itertools mobule.

- str_util.py
    >some useful tools in manipulation of str.

- echo_server_select.py
    >an echo server based on select
    >run it with "python echo_server_select.py"
    >connect it with tcp like "telnet 127.0.0.1 8080"

- echo_server_poll.py
    >an echo server based on poll
    >run it with "python echo_server_poll.py <host:port>"
    >connect it with tcp like "telnet 127.0.0.1:8080"
    >send "End" if you want to close the connection

- echo_server_epoll.py
    >an echo server based on epoll
    >run it with "python echo_server_epoll.py <host:port>"
    >connect it with tcp like "telnet 127.0.0.1:8080"
    >send "End" if you want to close the connection
