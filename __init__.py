from calibre import EditBookToolPlugin


class FimfictionEbookPlugin(EditBookToolPlugin):

    name = 'Fimfiction Ebook Plugin'
    version = (1, 0, 0)
    author = 'EveCouto'
    supported_platforms = ['windows']
    description = 'Allows for fixing images and merging updated epubs'
    minimum_calibre_version = (1, 46, 0)
