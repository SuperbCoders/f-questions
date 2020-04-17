import requests

from deal_api.models import Document, DocumentAnswer
from deal_digger.celery import app
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@app.task(name="extract_text", time_limit=40 * 60)
def extract_text(doc_id):
    logger.info(f'Starting {doc_id}')
    doc = Document.objects.get(id=doc_id)
    doc.status = Document.States.PROCESSING
    doc.save(update_fields=["status"])

    logger.info(f'Sending request {doc_id}')

    url = "http://ocr:8001/api/v1/documents/"
    files = {"file": ("ustav.pdf", open(doc.pdf_file.path, "rb"), "application/pdf", {"Expires": "0"})}
    headers = {
        "Accept": "application/json",
    }
    params = {
        "start": 1,
        "quality": "true"
    }
    response = requests.post(url=url, params=params, headers=headers, files=files, timeout=None)

    logger.info(f'Received request {doc_id}')
    logger.info(f'Raw response body: \n{response.text[:100]}')

    data = response.json()
    if data == '500':
        doc.status = Document.States.OCR_ERROR
    else:
        whole_text = ' '.join(
            ' '.join(i['body'] for i in part['text'])
            for part in response.json()['content']
        )

        doc.text = whole_text
        doc.status = Document.States.PROCESSED

    doc.save()
    logger.info(f'Saved text {doc_id}')


@app.task(name="ask_questions", autoretry_for=(Exception,), max_retries=1)
def ask_questions(doc_id):
    from deal_api.dl_model import model as pavlov_answer_model

    logger.info(f'Starting {doc_id}')
    doc = Document.objects.get(id=doc_id)
    doc.status = Document.States.PROCESSING
    doc.save()

    logger.info(f'Asking {doc_id} about executor')
    executor_answer, raw_answers = pavlov_answer_model.predict_executor(doc.text)
    ans, created = DocumentAnswer.objects.get_or_create(
        document=doc,
        question_type=DocumentAnswer.QuestionTypes.EXECUTOR
    )
    ans.answer = executor_answer or 'Модель не смогла ответить'
    ans.raw_answer = ', '.join(raw_answers)
    ans.save()

    logger.info(f'Asking {doc_id} about executor period')
    executor_answer = pavlov_answer_model.predict_executor_period(doc.text)
    ans, created = DocumentAnswer.objects.get_or_create(
        document=doc,
        question_type=DocumentAnswer.QuestionTypes.EXECUTOR_PERIOD
    )
    ans.answer = executor_answer or 'Модель не смогла ответить'
    ans.save()

    doc.status = Document.States.PROCESSED
    doc.save()

    logger.info(f'Saved answers {doc_id}')
