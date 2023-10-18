# Use Hugging Face transformers image as a base image
FROM huggingface/transformers-pytorch-gpu

# Set working directory
WORKDIR /workspace

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN pip uninstall -y ctransformers
RUN CT_CUBLAS=1 pip install ctransformers --no-binary ctransformers

EXPOSE 3000

COPY docker/entry.sh /entry.sh
RUN chmod +x /entry.sh
ENTRYPOINT ["/entry.sh"]