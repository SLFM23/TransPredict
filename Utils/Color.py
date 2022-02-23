class Color:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def bold(text):
        return Color.BOLD + text + Color.END

    @staticmethod
    def set_bold(text, bold = False):
        if bold:
            return Color.BOLD + text
        else:
            return text

    @staticmethod
    def green(text, bold = False):
        result = Color.set_bold(Color.GREEN + text, bold)

        return result + Color.END

    @staticmethod
    def blue(text, bold = False):
        result = Color.set_bold(Color.BLUE + text, bold)

        return result + Color.END

    @staticmethod
    def red(text, bold = False):
        result = Color.set_bold(Color.RED + text, bold)

        return result + Color.END