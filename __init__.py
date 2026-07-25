from calibre.customize import InterfaceActionBase


class FimfictionEbookPlugin(InterfaceActionBase):

    name = 'Fimfiction Ebook Plugin'
    version = (1, 0, 0)
    author = 'EveCouto'
    supported_platforms = ['windows']
    description = 'Allows for fixing images and merging updated epubs'
    minimum_calibre_version = (9, 11, 0)
