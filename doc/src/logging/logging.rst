Developer Notes
===============

Logging
-------

Since this is a library, there default expected behavior is to *not* produce any kind of extra logging noise. This should be convenient for the library user. However, for effective development of this library itself, it should be possible to quickly enable library logging when required.

Why is logging disabled?
........................

Logging is disabled because this is the expected practice for a Python library. For a more in-depth explanation, see [logging_howto]_ or [logging_library]_.

.. [logging_howto] https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
.. [logging_library] https://docs.python-guide.org/writing/logging/#logging-in-a-library

How to enable logging in REPL?
..............................

.. code-block:: python

   from cat.log import enable_logging
   enable_logging()

How to enable logging when running pytest?
..........................................

Note that there is a custom command line argument for :code:`pytest` that enables logging (:code:`--enable-logging`). However, since :code:`pytest` also does input capturing (i.e. does not show the results of any print/logging statements by default), then you would also need to disable input capturing with :code:`--capture=no`

.. code-block:: bash

   pytest test/factorize/test_fermat.py --enable-logging --capture=no

How to use logging in code?
...........................

.. code-block:: python

   import logging
   from cat.log import enable_logging

   def foo():
       logger = logging.getLogger('cat')
       logger.info('Hello, logging world!')

   if __name__ == '__main__':
       enable_logging()
       foo()
