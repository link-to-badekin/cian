






def create_unique_pdf(name, newfile):
	global path_to
	if os.path.exists(path_to + '/pdf/'+name+'.pdf'):
		index = name.find('((')
		if index == -1:
			name = name + '((' + str(1) + '))'
		else:
			сopy_num = int(name[index:-2])
			name = name + '((' + str(copy_num+1) + '))'
	newfile.write(path_to + '/pdf/'+name+'.pdf')

line = 'my name'
i = 0
while i < 10 :
	index = line.find('((')
	if index == -1:
		line = line + '((' + str(1) + '))'
	else:
		num = int(line[index+2:-2])
		line = line[:index] + '((' + str( num +1) + '))'
	print(line)
	i = i+1

