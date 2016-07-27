setwd("C://Users//HP//Downloads")
data = read.csv(file="Train_pjb2QcD.csv", header=TRUE, sep=",")

##############  Imputaion  #####################################

data[data==""] <- NA
random = runif(length(data[is.na(data[,5]),5]), 0, 1)
index  = which(is.na(data[,5]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(data[,5]=="M")) / (length(which(data[,5]=="M"))+length(which(data[,5]=="F"))))
    data[index[i],5] = "M"
  else
    data[index[i],5] = "F"
}

random = runif(length(data[is.na(data[,7]),7]), 0, 1)
index  = which(is.na(data[,7]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(data[,7]=="D")) / (length(which(data[,3]=="D"))+length(which(data[,3]=="M"))))
    data[index[i],3] = "Yes"
  else
    data[index[i],3] = "No"
}

data[is.na(data[,4]),4] <- 0

random = runif(length(data[is.na(data[,6]),6]), 0, 1)
index  = which(is.na(data[,6]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(data[,6]=="Yes")) / (length(which(data[,6]=="Yes"))+length(which(data[,6]=="No"))))
    data[index[i],6] = "Yes"
  else
    data[index[i],6] = "No"
}

data[is.na(data[,9]),9] <- mean(as.numeric(data[which(data$LoanAmount>=0),9]))
data[is.na(data[,10]),10] <- mean(as.numeric(data[which(data$Loan_Amount_Term>=0),10]))
data$Credit_History = factor(data$Credit_History, levels = c("0", "1"),ordered=F)

random = runif(length(data[is.na(data[,11]),11]), 0, 1)
index  = which(is.na(data[,11]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(data[,11]=="1")) / (length(which(data[,11]=="1"))+length(which(data[,11]=="0"))))
    data[index[i],11] = "1"
  else
    data[index[i],11] = "0"
}

# train = data[1:floor(0.75*dim(data)[1]),]
# validation  = data[floor((0.75*dim(data)[1])+1):dim(data)[1],]

#####################    Random Forest    ###################################

library(randomForest)
library(caret)

data = data[,-1]
folds = createFolds(data$Gender, k=5)
n_trees = 100
error_RF = 0.0
for (i in 1:5) {
  training_data = data[-folds[[i]],]
  test_data = data[folds[[i]],]
  
  fit.RF <- randomForest(Loan_Status ~ ., data=training_data, replace=FALSE,importance=TRUE, ntree=n_trees)
  
  prediction = predict(fit.RF,test_data[-12],type = c("class"))
  combined_results = cbind(prediction,test_data[12])  
  error_RF = error_RF + 1 - (sum(combined_results[1]==combined_results[2])/dim(combined_results[1])[1])
}
error_RF = error_RF/5
error_RF


#####################        SVM          ######################################

library('e1071')                            # for svm
folds = createFolds(data$Gender, k=5)
error_svm = 0.0 
for (i in 1:5) {
  
  training_data = data[-folds[[i]],]
  test_data     = data[folds[[i]],]  
  
  fit.svm  = svm(Loan_Status ~ ., data = training_data)
  pred = predict(fit.svm, test_data)
  error_svm = error_svm + 1 - sum(pred == test_data[,12])/dim(test_data)[1]
  
}

error_svm = error_svm/5
error_svm
##################### Logistic Regression #################################

folds = createFolds(data$Gender, k=5)
error_logistic = 0.0 
for (i in 1:5) {
  
  training_data = data[-folds[[i]],]
  test_data     = data[folds[[i]],]  
  
  fit.logistic  = glm(Loan_Status ~.,family=binomial(link='logit'),data=training_data)
  pred = predict(fit.logistic,test_data, type = "response")
  pred[which(pred>=0.5)] = "Y"
  pred[which(pred<0.5)]  = "N"
  pred = as.factor(pred)
  error_logistic = error_logistic + 1 - sum(pred == test_data[,12])/dim(test_data)[1]
  cat('\n',error_logistic)
}

error_logistic = error_logistic/5
error_logistic

##################### Making same changes to the test data set ###################################

test = read.csv(file="test.csv", header=TRUE, sep=",")

View(test)

##############  Imputaion  #####################################

test[test==""] <- NA
random = runif(length(test[is.na(test[,2]),2]), 0, 1)
index  = which(is.na(test[,2]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(test[,2]=="Male")) / (length(which(test[,2]=="Male"))+length(which(test[,2]=="Female"))))
    test[index[i],2] = "Male"
  else
    test[index[i],2] = "Female"
}

test$Married = factor(test$Married, levels = c("","No", "Yes"),ordered=F)

test[is.na(test[,4]),4] <- 0

random = runif(length(test[is.na(test[,6]),6]), 0, 1)
index  = which(is.na(test[,6]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(test[,6]=="Yes")) / (length(which(test[,6]=="Yes"))+length(which(test[,6]=="No"))))
    test[index[i],6] = "Yes"
  else
    test[index[i],6] = "No"
}

test[is.na(test[,9]),9] <- mean(as.numeric(test[which(test$LoanAmount>=0),9]))
test[is.na(test[,10]),10] <- mean(as.numeric(test[which(test$Loan_Amount_Term>=0),10]))
test$Credit_History = factor(test$Credit_History, levels = c("0", "1"),ordered=F)

random = runif(length(test[is.na(test[,11]),11]), 0, 1)
index  = which(is.na(test[,11]))

for (i in 1:length(random)) {
  if(random[i]<= length(which(test[,11]=="1")) / (length(which(test[,11]=="1"))+length(which(test[,11]=="0"))))
    test[index[i],11] = "1"
  else
    test[index[i],11] = "0"
}

############## Predictions #############

fit.RF <- randomForest(Loan_Status ~ ., data=data, replace=FALSE,importance=TRUE, ntree=n_trees)
pred.RF = predict(fit.RF,test,type = c("class"))
submit.RF <- data.frame(Loan_ID= test$Loan_ID, Loan_Status= pred.RF )
write.csv(submit.RF, "RF-Prediction")

fit.svm = svm(Loan_Status ~ ., data = data)
pred.svm = predict(fit.svm, test)
submit.svm <- data.frame(Loan_ID= test$Loan_ID, Loan_Status= pred.svm )
write.csv(submit.svm, "SVM-Prediction")

fit.logistic  = glm(Loan_Status ~.,family=binomial(link='logit'),data=data)
pred = predict(fit.logistic,test, type = "response")
pred[which(pred>=0.5)] = "Y"
pred[which(pred<0.5)]  = "N"
pred.logistic = as.factor(pred)
submit.logistic <- data.frame(Loan_ID= test$Loan_ID, Loan_Status= pred.logistic )
write.csv(submit.svm, "Logistic-Prediction")