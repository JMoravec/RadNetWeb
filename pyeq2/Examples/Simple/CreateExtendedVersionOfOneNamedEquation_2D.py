



import os, sys, inspect

# ensure pyeq2 can be imported
if -1 != sys.path[0].find('pyeq2-read-only'):raise Exception('Please rename SVN checkout directory from "pyeq2-read-only" to "pyeq2"')
exampleFileDirectory = sys.path[0][:sys.path[0].rfind(os.sep)]
pyeq2IimportDirectory =  os.path.join(os.path.join(exampleFileDirectory, '..'), '..')
if pyeq2IimportDirectory not in sys.path:
    sys.path.append(pyeq2IimportDirectory)
    
    import pyeq2


# print all possible extended version names
print("List of all possible extended version names")
for extendedVersionName in pyeq2.ExtendedVersionHandlers.extendedVersionHandlerNameList:
    print(extendedVersionName)
    
print()

# create an extended version of one equation
equation = pyeq2.Models_2D.BioScience.HyperbolicLogistic('SSQABS', 'InverseWithOffset')

# note that the extended version name can contain spaces
equation = pyeq2.Models_2D.BioScience.HyperbolicLogistic('SSQABS', 'Inverse With Offset')

print("Instantiated", equation.GetDisplayName())

print()

#print("This should raise an exception")
#equation = pyeq2.Models_2D.BioScience.HyperbolicLogistic('SSQABS', 'Bad Extended Version Name')
