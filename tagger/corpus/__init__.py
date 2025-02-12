from photoviewer.utils import read_file


def content_to_list(content):
    """
    Convert content to a list of lines.
    """
    return content.strip().split("\n")

# Spanish
ES_ITEMS = content_to_list(read_file("tagger/corpus/ES/items.txt"))
ES_DESCRIPTIONS = content_to_list(read_file("tagger/corpus/ES/descriptions.txt"))
ES_LABELS = ES_ITEMS + ES_DESCRIPTIONS

# English
EN_ITEMS = content_to_list(read_file("tagger/corpus/EN/items.txt"))
EN_DESCRIPTIONS = content_to_list(read_file("tagger/corpus/EN/descriptions.txt"))
EN_LABELS = EN_ITEMS + EN_DESCRIPTIONS
