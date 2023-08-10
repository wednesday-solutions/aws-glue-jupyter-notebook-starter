FROM amazon/aws-glue-libs:glue_libs_3.0.0_image_01
RUN pip3 install -U pip setuptools wheel
RUN pip3 install -U spacy
RUN pip3 install scispacy
RUN pip3 install boto
RUN pip3 install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_ner_bc5cdr_md-0.5.1.tar.gz
RUN pip3 install nltk
RUN pip3 install python-dotenv

# ENV AWS_REGION ap-southeast-1
