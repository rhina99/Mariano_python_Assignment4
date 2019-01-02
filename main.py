


import string

### DO NOT MODIFY THIS FUNCTION ###
def read_word_list(file_name):
    '''
    file_name (str): the name of the file containing the list of words
    to load.
    
    Returns: a set of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    try:
        in_file = open(file_name, 'r') # in_file: file
        line = in_file.readline()      # line: str
        word_list = line.split()       # word_list: list of str
        in_file.close()
    except IOError:
        print("Unable to read:", file_name)
        word_list = []
    return set(word_list)

### DO NOT MODIFY THIS FUNCTION ###
def read_message_string(file_name):
    """
    Returns: a possibly profound message in encrypted text.
    """
    try:
        in_file = open(file_name, "r")
        message = str(in_file.read())
        in_file.close()
    except IOError:
        print("Unable to read: ", file_name)
        message = ""
    return message

WORDLIST_FILENAME = 'words.txt'
class message(object):
    N_LETTERS = len(string.ascii_lowercase)
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a message object
                
        text (str): the message's text

        a message object has one attribute:
            self.message_text (str, determined by input text)
        '''
        self.message_text = text

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### IMPLEMENT THIS METHOD
    def create_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (int): the amount by which to shift every letter of the 
        alphabet, 0 <= shift < 26.

        Returns: a dictionary mapping a letter (str) to another
                 letter (str), for all lower and upper case letters.
        '''

        x = list(string.ascii_lowercase) #list of lower alphabets
        y = list(string.ascii_uppercase) #list of upper alphabets
        lower = x.copy() #make a list of lower alphabets which the order is going to change after "shift"
        upper = y.copy() #make a list of upper alphabets which the order is going to change after "shift"

        for item in lower[:shift]:
            lower.append(item)
        del lower[:shift]

        for item in upper[:shift]:
            upper.append(item)
        del upper[:shift]

        Lkey = x
        Lvalue = lower
        Ukey = y
        Uvalue = upper

        d = dict(zip(Lkey, Lvalue))
        d2 = dict(zip(Ukey, Uvalue))
        d.update(d2)
        return d    #make 26 dictionaries with each values shifted 26 times.

    ### IMPLEMENT THIS METHOD
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        shift (int): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (str) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dic = self.create_shift_dict(shift)
        result = []
        for key in self.message_text:
            if key in shift_dict:
                alt = shift_dic[key]
            else:
                alt = key
            result.append(alt)

        return "".join(result)


class plaintext_message(message):
    ### IMPLEMENT THIS METHOD ###
    def __init__(self, text, shift):
        '''
        Initializes a plaintext_message object        
        
        text (str): the message's text
        shift (int): the shift associated with this message

        A plaintext_message object inherits from message and has 5 attributes:
            self.message_text (str, determined by input text)
            self.shift (int, determined by input shift)
            self.message_text_encrypted (str, created using shift)

        Hint: consider using the parent class constructor and the 
        set_shift method so no code is repeated.
        '''
        super().__init__(text)   #by using super(9, we can initialize the parent class (class message)'s objects.
        self.set_shift(shift)
        

    ### DO NOT MODIFY THIS METHOD ###
    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    ### DO NOT MODIFY THIS METHOD ###
    def set_shift(self, shift):
        '''
        Changes self.shift of the plaintext_message and updates other 
        attributes determined by shift (ie. message_text_encrypted).
        
        shift (int): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.message_text_encrypted = self.apply_shift(shift)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted


class ciphertext_message(message):
    ### IMPLEMENT THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a ciphertext_message object
                
        text (str): the message's text

        a ciphertext_message object has two attributes:
            self.message_text (str, determined by input text)
            self.valid_words (set, determined using read_word_list())
        '''
        self.message_text = text
        self.valid_words = read_word_list(WORDLIST_FILENAME)


    ### DO NOT MODIFY THIS METHOD ###
    def is_word(self, word):
        '''
        Determines if word is a valid word, ignoring
        capitalization and punctuation
        
        word (str): a possible word.
    
        Returns: True if word is in word_list, False otherwise

        Example:
        >>> ciphertext.is_word('bat') returns
        True
        >>> ciphertext.is_word('asdf') returns
        False
        '''
        garbage = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""
        return word.strip(garbage).lower() in self.valid_words

    
    ### IMPLEMENT THIS METHOD ###
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value.
        '''

        #We find the same word that matches both in the text and in the world list, then we count the word in text list that are most used(matched) in the word list.
        #Since we have max 26 of shifts, we have 26 trials to find a maximum matched word count.
        #We set one of the trial that had a maximum of matched word count in text as a best shift
        best_shift = 0
        best_message_text = ""
        max_count = 0
        
        for shift in range(1, self.N_LETTERS):
            decrypted_message = self.apply_shift(shift)
            decrypted_m_lst = decrypted_message.split()

            match_count = 0
            for decrypted_word in decrypted_m_lst:
                if self.is_word(decrypted_word) == True: #if word in decrypted word matches with the word in word list that was brought from the is_word() function, we counts match_count.
                    match_count += 1
            if max_count < match_count:
                max_count = match_count
                best_shift = shift
                best_decrypted_message = decrypted_message

        return (best_shift, best_decrypted_message)
            

# DO NOT CHANGE ANY CODE AFTER THIS LINE!!

# Unit test - just verify that create_shift_dict is properly implemented.

message = message("Hello, World!")
print("*** create_shift_dict:", end=" ")
n_errors = 0
for i in range(1, message.N_LETTERS):
    shift_dict = message.create_shift_dict(i)
    assert len(shift_dict) == message.N_LETTERS * 2
    for key in shift_dict:
        alt = shift_dict[key]
        if key.isupper():
            base = ord('A')
        elif key.islower():
            base = ord('a')
        org = chr(((ord(key) - base) + i) % message.N_LETTERS + base)
        if alt != org:
            n_errors += 1

if n_errors != 0:
    print("FAILED")
else:
    print("PASSED")
assert n_errors == 0

# Unit test - verify that apply_shift is properly implemented.
print("*** apply_shift:", end=' ')
result = message.apply_shift(1)
if result != 'Ifmmp, Xpsme!':
    print("FAILED")
else:
    print("PASSED")

# Integration test case (plaintext_message)

plaintext = plaintext_message('Hello', 2)
print('Expected Output: Jgnnq', end=' ')
print('Actual Output:', plaintext.get_message_text_encrypted())
assert 'Jgnnq' == plaintext.get_message_text_encrypted()

# Integration test case (ciphertext_message)

ciphertext = ciphertext_message('Jgnnq')
print('Expected Output:', (24, 'Hello'), end = ' ')
print('Actual Output:', ciphertext.decrypt_message())
assert (24, 'Hello') == ciphertext.decrypt_message()

# Actually try to decode the message.

ciphertext = ciphertext_message(read_message_string("message.txt"))
result = ciphertext.decrypt_message()
print("Best shift:", result[0])
print(result[1])
