import csv
import collections
import arff
import itertools

class DataPreProcessing:
    #extracao da planilha de dados
    def extractData(self, inputFile, classes):
        pp5 = [] # lista de tuplas contendo rotulo e conteudo

        rawset = csv.reader(open(inputFile))
        columnSet = zip(*rawset)[1:]
        for column in columnSet:
            label = classes[int(column[0])-1]
            mutableTuple = [label]
            mutableTuple += [float(value) for value in list(column)[1:]]
            cleanseData()
            pp5.append(mutableTuple)
        return pp5

    #separa rotulos dos dados e devolve lista contendo (rotulo, conteudo)
    def collectLabels(self, extractedData):
        dataValues = ["class"]
        dataValues += ['at' + str(index+1) for index in range(7070)]
        return dataValues #[(labels[index],extractedData[index]) for index in range(1,len(extractedData) - 2)]

    def retrieveClasses(self, inputFileWithClasses):
        with open(inputFileWithClasses, 'rb') as f_in:
            content = f_in.read()
            content = str(content).replace("\r", " ").replace('\n', '\n') #removendo caracteres inuteis
            content = content.split('\n') #separa linhas
            return content[1:len(content) - 1]

    def cleanseData(self, dataset):
        for column in datset:
            for value in column:
                

if __name__ == "__main__":
    dataPre = DataPreProcessing();
    classes = dataPre.retrieveClasses("pp5i_train_class.txt") # rotulos de cada coluna
    dataTraining = dataPre.extractData("pp5i_train.gr.csv", classes)
    dataTraining = dataPre.cleanseData(dataTraining)
    # dataTest = dataPre.extractData("pp5i_test.gr.csv")
    labeledDataTraining = dataPre.collectLabels(dataTraining) #conjunto de treinamento
    print labeledDataTraining
    # labeledDataTest = dataPre.collectLabels(dataTest) # conjunto de teste

    arff.dump('result.arff', dataTraining, relation="GenicExpression", names= labeledDataTraining)
