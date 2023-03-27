# CREARTE AND COMPILE A PIPELINE
import os
import kfp
from kfp import dsl
from kfp import compiler
import kfp.components as comp


URL_READ_LINES_COMP = 'gs://ml-auto-pipelines-bucket/components-yamls/line-reader-writer/kubeflow_component_spec.yaml'

@dsl.component()
def get_input_parameters(input_path_1: str, 
                         output_path_1: str,
                         lines_to_read_1: int) -> str:
    component_outputs = {"input_path_1": input_path_1, "lines_to_read_1": lines_to_read_1}
    print("component_outputs: {}".format(component_outputs))
    return component_outputs

@dsl.pipeline(name='custom-components-v1', description='A pipeline with custom components')
def custom_components_pipeline(input_path_1: str = 'gs://ml-auto-pipelines-bucket/inputs/test_input_lines.txt',
                               output_path_1: str = 'gs://ml-auto-pipelines-bucket/inputs/test_output_lines.txt',
                               lines_to_read_1: int = 5):

    
    inp_comp = get_input_parameters(input_path_1, output_path_1, lines_to_read_1)
    read_lines_task01 = kfp.components.load_component_from_url(
        url=URL_READ_LINES_COMP)  # Passing pipeline parameter as argument to consumer op
    
    read_lines_task01(input_1=inp_comp.outputs["input_path_1"], 
                      parameter_1=inp_comp.outputs["lines_to_read_1"]) 


# V1 Compiler -> it works...!
compiler.Compiler().compile(
    pipeline_func=custom_components_pipeline,
    package_path='custom_components_pipeline.yaml')

print("List directory files")
print(os.listdir())
