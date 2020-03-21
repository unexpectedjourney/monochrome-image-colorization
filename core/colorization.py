async def colorize_file(params):
    filename = params.get("filename")
    if not filename:
        return


    # part for image colorization
