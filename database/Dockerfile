FROM python:3.8-slim-buster


# 기본 도커 가상 컴퓨터에서의 설치 패키지 
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 복사 붙여넣기할 디렉토리명 
COPY . /usr/app

WORKDIR /usr/app 

RUN pip install -U pip && \
    pip install requests pandas psycopg2-binary python-dotenv

ENTRYPOINT [ "python","data_generator.py"]
CMD ["db"]