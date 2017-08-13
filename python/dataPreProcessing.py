# -*- coding: UTF-8 -*-
import csv
import collections
import arff
import itertools
import numpy as np
import pandas as pd
import scipy.stats as st


class DataPreProcessing:


    def extractTrain(self, inputFile, classes):
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
        genes = dadosLimpos.columns[:-1] #nome dos genes
        classList = pd.Series(dadosLimpos['Class'].values.ravel()).unique() #só para pegar o nome das classes


        genesTvalues = {}
        for className in classList:
            tgenes = []
            for gene in genes:
                sample1 = dadosLimpos[dadosLimpos['Class'] == className][gene]
                sample2 = dadosLimpos[dadosLimpos['Class'] != className][gene]
                t = st.ttest_ind(sample1,sample2,equal_var=False)
                tgenes.append(t[0]) #achamos que é um valor resultante
            genesTvalues[className] = pd.Series(tgenes,index=genes) #achamos que é o bind dos valores p/ o gene
        genesTvaluesDf = pd.DataFrame(genesTvalues) #exibe o conteúdo numa estrutura tabular

        subsets = [15]

        for setSize in subsets:
            topArray = []
            for className in classList:
                topArray.append(genesTvaluesDf.sort_values(className, ascending=False).index[:setSize])

            topGenes = list(set(topArray[0]) | set(topArray[1]) | set(topArray[2]) | set(topArray[3]) | set(topArray[4]))

            topGenes.append('Class')

            trainTopN = dadosLimpos[topGenes]
            print trainTopN
            # sortedTrainTopN =  trainTopN.reindex(np.random.permutation(trainTopN.index))
            trainTopN.to_csv('./train_top' + str(setSize) + '.csv', index=False)

    #extracao da planilha de dados
    def extractData(self, inputFile, classes):
        pp5 = [] # lista de tuplas contendo rotulo e conteudo
        cleansedSet = []
        rawset = pd.read_csv(inputFile)
        thresholdSet = []
        baseSet = []

        dadosTeste = rawset.transpose()
        newColumns = dadosTeste[:1]
        dadosTeste.columns = newColumns.values.flat;
        dadosTeste = dadosTeste.drop("SNO")
        print dadosTeste

        #threshold
        # for column in rawset:
        #     maxVal = 0
        #     minVal = float('inf')
        #     tempColumn = column
        #     for index, value in enumerate(tempColumn[1:]):
        #         tempVal = int(value)
        #         if tempVal < 20:
        #             tempColumn[index+1] = 20
        #         elif tempVal > 16000:
        #             tempColumn[index+1] = 16000
        #     thresholdSet.append(tempColumn)
        #
        #Fold difference

        dadosTesteThreshold = dadosTeste.clip(upper=16000, lower=20)
        dadosTesteLimpos =  dadosTesteThreshold.loc[:,(dadosTesteThreshold.max(axis=0) - dadosTesteThreshold.min(axis=0)) > 2]

        # for column in thresholdSet:
        #     maxVal = 0
        #     minVal = float('inf')
        #     for value in column[1:]:
        #         tempVal = int(value)
        #         if tempVal > maxVal:
        #             maxVal = tempVal
        #         if tempVal < minVal:
        #             minVal = tempVal
        #
        #     if (maxVal - minVal)/2 >= 2:
        #     # if (maxVal - minVal) > 200 and (maxVal/minVal) > 2:
        #         cleansedSet.append(column)

        # print len(cleansedSet)




        # classes = self.retrieveClasses("pp5i_train_class.txt")
        # print cleansedSet




        # df = pd.DataFrame(cleansedSet[1:])
        # df.to_csv('./clean-test-dataset.csv', index=False, header=False)
        #
        # a = itertools.izip(*csv.reader(open("./clean-test-dataset.csv", "rb")))
        # csv.writer(open("./test-transposed.csv", "wb")).writerows(a)
        #
        # dadosLimpos = pd.read_csv('./test-transposed.csv');
        # genes = dadosLimpos.columns[:-1] #nome dos genes
        # classList = pd.Series(dadosLimpos['Class'].values.ravel()).unique() #só para pegar o nome das classes

        subsets = [15]

        for setSize in subsets:
            trainingGenes = pd.read_csv('./train_top' + str(setSize) + '.csv').columns[:-1]
            selectedGenes = dadosTesteLimpos[trainingGenes]
            selectedGenes['Class'] = '?'

            print selectedGenes

            selectedGenes.to_csv('./test_top' + str(setSize) + '.csv', index=False)



        # genesTvalues = {}
        # for className in classList:
        #     tgenes = []
        #     for gene in genes:
        #         sample1 = dadosLimpos[dadosLimpos['Class'] == className][gene]
        #         sample2 = dadosLimpos[dadosLimpos['Class'] != className][gene]
        #         t = st.ttest_ind(sample1,sample2,equal_var=False)
        #         tgenes.append(t[0]) #achamos que é um valor resultante
        #     genesTvalues[className] = pd.Series(tgenes,index=genes) #achamos que é o bind dos valores p/ o gene
        # genesTvaluesDf = pd.DataFrame(genesTvalues) #exibe o conteúdo numa estrutura tabular


        # subsets = [2,4,6,8,10,12,20,25,30]
        # for setSize in subsets:
        #     topArray = []
        #     for className in classList:
        #         topArray.append(genesTvaluesDf.sort_values(className, ascending=False).index[:setSize])
        #
        #     topGenes = list(set(topArray[0]) | set(topArray[1]) | set(topArray[2]) | set(topArray[3]) | set(topArray[4]))
        #
        #     topGenes.append('Class')
        #
        #     trainTopN = dadosLimpos[topGenes]
        #     print trainTopN
        #     # sortedTrainTopN =  trainTopN.reindex(np.random.permutation(trainTopN.index))
        #     trainTopN.to_csv('./train_top' + str(setSize) + '.csv', index=False)


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
        dataValues = ["Class"]
        dataValues += ['at' + str(index+1) for index in range(7070)]
        return dataValues #[(labels[index],extractedData[index]) for index in range(1,len(extractedData) - 2)]

    def retrieveClasses(self, inputFileWithClasses):
        with open(inputFileWithClasses, 'rb') as f_in:
            header = ["Class"]
            content = f_in.read()
            content = str(content).replace("\r", " ").replace('\n', '\n') #removendo caracteres inuteis
            content = content.split('\n') #separa linhas
            return (header + content[1:len(content) - 1])


if __name__ == "__main__":
    dataPre = DataPreProcessing();
    classes = dataPre.retrieveClasses("pp5i_train_class.txt") # rotulos de cada coluna
    # dataTraining = dataPre.extractTrain("pp5i_train.gr.csv", classes)
    dataTest = dataPre.extractData("pp5i_test.gr.csv", classes)
    # labeledDataTraining = dataPre.collectLabels(dataTraining) #conjunto de treinamento
    # print labeledDataTraining
    # labeledDataTest = dataPre.collectLabels(dataTest) # conjunto de teste


    arff.dump('result.arff', dataTraining, relation="GenicExpression", names= labeledDataTraining)
