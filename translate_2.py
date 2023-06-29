from PyDictionary import PyDictionary

dictionary = PyDictionary()

word = "example"  # слово, которое нужно перевести

# получаем полный перевод слова
meaning = dictionary.meaning(word)

# выводим описание каждого значения слова
for key in meaning:
    print(f"{key}:")
    for value in meaning[key]:
        print(f"- {value}")

# выводим примеры использования слова
print("Examples:")
examples = dictionary.synonym(word)
for example in examples:
    print(f"- {example}")
