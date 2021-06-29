def get_characters_and_their_unicode_by_range():
    # https://stackoverflow.com/a/7001371/7639845
    def char_range(c1, c2):
        """Generates the characters from `c1` to `c2`, inclusive."""
        for c in range(ord(c1), ord(c2)+1):
            yield c, chr(c)

    print("----------------get_characters_and_their_unicode_by_range---------------------------")
    print([value for value in char_range("A", "Z")])
    print([value for value in char_range("a", "z")])


def get_characters_and_their_index_range():
    print("----------------get_characters_and_their_index_range---------------------------")
    from string import ascii_letters

    def range_alpha(start_letter, end_letter):
      return ascii_letters[
        ascii_letters.index(start_letter):ascii_letters.index(end_letter) + 1
    ]

    print('range: a-z: ', range_alpha('a', 'z'))
    print('range: A-Z: ', range_alpha('A', 'Z'))
    print('range: a-Z: ', range_alpha('a', 'Z'))
    print('range: b-C: ', range_alpha('b', 'C'))
    

def list_all_characters():
    print("----------------list_all_characters---------------------------")
    import string
    print('lowercase chars: ', string.ascii_lowercase)
    print('lowercase len:   ', len(string.ascii_lowercase))
    print('exists attributes: ', string.__all__)

if __name__ == '__main__':
    get_characters_and_their_unicode_by_range()
    get_characters_and_their_index_range()
    list_all_characters()
    