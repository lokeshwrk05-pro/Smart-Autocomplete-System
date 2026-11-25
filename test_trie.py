from trie import Trie

trie = Trie()

trie.insert("program")
trie.insert("programmer")
trie.insert("programming")
trie.insert("progress")
trie.insert("project")
trie.insert("python")

print("Suggestions for 'prog':")
print(trie.get_suggestions("prog"))

print("\nSuggestions for 'pro':")
print(trie.get_suggestions("pro"))

print("\nSuggestions for 'xyz':")
print(trie.get_suggestions("xyz"))