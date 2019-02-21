
Context managers for capturing C-level output::

    from wurlitzer import pipes

    with pipes() as (stdout, stderr):
        call_c_function()
    out = stdout.read()
    err = stderr.read()


