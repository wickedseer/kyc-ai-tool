# AI Tool to Assist KYC (Know Your Customer)

An intelligent document processing system that automates the extraction and verification of key information from identity documents, built using Flask, OpenCV, and Tesseract OCR.


## Table of Contents

  - [Overview](#overview)
  - [Features](#features)
  - [Supported Documents](#supported-documents)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Demo Video](#demo-video)
  - [Published Research Papers](#published-research-papers)


## Overview

KYC (Know Your Customer) is a mandatory verification process used by financial institutions, banks, and businesses to confirm the identity of their clients. This project automates the traditionally manual and time-consuming KYC process by using computer vision and OCR (Optical Character Recognition) to extract relevant information from identity documents with minimal human intervention.

The system accepts images of identity documents, preprocesses them for optimal OCR accuracy, detects and extracts text using a CTPN (Connectionist Text Proposal Network) model, and parses the extracted text to return structured, labeled data.

## Features

- Automatic text detection and extraction from identity document images
- Document-specific field parsing for Aadhaar, PAN, and GST certificates
- Image preprocessing using adaptive thresholding for improved OCR accuracy
- Address extraction from the back side of Aadhaar cards
- RESTful API for easy integration with mobile or web clients
- Structured JSON responses for all extracted fields



## Supported Documents

| Document | Extracted Fields |
|----------|-----------------|
| Aadhaar Card (Front) | Name, Date of Birth, Gender, Aadhaar Number |
| PAN Card | PAN Number, Name, Father's Name, Date of Birth |
| GST Certificate | Registration Number, Legal Name, Trade Name, Date of Liability, Date of Issue, Address, Type of Registration |



## Tech Stack

- **Backend Framework:** Flask (Python)
- **Image Processing:** OpenCV
- **OCR Engine:** Tesseract OCR (via pytesseract)
- **Text Detection Model:** CTPN (Connectionist Text Proposal Network)
- **Deep Learning:** TensorFlow
- **Image Thresholding:** scikit-image



## Installation

### Prerequisites

- Python 3.7+
- Tesseract OCR installed on your system
- TensorFlow compatible environment

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/wickedseer/kyc-ai-tool.git
   cd kyc-ai-tool
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate      # On Windows: .\env\Scripts\Activate.ps1
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR:
   - **Ubuntu/Debian:** `sudo apt install tesseract-ocr`  
   - **Windows:** Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

5. Run the application:
   ```bash
   python runserver.py
   ```
   The app will start at `http://localhost:5555` and open automatically in your browser.


## Usage

1. Open the application in your browser.
2. Log in with the default credentials:
   - **Username:** admin
   - **Password:** 12345678
3. From the dashboard, select the type of document you want to process.
4. Upload an image of the identity document.
5. The system will extract and display the relevant fields in a structured format.

## API Endpoints

### `POST /upload`
Uploads a document image and returns extracted fields.

**Form Data Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Document type: `Aadhar`, `Aadhar Back`, `PAN`, `GST` |
| `photo-pan` | file | Image file (used for PAN and Aadhaar Back) |
| `photo-aadhar` | file | Image file (used for Aadhaar) |
| `photo-gst` | file | Image file (used for GST) |

**Sample Response (PAN Card):**
```json
{
  "status": true,
  "fields": {
    "PANNo": "ABCDE1234F",
    "DateOfBirth": "01/01/1995",
    "Name": "JOHN DOE",
    "FatherName": "RICHARD DOE"
  },
  "image_path": "./kycweb/UPLOAD_FOLDER/PAN/2024_01_01_12_00_00.png"
}
```

**Sample Response (Aadhaar Front):**
```json
{
  "status": true,
  "fields": {
    "AadharNo": "1234 5678 9012",
    "Name": "JOHN DOE",
    "DateofBirth": "01-01-1995",
    "Gender": "Male"
  },
  "image_path": "./kycweb/UPLOAD_FOLDER/Aadhar/2024_01_01_12_00_00.png"
}
```

**Sample Response (GST Certificate):**
```json
{
  "status": true,
  "fields": {
    "registration_number": "27ABCDE1234F1Z5",
    "legal_name": "EXAMPLE ENTERPRISES",
    "trade_name": "EXAMPLE STORE",
    "date_of_liability": "01/01/2020",
    "date_of_issue": "15/01/2020",
    "address": "123, Example Street, Mumbai",
    "type_of_registration": "Regular"
  },
  "image_path": "./kycweb/UPLOAD_FOLDER/GST/2024_01_01_12_00_00.png"
}
```


## Demo Video

https://github.com/user-attachments/assets/04dd5d67-8548-4c94-8245-a6b4975f8270


## Published Research Papers

**Title:** A Comprehensive Survey of Identity Document Data Extraction Techniques for Efficient KYC Verification and Identity Management    
**Published in:** International Research Journal of Engineering and Technology (IRJET)     
**Link:** https://www.irjet.net/archives/V10/i12/IRJET-V10I12125.pdf


**Title:** An Efficient OCR System for Extracting Information from Indian Identity Documents using CTPN  
**Published in:** Ajeenkya DY Patil Journal of Innovation in Engineering & Technology  
**Link:** https://adypsoe.in/adypjiet/assets/publications/2024/Dec/R3-ADYPJIET-An-Efficient-OCR-System-for-Extracting.pdf
