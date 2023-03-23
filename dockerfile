FROM python:3
ENV PYTHONUNBUFFERED 1
# ENV TZ=Asia/Ho_Chi_Minh
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir /ChatATTT
WORKDIR /ChatATTT
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]