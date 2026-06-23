# 🔐 Convolutional Encoder & Viterbi Decoder

Interactive web application for demonstrating forward error correction using convolutional codes.

## Features
- Text to 8-bit ASCII conversion
- Rate-1/2,2/3/ K=3 convolutional encoding (G₁=111, G₂=101)
- AWGN channel simulation with adjustable SNR
- Viterbi decoding with trellis visualization
- Real-time BER analysis and performance plots

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
