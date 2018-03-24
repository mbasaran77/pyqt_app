import gettext

_ = gettext.gettext

tr_on = True

if tr_on:
    tr = gettext.translation('lingual', localedir='locale', languages=['TR'])
    tr.install()

    _ = tr.gettext
def print_some_strings():
    print(_("Hello world"))
    print(_("This is a translatable string"))


if __name__ == '__main__':
    print_some_strings()
