import csv
import os
import numpy as np
import math

# Name: Mahmoud Mohamed Ismail           ID: 20170271  GROUP: IS_DS_3
# Assignment3 - Naïve Bayesian
class Attribute:
    def __init__(self, information_name , name, class_value, count, column_value, probabilty, view):
        self.information_name = information_name
        self.name = name
        self.class_value = class_value #unacc acc vgood good
        self.count = count
        self.column_value = column_value
        self.probabilty = probabilty
        self.view = view


class Information:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

def get_unique_values():
     # each index contains unique values of each column
     values = []
     with open(os.getcwd()+'\\car.data.csv') as csv_file:
         csv_reader = csv.reader(csv_file, delimiter=',')
         line_count = 0
         for row in csv_reader:
             for i in range(0,len(row)):
                 if line_count == 0:
                     temp_arr = []
                     temp_arr.append(row[i])
                     values.append(temp_arr)
                 else:
                     values[i].append(row[i])
             line_count += 1
     unique_values =[]
     for arr in values:
         temp =[]
         for x in arr:
             if x not in temp:
                 temp.append(x)
         unique_values.append(temp)
     return unique_values

def get_information(unique_values):
    attributes = []
    # classifiers is last element in unique_values
    classifiers = unique_values[len(unique_values)-1]
    unique_values.remove(classifiers)
    # now get Information with it's attributes and count.   each index represents a feature.
    temp_information_count = 1
    for arr in unique_values:
        temp_information_name = "Information" + str(temp_information_count)
        for x in arr:
            temp_attribute_name = x#vhigh high med low
            for classifier in classifiers:
                temp_classifier_name = classifier#unacc #acc # vgood #good
                temp_count = 0
                temp_attribute = Attribute(temp_information_name, temp_attribute_name, temp_classifier_name, temp_count,temp_information_count-1,0,"")
                attributes.append(temp_attribute)
        temp_information_count += 1

    with open(os.getcwd() + '\\car.data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            temp_count = 0
            arr = []
            trainning_set = []
            test_set = []
            for row in csv_reader:
                arr.append(row)
            temp = []
            for i in range(0,len(arr)):
                temp.append(i)
            index_of_random_rows = np.random.choice(temp, int(0.75 * len(arr)), False)
            for i in range(0,len(arr)):
                if i in index_of_random_rows:
                    trainning_set.append(arr[i])
                else:
                    test_set.append(arr[i])
    for attribute in attributes:
            for row in trainning_set:
                for i in range(0,len(row)):#0 1 2 3 4 5
                    if i == attribute.column_value and row[i] == attribute.name and row[len(row)-1] == attribute.class_value:
                        temp_count += 1
            attribute.count = temp_count
            temp_count = 0

    # fill in information objects and append in list
    temp_information = []
    for attribute in attributes:
        flag = check(temp_information, attribute.information_name)
        if(flag != -1):
            temp_information[flag].attributes.append(attribute)
        else:
            temp_information.append(Information(attribute.information_name, [attribute]))

    temp_values = get_unique_values()
    temp_classifiers = temp_values[len(temp_values)-1]
    temp_count_classifers = []
    for x in temp_classifiers:
        count = 0
        for row in trainning_set:
            if x in row:
                count +=1
        temp_count_classifers.append(count)

    for i in range(0,len(temp_count_classifers)): #0 1 2 3
        for x in temp_information:
            for j in x.attributes:
                if j.class_value == temp_classifiers[i]:
                    j.probabilty = j.count / temp_count_classifers[i]
                    j.view = str(j.count)+"/"+ str(temp_count_classifers[i])
    # return information gained from training set adn test_set to apply these infomration on ( to calculate accuracy)
    return [temp_information,test_set]
def check(information_list,information_name):
    for i in range(0,len(information_list)):
        if information_list[i].name == information_name:
            return i
    return -1


def get_attributes_with_same_name(temp_information_list,name,col):
    attributes =[]
    temp_information = temp_information_list[col]
    for attribute in temp_information.attributes:
        if name == attribute.name:
            attributes.append(attribute)

    return attributes

def get_learned_data(row,temp_infomration):

    # get unique values
    unique_list = get_unique_values()
    classifiers = unique_list[len(unique_list) - 1]
    # get probability of all classifers
    probability_classifers = get_probability_of_classifers()
    # remove last column
    list =[]
    for value in row:
        i=  value.pop(len(value)-1)
        list.append(i)

    learned_data = []
    for value in row:
        # get data with same attributes values
        attributes = []
        for i in range(0,len(value)):
            temp_attribute = get_attributes_with_same_name(temp_infomration,value[i],i)
            attributes.append(temp_attribute)
        #calculate probability
        probability_list = []
        for i in range(0,len(attributes[0])):
            temp_number = 1
            for attribute in attributes:
                temp_number *= attribute[i].probabilty
            temp_number *= probability_classifers[i]
            probability_list.append(f"{temp_number:.6f}")
        #choose biggest probaility and assign classifier column with the classifer which has biggest probability
        index_of_largest_probability = get_index_of_max(probability_list)
        learned_data.append(classifiers[index_of_largest_probability])
    print("Test phase:")
    for i in range(0,len(row)):
        print("Tuple data: ",row[i])
        print("Classifer Value in original file: ",list[i])
        print("Classifer value after prediction: ",learned_data[i])
        print("---------------------------------")
    accuarcy = 0
    for i in range(0,(len(list))):
        if list[i] == learned_data[i]:
            accuarcy+=1
    print("total accuarcy:" , f"{accuarcy / len(list) * 100:.2f}")






















def get_index_of_max(list):
    max = list[0]
    index = 0
    for i in range(1,len(list)):
        if list[i] > max:
            max = list[i]
            index = i
    return index





def getAccuracy(temp_information, test_set):
    get_learned_data(test_set,temp_information)





def get_probability_of_classifers():
    unique_list = get_unique_values()
    unique_classifiers = unique_list[len(unique_list)-1]
    data =[]
    with open(os.getcwd() + '\\car.data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)
    probability_of_each_classifier = []
    for classifer in unique_classifiers:
        temp_count = 0
        for row in data:
            if classifer in row:
                temp_count +=1
        probability_of_each_classifier.append(temp_count/len(data))

    return probability_of_each_classifier








def main():
    unique_values = get_unique_values()
    information = get_information(unique_values)
    getAccuracy(information[0],information[1])




main()












