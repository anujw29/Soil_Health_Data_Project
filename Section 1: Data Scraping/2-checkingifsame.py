# When I manually downloaded CSVs by selecting the Micronutrient option and Macronutrient option for various files, I found out that in both 
# cases I am getting the same file which is basically a combined CSV with columns of Macro and Micro both.
#So I didnt keep any option to click on macro and micro button in the webscrape_final.py code


#Used ChatGPT to write this basic code
file1 = r"C:\Users\anujw\Downloads\baksa 24-25 macro.csv"
file2 = r"C:\Users\anujw\Downloads\baksa 24-25 micro.csv"
def same_files(f1, f2):
    with open(f1, 'rb') as file1, open(f2, 'rb') as file2:
        while True:
            b1 = file1.read(4096)
            b2 = file2.read(4096)
            if b1 != b2:
                return False
            if not b1: 
                return True

result = same_files(file1, file2)
print("Files are same." if result else "Files are different.")



