



import os, sys, inspect

# ensure pyeq2 can be imported
if -1 != sys.path[0].find('pyeq2-read-only'):raise Exception('Please rename SVN checkout directory from "pyeq2-read-only" to "pyeq2"')
exampleFileDirectory = sys.path[0][:sys.path[0].rfind(os.sep)]
pyeq2IimportDirectory =  os.path.join(os.path.join(exampleFileDirectory, '..'), '..')
if pyeq2IimportDirectory not in sys.path:
    sys.path.append(pyeq2IimportDirectory)
    
    import pyeq2


# see IModel.fittingTargetDictionary
equation = pyeq2.Models_3D.BioScience.HighLowAffinityIsotopeDisplacement('SSQABS')

pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(equation.exampleData, equation, False)


# Note that all coefficients are set with estimated values
equation.estimatedCoefficients = [2.0, 3.0E13]


equation.Solve()


##########################################################


print(equation.GetDisplayName(), str(equation.GetDimensionality()) + "D")
print(equation.fittingTargetDictionary[equation.fittingTarget], '=', equation.CalculateAllDataFittingTarget(equation.solvedCoefficients))
print("Fitted Parameters:")
for i in range(len(equation.solvedCoefficients)):
    print("    %s = %-.16E" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i]))
