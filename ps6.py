import string

def load_words(file_name):
    '''
    Loads a list of valid words from a file.

    File_name (string): the name of the file containing the list
    of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.
    '''
    print('Loading word list from file...')
    in_file = open(file_name, 'r')
    line = in_file.readline() # Read the first line of the file
    word_list = line.split() # Split the line into words
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise
    '''
    word = word.lower() # Convert the word to lowercase
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"") # Remove punctuation
    return word in word_list # Check if the word is valid

def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        shift_dict = {}
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase

        for i in range(26):
            shift_dict[lowercase[i]] = lowercase[(i + shift) % 26]
            shift_dict[uppercase[i]] = uppercase[(i + shift) % 26]

        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by the given shift.

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string)
        '''
        shift_dict = self.build_shift_dict(shift)
        encrypted_message = []

        for char in self.message_text:
            if char.isalpha():
                encrypted_message.append(shift_dict[char])
            else:
                encrypted_message.append(char)

        return ''.join(encrypted_message)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)
        '''
        #Initialize Message class with the text
        Message.__init__(self, text)

        #store the shift value
        self.shift = shift

        #Build the encryption dictionary using the shift
        self.encrypting_dict = self.build_shift_dict(shift)

        #Encrpyt the message text
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''Returns the shift value used for encryption'''
        return self.shift

    def get_encrypting_dict(self):
        '''Returns: a COPY of self.encrypting_dict'''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''Returns the encrypted message text'''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes the shift and updates the encryption'''
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypts the message by trying every possible shift value and finding the "best" one.
        The best shift is the one that results in the highest number of valid words in the message.
        It returns the shift and the decrypted message.

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift = None
        best_decrypted_text = None
        max_valid_words = 0

        # Try all possible shifts (from 0 to 25) to find the best one
        for shift in range(26):
            decrypted_text = self.apply_shift(26-shift) # Decrypt by applying the reverse shift
            words = decrypted_text.split() # Split the text into words
            valid_word_count = sum(1 for word in words if is_word(self.valid_words, word)) # Count valid words

            # If this shift hasmore valid words, update the best shift and the decrypted text
            if valid_word_count > max_valid_words:
                max_valid_words = valid_word_count
                best_shift = shift
                best_decrypted_text = decrypted_text

        # Return the best shift and the decrypted text
        return best_shift, best_decrypted_text

if __name__ == "__main__":
    #Example test case (PlaintextMessage)
    import os
    print(os.getcwd())
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #Decrypt the story (example)
    ciphertext = CiphertextMessage(get_story_string()) #Get encrypted story
    print('Actual Output:', ciphertext.decrypt_message())