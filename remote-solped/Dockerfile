# Use an official AWS Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.8

# Copy only the necessary files for installing dependencies
COPY requirements.txt .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


# Copy function code
COPY . ${LAMBDA_TASK_ROOT}


# Set the command to run the Python script
CMD ["lambda_function.lambda_handler"]
