import calculatorTools

try:
    calculatorTools.load_from_log()
except FileNotFoundError:
    print("no files found - have you run letsplay?")