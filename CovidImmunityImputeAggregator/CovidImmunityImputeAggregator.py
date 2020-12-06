import os, sys, csv, math

path = '.'
outCSV = 'zzOUt.csv'

for fp in os.listdir(path):
    if (fp == outCSV):
        continue

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

        # check for argument
        if (not idx == 0):
            nheaders = ['species']
            nrows = []
            numArg = 1
            grabPrevious = False

            lastArg = sys.argv[-1]
            if (lastArg.startswith("n")):
                lastArg = lastArg[1:]
                grabPrevious = True

            try:
                tArg = int(lastArg)

                if (tArg >= 1):
                    numArg = int(round(tArg, 0))
            except ValueError:
                numArg = 1
                
            tnum = int(math.ceil(idx / numArg))

            for k in range(len(csvlines)):
                trow = [csvlines[k][0]]

                if (grabPrevious):
                    for l in range(idx - numArg, idx - 1):
                        trow.append(csvlines[k][l])
                        if (k == 0):
                                nheaders.append(csvheaders[l])
                elif (numArg > 1):
                    for l in range(tnum, idx - 2, tnum):
                        trow.append(csvlines[k][l])
                        if (k == 0):
                                nheaders.append(csvheaders[l])

                trow.append(csvlines[k][idx-1])
                trow.append(csvlines[k][idx])

                # add the temp row to the main array
                nrows.append(trow)

            # append the headers to the main array
            nheaders.append(csvheaders[idx-1])
            nheaders.append(csvheaders[idx])

            # write new csv file somewhere
            with open(outCSV, 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(nheaders)
                writer.writerows(nrows)
        else:
            print('NO MORE UNKNOWNS')
            with open(outCSV, 'w') as out_file:
                writer = csv.writer(out_file)

        # there should only be one csv file, quit loop
        break

print('Completed Run')