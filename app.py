# from src.mlproject.logger import logging
# from src.mlproject.exception import CustomException
# from src.mlproject.components.data_ingestion import DataIngestion
# from src.mlproject.components.data_ingestion import DataIngestionConfig
# from src.mlproject.components.data_transformation import DataTransformationConfig, DataTransformation
# from src.mlproject.components.model_trainer import ModelTrainerConfig, ModelTrainer


# import sys

# if __name__=="__main__":
#     logging.info("The execution has started")

#     try:
#         # data_ingestion_config=DataIngestionConfig()
#         data_ingestion=DataIngestion()
#         train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

#         # data_transformation_config = DataTransformationConfig()
#         data_transformation = DataTransformation()
#         train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)

#         ## Model training
#         model_trainer = ModelTrainer()
#         print(model_trainer.initiate_model_trainer(train_arr, test_arr))

#     except Exception as e:
#             logging.error(f"Error occurred: {str(e)}")
#             # This forces Python to print the raw, ugly traceback directly to your terminal screen
#             import traceback
#             traceback.print_exc()
#             raise e

from flask import Flask, request, jsonify
from src.mlproject.pipelines.prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route('/')
def home():
    return "Student Performance Prediction API is Live! Send a POST request to /predict."

@app.route('/predict', methods=['POST'])
def predict_datapoint():
    try:
        data = request.json
        
        # Map incoming JSON parameters directly to our structured data class
        data_structure = CustomData(
            gender=data['gender'],
            race_ethnicity=data['race_ethnicity'],
            parental_level_of_education=data['parental_level_of_education'],
            lunch=data['lunch'],
            test_preparation_course=data['test_preparation_course'],
            reading_score=int(data['reading_score']),
            writing_score=int(data['writing_score'])
        )
        
        final_new_data = data_structure.get_data_as_data_frame()
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(final_new_data)
        
        return jsonify({'predicted_math_score': float(results[0])})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    # Required port configuration for Hugging Face Spaces Docker environments
    app.run(host="0.0.0.0", port=7860)