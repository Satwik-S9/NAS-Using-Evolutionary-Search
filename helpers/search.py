# mutation class containg four different types of mutations.
class Mutation():

  def swap_mutation(self,model_genome):
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

  def inversion_mutation(self,model_genome):
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

  def add_layer_mutation(self,model_genome):
    """
    choose a layers in the model genome and replace them by new layer
    """
    layer1 = []
    layer2 = random_layer(function,filters,kernels,af,"NC")
    layer2 = layer2.split(";")
    print(layer2)
    layer1 = model_genome.split(';') 
    genome = ''
    for i in range(len(layer1)-3):
      if layer1[i][:2] == "NC":
        layer1[i]=layer2[0]
        break
    for i in range(len(layer1)-1):
      genome+=layer1[i]+";"
    print(layer1)
    print(layer2)
    print(genome)
    return genome 
  
  def filter_mutation(self,model_genome):
    """
    Choose a layer in the model genome and change the number of filters in them
    """
    layer1 = model_genome.split(';')
    layer3 = []
    genome = ''
    for i in range(len(layer1)):
      if layer1[i][:2]=="NC":
        s = ''
        b = random.randint(0,len(filters)-1)
        layer2 = layer1[i].split(" ")
        if layer2[1]==filters[b]:
          b = random.randint(0,len(filters)-1)
        layer2[1]=filters[b]
        print(layer2[1])
        for j in range(len(layer2)):
          if j != len(layer2)-1:
            s = s + layer2[j]+" "
          else:
            s = s + layer2[j]
        print(s)
        layer3.append(s)
      else:
        layer3.append(layer1[i])
    for i in range(len(layer3)-1):
      genome+=layer3[i]+";"
    print(layer3)
    return genome
    
# defining the class of algorithm
class Evolutionary_algorithm():

  def __init__(self,p,layers):
    self.p = p
    self.layers = layers
    self.population = []
    self.history = []
    self.accuracy = []

  # initialize population
  def initialise(self):
    for i in range(self.p):
      x = random_architecture(self.layers)
      if x not in self.population:
        r = train_model(x, verbose=2, lr=1e-3, lr_decay=0.1)
        self.population.append(x)
        self.history.append(x)
        self.accuracy.append(r)
    return self.population,self.accuracy,self.history

  def search(self,nsamples, mutation:str = 'filter'):
    # running initial algorithm
    while True:
      samples = []
      for i in range(nsamples):
        a = random.randint(0,len(self.population)-1)
        if self.population[a] not in samples:
          samples.append([self.population[a],self.accuracy[a]])
      max1,max2 = 0,0
      j,k = 0,0
      for i in range(len(samples)):
        if samples[i][1][0]>max1:
          max2 = max1
          max1 = samples[i][1][0]
          k = j
          j = i
      print("Architecture having Highest accuracy in samples:\n",samples[j])
      print("Architecture having Second highest accuracy in samples:\n",samples[k])
      if max1>0.75:
        return samples[j],self.population,self.accuracy,self.history
      
      # mutating the genome
      m = Mutation()
      if mutation == 'filter':
        new_ge = m.filter_mutation(samples[j][0])
      elif mutation == 'swap':
        new_ge = m.swap_mutation(samples[j][0])
      elif mutation == 'inversion':
        new_ge = m.inversion_mutation(samples[j][0])
      elif mutation == 'addl':
        new_ge = m.add_layer_mutation(samples[j][0])
      print(new_ge)

      # training model on the mutated genome
      if new_ge not in self.population and mutation != 'swap':
        r = train_model(new_ge, verbose=2, lr=1e-3, lr_decay=0.1)
        if r[0]-samples[j][1][0]>0:
          print("Mutation accuracy is greater than parent adding child to population")
          self.population.append(new_ge)
          self.history.append(new_ge)
          self.accuracy.append(r)
        elif new_ge not in self.population and mutation != 'swap':
          try:
            r = train_model(new_ge, verbose=2, lr=1e-3, lr_decay=0.1)
          except Exception as e:
            continue
          if r[0]-samples[j][1][0]>0:
            print("Mutation accuracy is greater than parent adding child to population")
            self.population.append(new_ge)
            self.history.append(new_ge)
            self.accuracy.append(r)
        else:
          print("Mutation accuracy is less than parent not adding child to population")

