# Translate-books-for-the-visually-impaired
Translate a well-written book for the visually impaired, in which all the pictures have been replaced with valid, appropriate descriptions.

# Project Overview
![image](https://github.com/HerocatUED/Translate-books-for-the-visually-impaired/blob/mater/overview.jpg)

# Setup
1. Prepare Python [environment](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/environment.md)
2. Install [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html) and [pytorch](https://pytorch.org/get-started/locally/), CUDA10 is recommended because both PaddleOCR and LAVIS support it.
3. Install [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/quickstart.md)
4. Install [LAVIS](https://github.com/salesforce/LAVIS#installation)
5. Install other requirements with following command
```bash
pip install -r requirements.txt
```

# Quick Start
1. Sign up for an baidu translation API account [here](Sign up for an account)
2. Put scanned books (as PDF file) into input folder
3. Run main.py with following command (with your translation account)
```bash
python main.py --id yourID --key yourKey
```
4. You can find translated books (as TXT file) in output folder 
