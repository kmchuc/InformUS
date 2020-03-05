class TrieNode():

    def __init__(self):

        # initializing one node for trie
        self.children = {}
        self.last = False

class Trie():

    def __init__(self):

        # initializing the trie structure
        self.root = TrieNode()
        self.party_list = []

    def formTrie(self, keys):

        # forms trie structure with given set of strings
        # if it doesn't already exist it merges the key into it by extending the structure
        for key in keys:
            # inserting key into the trie
            self.insert(key)
    
    def insert(self, key):
        # inserts key into trie if it doesn't exist
        # if key is prefix of trie node, mark as lead node
        node = self.root

        for a in list(key):
            if not node.children.get(a):
                node.children[a] = TrieNode()
            
            node = node.children[a]

        node.last = True

    def search(self, key):

        # searches for the given key in the trie for a full word match and returns True or else returns False
        node = self.root
        found = True
        
        for a in list(key):
            if not node.children.get(a):
                found = False
                break

            node = node.children[a]
        return node and node.last and found

    def suggestionsRec(self, node, word):

        # method to recursively traverse the trie and return a whole word
        if node.last:
            self.word_list.append(word)
        
        for a,n in node.children.items():
            self.suggestionsRec(n, word + a)
    
    def printAutoSuggestions(self, key):

        # returns all words in the trie whose common prefix is the given key thus listing out all the suggestions for autocomplete
        node = self.root
        not_found = False
        temp_word = ''

        for a in list(key):
            if not node.children.get(a):
                not_found = True
                break

            temp_word += a
            node = node.children[a]
        
        if not_found:
            return 0

        elif node.last and not node.children:
            return -1
        
        self.suggestionsRec(node, temp_word)

        for s in self.word_list:
            print(s)
        
        return 1

# driver code
keys = ["Ace Party", "Alaskan Independence Party", "American Independence Conservative", "American Independent Party", "American Party", "American People's Freedom Party", "Americans Elect", "Citizen's Party", "Commandments Party", "Commonwealth Party of the U.S.", "Communist Party", "Concerned Citizens Party Of Connecticut", "Constitution Party", "Constitutional", "Country", "D.C. Statehood Green Party", "Democratic-Nonpartisan League", "Democratic Party", "Democratic/Conservative", "Democratic-Farmer-Labor", "Desert Green Party", "Federalist", "Freedom Labor Party", "Freedom Party", "George Wallace Party", "Grassroots", "Green Party", "Green-Rainbow", "Human Rights Party", "Independence Party", "Independent", "Independent American Party", "Independent Conservative Democratic", "Independent Green", "Independent Party of Delaware", "Industrial Government Party", "Jewish/Christian National", "Justice Party", "La Raza Unida", "Labor Party", "Less Federal Taxes", "Liberal Party", "Libertarian Party", "Liberty Union Party", "Mountain Party", "National Democratic Party", "Natural Law Party", "New Alliance", "New Jersey Conservative Party", "New Progressive Party", "No Party Affiliation", "No Party Preference", "None", "Nonpartisan", "Non-Party", "One Earth Party", "Other", "Pacific Green", "Party for Socialism and Libertarian", "Peace and Freedom", "Peace and Freedom Party", "People Over Politics", "People's Party", "Personal Choice Party", "Popular Democratic Party", "Progressive Party", "Prohibition Party", "Puerto Rican Independence Party", "Raza Unida Party", "Reform Party", "Republican Party", "Resource Party", "Right To Life", "Socialist Equality Party", "Socialist Labor Party", "Socialist Party", "Socialist Party U.S.A.", "Socialist Workers Party", "Taxpayers", "Taxpayers Without Representation", "Tea Party", "Theo-Democratic", "U.S. Labor Party", "U.S. Taxpayers Party", "Unaffiliated", "United Citizen", "United Party", "Unknown", "Veterans Party", "We The People", "Write-In"]

# key for autocomplete suggestions
key = "hel"
status = ["Not found", "Found"]

# creats trie object
t = Trie()

# creating the trie structure with the given set of strings
t.formTrie(keys)

# autocompleting the given key using our trie structure
comp = t.printAutoSuggestions(key)

if comp == -1:
    print("No other strings found with this prefix\n")
elif comp == 0:
    print("No string found with this prefix\n")
