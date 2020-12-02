import os, sys, csv

path = '.'

for fp in os.listdir(path):
    if (fp.endswith('csv')):
        csvlines = []
        csvheaders = []
        tablines = []
        tabheaders = []

        with open(fp, 'r') as file:
            reader = csv.reader(file)
            for idx,line in enumerate(reader):
                if (idx == 0):
                    csvheaders = line
                elif (not line):
                    continue
                else:
                    csvlines.append(line)

        for ofp in os.listdir(path):
            if (ofp.endswith('txt')):
                with open(ofp, 'r') as file:
                    tabs = csv.reader(file, delimiter = ' ')
                    for idx,line in enumerate(tabs):
                        line = list(filter(None, line))
                        if (idx == 0):
                            tabheaders = line
                        elif (not line):
                            continue
                        else:
                            tablines.append(line)

                # there should only be one txt file, quit loop
                os.remove(ofp)
                break

        # replace column here and write the file back
        if (not tabheaders == []):
            spot = tabheaders[-1]
            for i in range(1, len(csvlines)):
                csvlines[i][int(spot[1:])] = tablines[i][len(tabheaders)]

            with open(fp, 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(csvheaders)
                for k in range(len(csvlines)):
                    writer.writerow(csvlines[k])

        # find next column index where value is N/A
        idx = 0
        for i in range(len(csvlines[0])):
            for j in range(len(csvlines)):
                if (csvlines[j][i] == 'NA'):
                    idx = i
                    break
            if (not idx == 0):
                    break

        # write new csv file somewhere
        if (not idx == 0):
            with open('zzOut.csv', 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(('species', csvheaders[idx-1], csvheaders[idx]))
                for k in range(len(csvlines)):
                    writer.writerow((csvlines[k][0], csvlines[k][idx-1], csvlines[k][idx]))
        else:
            print('NO MORE UNKNOWNS')
            with open('out\log.csv', 'w') as out_file:
                writer = csv.writer(out_file)

        # there should only be one csv file, quit loop
        break

print('Completed Run')