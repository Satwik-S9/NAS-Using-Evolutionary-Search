def swap_mutation(model_genome):
  """
  Randomly choose two layers in the model genome and swap them
  """
  # creating list and its copies
  la = []
  la = model_genome.split(';')
  fl = "FL relu"
  la.remove("FL relu")
  la_copy = la[:]  
  # print(f"{la}\n{la_copy}")

  # choosing two indices at random
  choice1 = random.choice(la_copy)
  ### print(choice1)
  la_copy.remove(choice1)
  choice2 = random.choice(la_copy)

  index1, index2 = la.index(choice1), la.index(choice2)
  # swapping two layers in the genome
  la[index1], la[index2] = choice2, choice1  
  print(f"Swapping :\n{choice1}\n{choice2}")
  # print(la)
  
  swapped_genome = ";".join(la) + fl + ";"
  # print(swapped_genome)

  return swapped_genome

def inversion_mutation(model_genome):
  """
  Select a sequence of layers at random and invert them
  """
  la = []
  la = model_genome.split(';')
  fl = "FL relu"
  la.remove("FL relu")
  # main_str = ";".join(la)

  idx1 = random.randint(0, len(la)-2)
  idx2 = random.randint(idx1+1, len(la)-1)
  # substr = get_substring(main_str, substr_len)
  sa = la[idx1:idx2]
  print(f"{la}\n{fl}\n{idx1}\n{idx2}\n{sa}")
  
  sa = sa[::-1]
  la[idx1:idx2] = sa

  inverted_genome = ";".join(la) + fl + ";"

  return inverted_genome
