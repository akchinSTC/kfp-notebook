#
# Copyright 2018-2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pytest
from kfp_notebook.pipeline import NotebookOp


@pytest.fixture
def notebook_op():
    return NotebookOp(name="test",
                      notebook="test_notebook.ipynb",
                      cos_endpoint="http://testserver:32525",
                      cos_bucket="test_bucket",
                      cos_directory="test_directory",
                      cos_dependencies_archive="test_archive.tgz",
                      image="test/image:dev")


def test_fail_without_cos_endpoint():
    with pytest.raises(TypeError) as error_info:
        NotebookOp(name="test",
                   notebook="test_notebook.ipynb",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


def test_fail_without_cos_bucket():
    with pytest.raises(TypeError) as error_info:
        NotebookOp(name="test",
                   notebook="test_notebook.ipynb",
                   cos_endpoint="http://testserver:32525",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


def test_fail_without_cos_directory():
    with pytest.raises(TypeError) as error_info:
        NotebookOp(name="test",
                   notebook="test_notebook.ipynb",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


def test_fail_without_cos_dependencies_archive():
    with pytest.raises(TypeError) as error_info:
        NotebookOp(name="test",
                   notebook="test_notebook.ipynb",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   image="test/image:dev")


def test_fail_without_runtime_image():
    with pytest.raises(ValueError) as error_info:
        NotebookOp(name="test",
                   notebook="test_notebook.ipynb",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz")


def test_fail_without_notebook():
    with pytest.raises(TypeError) as error_info:
        NotebookOp(name="test",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


def test_fail_without_name():
    with pytest.raises(TypeError) as error_info:
        NotebookOp(notebook="test_notebook.ipynb",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


def test_fail_with_empty_string_as_name():
    with pytest.raises(ValueError) as error_info:
        NotebookOp(name="",
                   notebook="test_notebook.ipynb",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


def test_fail_with_empty_string_as_notebook():
    with pytest.raises(Exception) as error_info:
        NotebookOp(name="test",
                   notebook="",
                   cos_endpoint="http://testserver:32525",
                   cos_bucket="test_bucket",
                   cos_directory="test_directory",
                   cos_dependencies_archive="test_archive.tgz",
                   image="test/image:dev")


@pytest.mark.skip(reason="not sure if we should even test this")
def test_default_bootstrap_url(notebook_op):
    assert notebook_op.bootstrap_script_url == 'https://raw.githubusercontent.com/elyra-ai/kfp-notebook/' \
                                                'v0.9.1/etc/docker-scripts/bootstrapper.py'


def test_override_bootstrap_url():
    notebook_op = NotebookOp(name="test",
                             bootstrap_script_url="https://test.server.com/bootscript.py",
                             notebook="test_notebook.ipynb",
                             cos_endpoint="http://testserver:32525",
                             cos_bucket="test_bucket",
                             cos_directory="test_directory",
                             cos_dependencies_archive="test_archive.tgz",
                             image="test/image:dev")
    assert notebook_op.bootstrap_script_url == "https://test.server.com/bootscript.py"


@pytest.mark.skip(reason="not sure if we should even test this")
def test_default_requirements_url(notebook_op):
    assert notebook_op.requirements_url == 'https://raw.githubusercontent.com/elyra-ai/' \
                                            'kfp-notebook/v0.9.1/etc/requirements-elyra.txt'


def test_override_requirements_url():
    notebook_op = NotebookOp(name="test",
                             requirements_url="https://test.server.com/requirements.py",
                             notebook="test_notebook.ipynb",
                             cos_endpoint="http://testserver:32525",
                             cos_bucket="test_bucket",
                             cos_directory="test_directory",
                             cos_dependencies_archive="test_archive.tgz",
                             image="test/image:dev")
    assert notebook_op.requirements_url == "https://test.server.com/requirements.py"


def test_construct_with_both_pipeline_inputs_and_outputs():
    notebook_op = NotebookOp(name="test",
                             notebook="test_notebook.ipynb",
                             cos_endpoint="http://testserver:32525",
                             cos_bucket="test_bucket",
                             cos_directory="test_directory",
                             cos_dependencies_archive="test_archive.tgz",
                             pipeline_inputs="test_input1.txt,test_input2.txt",
                             pipeline_outputs="test_output1.txt,test_output2.txt",
                             image="test/image:dev")
    assert notebook_op.pipeline_inputs == "test_input1.txt,test_input2.txt"
    assert notebook_op.pipeline_outputs == "test_output1.txt,test_output2.txt"


def test_construct_with_only_pipeline_inputs():
    notebook_op = NotebookOp(name="test",
                             notebook="test_notebook.ipynb",
                             cos_endpoint="http://testserver:32525",
                             cos_bucket="test_bucket",
                             cos_directory="test_directory",
                             cos_dependencies_archive="test_archive.tgz",
                             pipeline_inputs="test_input1.txt,test_input2.txt",
                             image="test/image:dev")
    assert notebook_op.pipeline_inputs == "test_input1.txt,test_input2.txt"


def test_construct_with_only_pipeline_outputs():
    notebook_op = NotebookOp(name="test",
                             notebook="test_notebook.ipynb",
                             cos_endpoint="http://testserver:32525",
                             cos_bucket="test_bucket",
                             cos_directory="test_directory",
                             cos_dependencies_archive="test_archive.tgz",
                             pipeline_outputs="test_output1.txt,test_output2.txt",
                             image="test/image:dev")
    assert notebook_op.pipeline_outputs == "test_output1.txt,test_output2.txt"


def test_add_pipeline_inputs(notebook_op):
    notebook_op.add_pipeline_inputs("test_input1.txt")
    assert '--inputs "test_input1.txt"' in notebook_op.container.args[0]


def test_add_pipeline_outputs(notebook_op):
    notebook_op.add_pipeline_outputs("test_output1.txt")
    assert '--outputs "test_output1.txt"' in notebook_op.container.args[0]


def test_add_env_variable(notebook_op):
    notebook_op.add_environment_variable("ENV_VAR_ONE", "1")
    env_var = notebook_op.container.env.pop()
    assert env_var.name == "ENV_VAR_ONE"
    assert env_var.value == "1"
