import misc

def echo(stuff):
    print("This version of echo ignores what you tell it to do.")

print()
print("====================================================")
echo(" I'm calling a function from a different module!")
print("====================================================")    

print()
print("=================================================")
misc.echo(" I'm calling a function from a different module!")
print("=================================================")

print()
print(type(misc))