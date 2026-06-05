library(dplyr)
library(caret)
library(xgboost)

# Load traffic data
traffic_data <- read.csv("traffic_data.csv")

# Data preprocessing
prepare_data <- function() {
  days <- c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
  traffic_data <- traffic_data %>%
    mutate(
      Day = factor(Day, levels = days),
      Hour = as.numeric(Hour),
      IsWeekend = ifelse(Day %in% c("Saturday","Sunday"), 1, 0),
      IsRushHour = ifelse(Hour %in% c(8:10,17:19), 1, 0),
      DayFactor = as.numeric(Day),
      HourSin = sin(2*pi*Hour/24),
      HourCos = cos(2*pi*Hour/24)
    ) %>%
    filter(!is.na(Congestion))
  return(traffic_data)
}

traffic_data <- prepare_data()

# Train model
train_model <- function(traffic_data) {
  feature_cols <- c("Hour","DayFactor","HourSin","HourCos","IsWeekend","IsRushHour")
  preproc <- preProcess(traffic_data[,feature_cols], method=c("center","scale"))
  traffic_processed <- predict(preproc, traffic_data)
  set.seed(123)
  trainIndex <- createDataPartition(traffic_data$Congestion, p=0.8, list=FALSE)
  train_data <- traffic_processed[trainIndex,]
  dtrain <- xgb.DMatrix(data=as.matrix(train_data[,feature_cols]), label=train_data$Congestion)
  params <- list(
    booster="gbtree", objective="reg:squarederror",
    eta=0.1, max_depth=6, subsample=0.8, colsample_bytree=0.8
  )
  model <- xgb.train(
    params, data=dtrain, nrounds=100
  )
  return(list(model=model, preproc=preproc, features=feature_cols))
}

model_info <- train_model(traffic_data)

# Predict API wrapper
predict_traffic <- function(model_info, day, hour) {
  input_data <- data.frame(
    Day = factor(day, levels=c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")),
    Hour = as.numeric(hour)
  )
  input_data <- input_data %>%
    mutate(
      IsWeekend=ifelse(Day %in% c("Saturday","Sunday"), 1, 0),
      IsRushHour=ifelse(Hour %in% c(8:10,17:19), 1, 0),
      DayFactor=as.numeric(Day),
      HourSin=sin(2*pi*Hour/24),
      HourCos=cos(2*pi*Hour/24)
    )
  input_processed <- predict(model_info$preproc, input_data)
  prediction <- predict(model_info$model, 
                        xgb.DMatrix(data=as.matrix(input_processed[,model_info$features])))
  return(prediction)
}
