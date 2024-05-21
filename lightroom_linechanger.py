'''
MIT License

Copyright (c) [2024] [Christian Becker]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# lightroom_linechanger

def check_state(filename):
    global zeilenr
    zeilenr = 0
    index = 0
    orig = False

    search = r'"$$$/AgImportDialog/ShootArrangement_1/Template=%Y/%m-%d"'
    with open(filename, 'r') as file:
        data = file.read()
        data = data.split('\n')
   
    for zeile in data:
        if zeile != search:
            index = index + 1
        elif zeile == search:
            orig = True
            zeilenr = index
                
    if orig == True:
        # tu dinge
        print('Datei im Originalzustand!')
        print('Zeile: {}'.format(zeilenr))
        change_line(filename, zeilenr)
    elif orig == False:
        print('Datei schon modifiziert!')

def change_line(filename, zeilenr):
    old = r'"$$$/AgImportDialog/ShootArrangement_1/Template=%Y/%m-%d"'
    new = r'"$$$/AgImportDialog/ShootArrangement_1/Template=%B %Y"'
    data_old = []
    data_new = []
    with open(filename, 'r') as file:
        with open(filename, 'r') as file:
            data_old = file.read()
            data_old = data_old.split('\n')
    print(data_old[zeilenr])
    
    index = 0
    
    for zeile in data_old:
        if index != zeilenr:
            index = index + 1
            data_new.append(zeile)
        elif index == zeilenr:
            print('Ändere Zeile...')
            index = index + 1
            data_new.append(new)
    
    with open(filename, 'w') as file:
        for element in data_new:
            file.write(element + '\n')
    
    with open(filename, 'r') as file:
        data_check = file.read()
        data_check = data_check.split('\n')

    print(data_check[zeilenr])

check_state('C:\Program Files\Adobe\Adobe Lightroom Classic\Resources\de\TranslatedStrings_Lr_de_DE.txt')
