from typing import Dict, List

import pytest
from pydantic import BaseModel
from transformers.testing_utils import nested_simplify

from docquery import pipeline
from docquery.document import load_document
from docquery.ocr_reader import TesseractReader


CHECKPOINTS = {
    "LayoutLMv1": "impira/layoutlm-document-qa",
    "LayoutLMv1-Invoices": "impira/layoutlm-invoices",
    "Donut": "naver-clova-ix/donut-base-finetuned-docvqa",
}


class QAPair(BaseModel):
    question: str
    answers: Dict[str, Dict]


class Example(BaseModel):
    name: str
    path: str
    qa_pairs: List[QAPair]


# Use the examples from the DocQuery space (this also solves for hosting)
EXAMPLES = [
    Example(
        name="contract",
        path="https://huggingface.co/spaces/impira/docquery/resolve/2f6c96314dc84dfda62d40de9da55f2f5165d403/contract.jpeg",
        qa_pairs=[
            {
                "question": "What is the purchase amount?",
                "answers": {
                    "LayoutLMv1": {"score": 0.9999, "answer": "$1,000,000,000", "word_ids": [97], "page": 0},
                    "LayoutLMv1-Invoices": {"score": 0.9997, "answer": "$1,000,000,000", "word_ids": [97], "page": 0},
                    "Donut": {"answer": "$1,0000,000,00"},
                },
            }
        ],
    ),
    Example(
        name="invoice",
        path="https://huggingface.co/spaces/impira/docquery/resolve/2f6c96314dc84dfda62d40de9da55f2f5165d403/invoice.png",
        qa_pairs=[
            {
                "question": "What is the invoice number?",
                "answers": {
                    "LayoutLMv1": {"score": 0.9997, "answer": "us-001", "word_ids": [15], "page": 0},
                    "LayoutLMv1-Invoices": {"score": 0.9999, "answer": "us-001", "word_ids": [15], "page": 0},
                    "Donut": {"answer": "us-001"},
                },
            }
        ],
    ),
    Example(
        name="statement",
        path="https://huggingface.co/spaces/impira/docquery/resolve/2f6c96314dc84dfda62d40de9da55f2f5165d403/statement.pdf",
        qa_pairs=[
            {
                "question": "What are net sales for 2020?",
                "answers": {
                    "LayoutLMv1": {"score": 0.9429, "answer": "$ 3,750\n", "word_ids": [15, 16], "page": 0},
                    "LayoutLMv1-Invoices": {"score": 0.9956, "answer": "$ 3,750\n", "word_ids": [15, 16], "page": 0},
                    "Donut": {"answer": "$ 3,750"},
                },
            }
        ],
    ),
    Example(
        name="readme",
        path="https://github.com/impira/docquery/blob/ef73fa7e8069773ace03efae2254f3a510a814ef/README.md",
        qa_pairs=[
            {
                "question": "What are the use cases for DocQuery?",
                "answers": {
                    # These examples demonstrate the fact that the "word_boxes" are way too coarse in the web document implementation
                    "LayoutLMv1": {
                        "score": 0.7728,
                        "answer": "DocQuery excels at a number of use cases involving structured, semi-structured, or unstructured documents. You can ask questions about invoices, contracts, forms, emails, letters, receipts, and many more. You can also classify documents. We will continue evolving the model, offer more modeling options, and expanding the set of supported documents. We welcome feedback, requests, and of course contributions to help achieve this vision.",
                        "word_ids": [7],
                        "page": 1,
                    },
                    "LayoutLMv1-Invoices": {
                        "score": 0.7931,
                        "answer": "DocQuery is a library and command-line tool that makes it easy to analyze semi-structured and unstructured documents (PDFs, scanned images, etc.) using large language models (LLMs). You simply point DocQuery at one or more documents and specify a question you want to ask. DocQuery is created by the team at Impira.",
                        "word_ids": [43],
                        "page": 0,
                    },
                    "Donut": {"answer": "engine Powered by large language"},
                },
            }
        ],
    ),
]


@pytest.mark.parametrize("example", EXAMPLES)
@pytest.mark.parametrize("model", CHECKPOINTS.keys())
def test_impira_dataset(example, model):
    document = load_document(example.path)
    pipe = pipeline("document-question-answering", model=CHECKPOINTS[model])
    for qa in example.qa_pairs:
        resp = pipe(question=qa.question, **document.context, top_k=1)
        assert nested_simplify(resp, decimals=4) == qa.answers[model]


def test_run_with_choosen_OCR_str():
    example = EXAMPLES[0]
    document = load_document(example.path, "tesseract")
    pipe = pipeline("document-question-answering", model=CHECKPOINTS["LayoutLMv1"])
    for qa in example.qa_pairs:
        resp = pipe(question=qa.question, **document.context, top_k=1)
        assert nested_simplify(resp, decimals=4) == qa.answers["LayoutLMv1"]


def test_run_with_choosen_OCR_instance():
    example = EXAMPLES[0]
    reader = TesseractReader()
    document = load_document(example.path, reader)
    pipe = pipeline("document-question-answering", model=CHECKPOINTS["LayoutLMv1"])
    for qa in example.qa_pairs:
        resp = pipe(question=qa.question, **document.context, top_k=1)
        assert nested_simplify(resp, decimals=4) == qa.answers["LayoutLMv1"]
