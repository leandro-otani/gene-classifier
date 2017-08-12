import csv
import collections
import arff
import itertools
import numpy as np
import pandas as pd
import scipy.stats as st

class DataPreProcessing:
    #extracao da planilha de dados
    def extractData(self, inputFile, classes):
        pp5 = [] # lista de tuplas contendo rotulo e conteudo
        cleansedSet = []
        rawset = csv.reader(open(inputFile))
        thresholdSet = []
        #threshold
        for column in rawset:
            maxVal = 0
            minVal = float('inf')
            tempColumn = column
            for index, value in enumerate(tempColumn[1:]):
                tempVal = int(value)
                if tempVal < 20:
                    tempColumn[index+1] = 20
                elif tempVal > 16000:
                    tempColumn[index+1] = 16000
            thresholdSet.append(tempColumn)

        #Fold difference
        for column in thresholdSet:
            maxVal = 0
            minVal = float('inf')
            for value in column[1:]:
                tempVal = int(value)
                if tempVal > maxVal:
                    maxVal = tempVal
                if tempVal < minVal:
                    minVal = tempVal

            if (maxVal - minVal)/2 >= 2:
            # if (maxVal - minVal) > 200 and (maxVal/minVal) > 2:
                cleansedSet.append(column)

        # print len(cleansedSet)

        classes = self.retrieveClasses("pp5i_train_class.txt")

        cleansedSet.append(classes)

        # print cleansedSet


        df = pd.DataFrame(cleansedSet[1:])
        df.to_csv('./clean-dataset.csv', index=False, header=False)

        a = itertools.izip(*csv.reader(open("./clean-dataset.csv", "rb")))
        csv.writer(open("./train-transposed.csv", "wb")).writerows(a)

        dadosLimpos = pd.read_csv('./train-transposed.csv');
        genes = dadosLimpos.columns[:-1]
        classes = pd.Series(dadosLimpos['class'].values.ravel()).unique()


        genesTvalues = {}
        for classe in classes:
            tgenes = []
            for gene in genes:
                sample1 = dadosLimpos[dadosLimpos['class'] == classe][gene]
                sample2 = dadosLimpos[dadosLimpos['class'] != classe][gene]
                t = st.ttest_ind(sample1,sample2,equal_var=False)
                tgenes.append(t[0])
            genesTvalues[classe] = pd.Series(tgenes,index=genes)
        genesTvaluesDf = pd.DataFrame(genesTvalues)

        print genesTvalues

        # columnSet = zip(cleansedSet)[1:]
        # for column in columnSet:
        #     label = classes[int(column[0])-1]
        #     mutableTuple = [label]
        #     mutableTuple += [float(value) for value in list(column)[1:]]
        #     cleanseData()
        #     pp5.append(mutableTuple)

        return pp5

    #separa rotulos dos dados e devolve lista contendo (rotulo, conteudo)
    def collectLabels(self, extractedData):
        dataValues = ["class"]
        dataValues += ['at' + str(index+1) for index in range(7070)]
        return dataValues #[(labels[index],extractedData[index]) for index in range(1,len(extractedData) - 2)]

    def retrieveClasses(self, inputFileWithClasses):
        with open(inputFileWithClasses, 'rb') as f_in:
            header = ["class"]
            content = f_in.read()
            content = str(content).replace("\r", " ").replace('\n', '\n') #removendo caracteres inuteis
            content = content.split('\n') #separa linhas
            return (header + content[1:len(content) - 1])


if __name__ == "__main__":
    dataPre = DataPreProcessing();
    classes = dataPre.retrieveClasses("pp5i_train_class.txt") # rotulos de cada coluna
    dataTraining = dataPre.extractData("pp5i_train.gr.csv", classes)
    # dataTest = dataPre.extractData("pp5i_test.gr.csv")
    labeledDataTraining = dataPre.collectLabels(dataTraining) #conjunto de treinamento
    # print labeledDataTraining
    # labeledDataTest = dataPre.collectLabels(dataTest) # conjunto de teste

    arff.dump('result.arff', dataTraining, relation="GenicExpression", names= labeledDataTraining)
