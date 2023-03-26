# CREARTE AND COMPILE A PIPELINE
import os
import kfp
from kfp import dsl
from kfp import compiler
import kfp.components as comp


URL_READ_LINES_COMP = 'gs://ml-auto-pipelines-bucket/components-yamls/line-reader-writer/kubeflow_component_spec.yaml'

@dsl.component()
def hello_world(text: str) -> str:
    print(text)
    return text

@dsl.pipeline(name='custom-components-v1', description='A pipeline with custom components')
def custom_components_pipeline(input_1: str = 'gs://ml-auto-pipelines-bucket/inputs/test_input_lines.txt',
                               output_1: str = 'gs://ml-auto-pipelines-bucket/inputs/test_output_lines.txt',
                               parameter_1: int = 5):

    read_lines_task01 = kfp.components.load_component_from_url(
        url=URL_READ_LINES_COMP)  # Passing pipeline parameter as argument to consumer op
    
    read_lines_task01(input_1=input_1, parameter_1=parameter_1) 


# V1 Compiler -> it works...!
compiler.Compiler().compile(
    pipeline_func=custom_components_pipeline,
    package_path='custom_components_pipeline.yaml')

print("List directory files")
print(os.listdir())
