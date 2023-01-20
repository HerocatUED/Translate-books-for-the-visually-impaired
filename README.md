# Translate-books-for-the-visually-impaired

Translate a well-written book for the visually impaired, in which all the pictures have been replaced with valid, appropriate descriptions.

## Project Overview

![image](https://github.com/HerocatUED/Translate-books-for-the-visually-impaired/blob/mater/overview.jpg)

## Setup

1. Prepare Python [environment](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/environment.md)
2. Install [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html) and [pytorch](https://pytorch.org/get-started/locally/), CUDA10 is recommended because both PaddleOCR and LAVIS support it.
3. Install [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/quickstart.md)
4. Install [LAVIS](https://github.com/salesforce/LAVIS#installation), if you want to train your own model, it is recommended to install it in editable mode.
5. Install other requirements with following command
    ```bash
    pip install -r requirements.txt
    ```


## Train

1. Download the [configuration file](https://drive.google.com/drive/folders/1_R--gXxzAYVg_ORV5RpuVE1A-CuTC8mc?usp=share_link) and [dataset](https://drive.google.com/file/d/105kgWN_Wu0a8CZARBQqU2CpJTkThfMPd/view?usp=share_link) for training, you can also orgnize your own dataset according to our example.
2. Put the annotations and images folder in the directory "LAVIS-main/cache/coco".
3. Copy the "caption_on_task.yaml" to "LAVIS-main" and "task_cap.yaml" to "LAVIS-main/lavis/configs". The "caption_on_task.yaml" determines the training configuration and "task_cap.yaml" determines the dataset. You can refer to [the official document](https://opensource.salesforce.com/LAVIS//latest/tutorial.datasets.html) to modify them for your training.
4. Open "LAVIS-main/lavis/datasets/builders/caption_builder.py" and edit class **COCOCapBuilder**, modify its default path to the "configs/task_cap.yaml" or according to where you put the configuration file.
5. If you install the LAVIS in editable mode, skip this step.Otherwise, run

    ```
    pip install .
    ```

    again to overwrite the previous version.
6. Run

    ```
    python train.py --cfg-path caption_on_task.yaml
    ```


To use the model you trained, just modify the path in model.yaml to your own model path.Ensure that your model is using BLIP architecture or there will be error.

## Dataset&Model

|File|Download|
|:----:|:----:|
|Chinese dataset|[Google Drive](https://drive.google.com/file/d/1t62z4kjycI5qOpchzIjV3A_sWrwKfSw2/view?usp=share_link)|
|English dataset|[Google Drive](https://drive.google.com/file/d/1lpD_I8_KHN-igmWMxRqPGNjigrmlCmHl/view?usp=share_link)|
|English dataset for LAVIS traning|[Google Drive](https://drive.google.com/file/d/105kgWN_Wu0a8CZARBQqU2CpJTkThfMPd/view?usp=share_link)|
|Pre-trained Model|[Google Drive](https://drive.google.com/file/d/1rPU4OLtWhpfIDiYLGngvolWkDN3srDuv/view?usp=share_link)|

## Quick Start

1. Sign up for an baidu translation API account [here](http://fanyi-api.baidu.com/product/11)
2. Download pre-trained model from [here](https://drive.google.com/file/d/1rPU4OLtWhpfIDiYLGngvolWkDN3srDuv/view?usp=share_link), and put it in the /model folder
3. Put scanned books (as PDF file) into input folder
4. Run main.py with following command (with your translation account)

    ```bash
    python main.py --id yourID --key yourKey
    ```

5. You can find translated books (as TXT file) in output folder 

