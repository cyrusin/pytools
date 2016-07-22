PyTools
================
Include some useful tools implemented by Python. 


Details
----------------------------
- trans_to_flash.py: 

    >Transfer *.txt, *.doc, *.pdf, *.odt to .swf whether the document is encoding in UTF-8 or GB18030
    >Install openoffice\unoconv\swftools on your *nix first

- url_fetch.py & url_fetch_mq.py:

    >Tool used to fetch web page
    >Using multi-threading

- file_processing.py:

    >Module used to process file fast
    >Implemented with coroutine and yield expression

- oop_utils.py:

    >Module used to implement your idea in OOP

- iter_tools.py:
    >Some useful tools based on python's itertools mobule

- str_util.py
    >Some useful tools in manipulation of str

- echo_server_select.py
    >An echo server based on select
    >
    >Run it with "python echo_server_select.py"
    >
    >Connect it with tcp like "telnet 127.0.0.1 8080"

- echo_server_poll.py
    >An echo server based on poll
    >
    >Run it with "python echo_server_poll.py <host:port>"
    >
    >Connect it with tcp like "telnet 127.0.0.1:8080"
    >
    >Send "End" if you want to close the connection

- echo_server_epoll.py
    >An echo server based on epoll
    >
    >Run it with "python echo_server_epoll.py <host:port>"
    >
    >Connect it with tcp like "telnet 127.0.0.1:8080"
    >
    >Send "End" if you want to close the connection

- thread_util.py
    >Useful tools for threading

- priorityQ.py
    >A simple priority queue 

- echo_server_greenlet.py
    >A echo server used greenlet, also a template of how to implement a server using greenlet without to many callbacks
