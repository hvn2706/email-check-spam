import logging
import pickle
import pandas as pd
from setting import setting
from app.dto.spam_email_detection.email import SpamEmailDetectionRequest, SpamEmailDetectionResponse
from app.helper.utility import remove_tags


_logger = logging.getLogger(__name__)


class SpamEmailDetectionService:
    @classmethod
    def detect_spam_email(cls, request: SpamEmailDetectionRequest) -> SpamEmailDetectionResponse:
        text = request.subject + " " + request.content
        
        email_content = pd.DataFrame([text], columns=['Text'])
        email_content["Clean_Text"] = email_content["Text"].apply(remove_tags)
        vector_representation = EmbeddingModel.embed(email_content["Clean_Text"][0])
        _logger.info(f"Vector representation size: {vector_representation.shape}")
        _logger.info(f"Text: {email_content['Clean_Text'][0]}")
        
        prediction = SpamEmailDetectionModel.model.predict(vector_representation)
        if prediction[0] == 0:
            return SpamEmailDetectionResponse(spam=False, cleanContent=email_content['Clean_Text'][0])
        return SpamEmailDetectionResponse(spam=True, cleanContent=email_content['Clean_Text'][0])


class EmbeddingModel:
    model = None
    
    @classmethod
    def init_embedding_model(cls):
        cls.model = pickle.load(open(setting.EMBEDDING_MODEL_PATH, 'rb'))
    
    @classmethod
    def embed(cls, text):
        return cls.model.transform([text])


class SpamEmailDetectionModel:
    model = None
    
    @classmethod
    def init_spam_email_detection_model(cls):
        cls.model = pickle.load(open(setting.SPAM_EMAIL_DETECTION_MODEL_PATH, 'rb'))
