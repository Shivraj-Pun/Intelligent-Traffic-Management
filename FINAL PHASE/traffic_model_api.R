library(plumber)
source("traffic_model_logic.R")

#* @apiTitle Traffic Congestion Prediction API

#* Predict traffic congestion
#* @param day The day of the week
#* @param hour The hour (0-23)
#* @get /predict
function(day, hour) {
  pred <- predict_traffic(model_info, day, as.numeric(hour))
  list(prediction = round(pred * 100, 1))
}

#* Return data for EDA
#* @get /eda
function() {
  traffic_data
}
