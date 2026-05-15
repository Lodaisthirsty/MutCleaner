import pytest
import tempfile
from pathlib import Path
import pickle
import warnings

from mutcleaner.core.pipeline import (
    Pipeline,
    create_pipeline,
    pipeline_step,
    PipelineOutput,
    multiout_step,
)


class TestSimplifiedPipelineInit:
    """Test simplified Pipeline initialization"""

    def test_pipeline_creation_with_data(self):
        """Test pipeline creation with initial data"""
        data = [1, 2, 3]
        pipeline = Pipeline(data, name="test_pipeline")

        assert pipeline.name == "test_pipeline"
        assert pipeline.data == [1, 2, 3]  # Always returns the actual data
        assert pipeline.artifacts == {}  # Always returns a dictionary
        assert pipeline.steps == []
        assert pipeline.results == []

    def test_pipeline_creation_without_data(self):
        """Test pipeline creation without initial data"""
        pipeline = Pipeline(name="empty_pipeline")

        assert pipeline.name == "empty_pipeline"
        assert pipeline.data is None
        assert pipeline.artifacts == {}

    def test_create_pipeline_helper(self):
        """Test the create_pipeline helper function"""
        data = {"key": "value"}
        pipeline = create_pipeline(data, name="helper_test")

        assert isinstance(pipeline, Pipeline)
        assert pipeline.name == "helper_test"
        assert pipeline.data == {"key": "value"}


class TestSimplifiedPipelineProperties:
    """Test simplified Pipeline properties"""

    def test_data_property_always_returns_actual_data(self):
        """Test that the data property always returns the actual data"""
        # At initialization
        pipeline = Pipeline([1, 2, 3])
        assert pipeline.data == [1, 2, 3]
        assert isinstance(pipeline.data, list)

        # List methods can be called directly
        copied_data = pipeline.data.copy()
        assert copied_data == [1, 2, 3]

        # After the data changes
        def double(data):
            return [x * 2 for x in data]

        pipeline.then(double)
        assert pipeline.data == [2, 4, 6]
        assert isinstance(pipeline.data, list)

    def test_artifacts_property_always_returns_dict(self):
        """Test that the artifacts property always returns a dictionary"""
        pipeline = Pipeline([1, 2, 3])

        # Initially an empty dictionary
        assert pipeline.artifacts == {}
        assert isinstance(pipeline.artifacts, dict)

        # After adding an artifact
        @multiout_step(stats="statistics")
        def analyze(data):
            return [x * 2 for x in data], {"count": len(data)}

        pipeline.then(analyze)

        assert "analyze.statistics" in pipeline.artifacts
        assert pipeline.artifacts["analyze.statistics"]["count"] == 3
        assert isinstance(pipeline.artifacts, dict)

    def test_structured_data_property_returns_pipeline_output(self):
        """Test that structured_data returns a PipelineOutput object"""
        pipeline = Pipeline([1, 2, 3])

        # Initially
        structured = pipeline.structured_data
        assert isinstance(structured, PipelineOutput)
        assert structured.data == [1, 2, 3]
        assert structured.artifacts == {}

        # After adding an artifact
        @multiout_step(stats="statistics")
        def analyze(data):
            return [x * 2 for x in data], {"count": len(data)}

        pipeline.then(analyze)

        structured = pipeline.structured_data
        assert isinstance(structured, PipelineOutput)
        assert structured.data == [2, 4, 6]
        assert "analyze.statistics" in structured.artifacts

    def test_consistent_user_experience(self):
        """Test a consistent user experience"""
        pipeline = Pipeline([1, 2, 3])

        # These operations should work at any time
        original_data = pipeline.data.copy()  # Always callable
        artifacts_keys = list(pipeline.artifacts.keys())  # Always callable

        @multiout_step(stats="statistics")
        def analyze(data):
            return [x * 2 for x in data], {"count": len(data)}

        pipeline.then(analyze)

        # After execution, the same access pattern should still work
        new_data = pipeline.data.copy()  # Still callable
        artifacts_keys = list(pipeline.artifacts.keys())  # Still callable

        assert len(new_data) == 3
        assert len(artifacts_keys) == 1


class TestSimplifiedPipelineBasicOperations:
    """Test basic operations of the simplified Pipeline"""

    def test_then_with_simple_function(self):
        """Test the then method with a simple function"""

        def double(x):
            return [item * 2 for item in x]

        pipeline = Pipeline([1, 2, 3])
        result_pipeline = pipeline.then(double)

        assert result_pipeline is pipeline  # Returns itself
        assert pipeline.data == [2, 4, 6]
        assert len(pipeline.steps) == 1
        assert len(pipeline.results) == 1
        assert pipeline.steps[0].success is True

    def test_then_chaining(self):
        """Test method chaining"""

        def add_one(data):
            return [x + 1 for x in data]

        def multiply_by_two(data):
            return [x * 2 for x in data]

        pipeline = Pipeline([1, 2, 3])
        result = pipeline.then(add_one).then(multiply_by_two)

        assert result is pipeline
        assert pipeline.data == [4, 6, 8]  # (1+1)*2, (2+1)*2, (3+1)*2
        assert len(pipeline.steps) == 2
        assert all(step.success for step in pipeline.steps)

    def test_pipeline_step_decorator_integration(self):
        """Test @pipeline_step decorator integration"""

        @pipeline_step(name="process_data")
        def process_list(data):
            """Process the input list"""
            return [x * 3 for x in data]

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(process_list)

        assert pipeline.data == [3, 6, 9]
        assert pipeline.steps[0].name == "process_data"
        assert hasattr(process_list, "_is_pipeline_step")
        assert getattr(process_list, "_step_type") == "single_output"

    def test_multiout_step_decorator_integration(self):
        """Test @multiout_step decorator integration"""

        @multiout_step(stats="statistics", metadata="info")
        def analyze_data(data):
            """Analyze data with statistics"""
            processed = [x * 2 for x in data]
            stats = {"count": len(processed), "sum": sum(processed)}
            metadata = {"processed_at": "2024-01-01"}
            return processed, stats, metadata

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(analyze_data)

        # Main data flow
        assert pipeline.data == [2, 4, 6]

        # Side outputs are stored in artifacts
        assert "analyze_data.statistics" in pipeline.artifacts
        assert "analyze_data.info" in pipeline.artifacts
        assert pipeline.artifacts["analyze_data.statistics"]["count"] == 3
        assert pipeline.artifacts["analyze_data.info"]["processed_at"] == "2024-01-01"

    def test_multiout_step_with_explicit_main(self):
        """Test @multiout_step with an explicit main output"""

        @multiout_step(main="result", errors="error_list", warnings="warning_list")
        def comprehensive_process(data):
            result = [x + 1 for x in data]
            errors = []
            warnings = ["minor issue"]
            return result, errors, warnings

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(comprehensive_process)

        assert pipeline.data == [2, 3, 4]
        assert "comprehensive_process.error_list" in pipeline.artifacts
        assert "comprehensive_process.warning_list" in pipeline.artifacts
        assert pipeline.artifacts["comprehensive_process.error_list"] == []
        assert pipeline.artifacts["comprehensive_process.warning_list"] == [
            "minor issue"
        ]


class TestSimplifiedPipelineUtilityMethods:
    """Test utility methods of the simplified Pipeline"""

    def test_peek_method(self):
        """Test the peek method"""

        def double_data(data):
            return [x * 2 for x in data]

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(double_data)

        # Record the data state for comparison
        original_data = pipeline.data.copy()  # This should now always work
        result = pipeline.peek()

        assert result is pipeline
        assert pipeline.data == original_data  # Data is not modified
        assert pipeline.data == [2, 4, 6]

    def test_peek_with_custom_function(self):
        """Test the peek method with a custom function"""
        captured_data = []

        def capture_data(data):
            captured_data.append(data.copy())

        pipeline = Pipeline([1, 2, 3])
        pipeline.peek(capture_data)

        assert captured_data == [[1, 2, 3]]
        assert pipeline.data == [1, 2, 3]  # Data is unchanged

    def test_store_method(self):
        """Test storing an artifact with the store method"""

        def double_data(data):
            return [x * 2 for x in data]

        def extract_sum(data):
            return sum(data)

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(double_data).store("doubled_sum", extract_sum)

        assert "doubled_sum" in pipeline.artifacts
        assert pipeline.artifacts["doubled_sum"] == 12  # sum([2, 4, 6])

    def test_get_artifact_method(self):
        """Test the get_artifact method"""

        @multiout_step(stats="statistics")
        def process_with_stats(data):
            return [x * 2 for x in data], {"count": len(data)}

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(process_with_stats)

        stats = pipeline.get_artifact("process_with_stats.statistics")
        assert stats == {"count": 3}

        with pytest.raises(KeyError, match="Artifact 'nonexistent' not found"):
            pipeline.get_artifact("nonexistent")

    def test_get_all_artifacts_method(self):
        """Test the get_all_artifacts method"""

        @multiout_step(stats="statistics", info="metadata")
        def process_data(data):
            return data, {"count": len(data)}, {"type": "test"}

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(process_data)

        all_artifacts = pipeline.get_all_artifacts()

        assert isinstance(all_artifacts, dict)
        assert "process_data.statistics" in all_artifacts
        assert "process_data.metadata" in all_artifacts
        assert all_artifacts["process_data.statistics"]["count"] == 3

        # Verify that the returned object is a copy
        all_artifacts["new_key"] = "new_value"
        assert "new_key" not in pipeline.artifacts

    def test_copy_method(self):
        """Test the copy method"""

        @multiout_step(stats="statistics")
        def process_data(data):
            return [x * 2 for x in data], {"count": len(data)}

        original = Pipeline([1, 2, 3], name="original")
        original.then(process_data)

        copied = original.copy()

        assert copied is not original
        assert copied.name == "original_copy"
        assert copied.data == [2, 4, 6]  # Data is copied
        assert copied.artifacts == original.artifacts  # Artifacts are copied
        assert copied.steps == []  # Steps are not copied
        assert copied.results == []  # Results are not copied

    def test_get_execution_summary(self):
        """Test retrieving the execution summary"""

        @pipeline_step(name="step1")
        def successful_step(data):
            return [x + 1 for x in data]

        def failing_step(data):
            raise ValueError("Test error")

        pipeline = Pipeline([1, 2, 3], name="test_pipeline")
        pipeline.then(successful_step)

        try:
            pipeline.then(failing_step)
        except RuntimeError:
            pass

        summary = pipeline.get_execution_summary()

        assert summary["pipeline_name"] == "test_pipeline"
        assert summary["total_steps"] == 2
        assert summary["successful_steps"] == 1
        assert summary["failed_steps"] == 1
        assert summary["total_execution_time"] > 0
        assert len(summary["steps"]) == 2
        assert summary["steps"][0]["success"] is True
        assert summary["steps"][1]["success"] is False

    def test_visualize_pipeline(self):
        """Test pipeline visualization"""

        @pipeline_step(name="process_data")
        def process_data(data):
            """Process the input data"""
            return [x * 2 for x in data]

        pipeline = Pipeline([1, 2, 3], name="viz_test")
        pipeline.then(process_data)

        visualization = pipeline.visualize_pipeline()

        assert "Pipeline: viz_test" in visualization
        assert "✓ Step 1: process_data" in visualization
        assert "[validated]" in visualization
        assert "Process the input data" in visualization
        assert "Current data type: list" in visualization

    def test_str_and_repr_methods(self):
        """Test string representation methods"""

        @multiout_step(stats="statistics")
        def process_data(data):
            return data, {"count": len(data)}

        pipeline = Pipeline([1, 2, 3], name="test_pipe")
        pipeline.then(process_data)

        str_repr = str(pipeline)
        assert "Pipeline('test_pipe')" in str_repr
        assert "1/1 steps executed" in str_repr
        assert "1 artifacts" in str_repr

        repr_str = repr(pipeline)
        assert "<Pipeline name='test_pipe'" in repr_str
        assert "steps=1" in repr_str
        assert "data_type=list" in repr_str
        assert "artifacts=1" in repr_str


class TestSimplifiedPipelineFileOperations:
    """Test file operations of the simplified Pipeline"""

    def test_save_and_load_data(self):
        """Test saving and loading data"""
        pipeline = Pipeline([1, 2, 3], name="save_test")

        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            temp_path = f.name

        try:
            # Save data
            result = pipeline.save(temp_path, format="pickle")
            assert result is pipeline

            # Load data
            loaded_pipeline = Pipeline.load(
                temp_path, format="pickle", name="loaded_test"
            )
            assert loaded_pipeline.data == [1, 2, 3]
            assert loaded_pipeline.name == "loaded_test"

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_save_and_load_artifacts(self):
        """Test saving and loading artifacts"""

        @multiout_step(stats="statistics")
        def process_data(data):
            return data, {"count": len(data), "sum": sum(data)}

        pipeline = Pipeline([1, 2, 3])
        pipeline.then(process_data)

        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            temp_path = f.name

        try:
            result = pipeline.save_artifacts(temp_path, format="pickle")
            assert result is pipeline

            # Verify that artifacts are saved
            with open(temp_path, "rb") as f:
                loaded_artifacts = pickle.load(f)

            assert "process_data.statistics" in loaded_artifacts
            assert loaded_artifacts["process_data.statistics"]["count"] == 3

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_save_and_load_structured_data(self):
        """Test saving and loading structured data"""

        @multiout_step(stats="statistics")
        def process_data(data):
            return [x * 2 for x in data], {"count": len(data)}

        pipeline = Pipeline([1, 2, 3], name="structured_test")
        pipeline.then(process_data)

        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            temp_path = f.name

        try:
            # Save structured data
            result = pipeline.save_structured_data(temp_path, format="pickle")
            assert result is pipeline

            # Load structured data
            loaded_pipeline = Pipeline.load_structured_data(
                temp_path, format="pickle", name="loaded_structured"
            )
            assert loaded_pipeline.data == [2, 4, 6]
            assert "process_data.statistics" in loaded_pipeline.artifacts
            assert loaded_pipeline.artifacts["process_data.statistics"]["count"] == 3

        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_save_structured_data_json(self):
        """Test saving and loading structured data in JSON format"""
        pipeline = Pipeline({"numbers": [1, 2, 3]}, name="json_test")
        pipeline.store("metadata", lambda data: {"type": "dict"})

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            # Save as JSON
            pipeline.save_structured_data(temp_path, format="json")

            # Load JSON
            loaded_pipeline = Pipeline.load_structured_data(temp_path, format="json")
            assert loaded_pipeline.data == {"numbers": [1, 2, 3]}
            assert "metadata" in loaded_pipeline.artifacts
            assert loaded_pipeline.artifacts["metadata"]["type"] == "dict"

        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestSimplifiedPipelineAdvancedFeatures:
    """Test advanced features of the simplified Pipeline"""

    def test_filter_method(self):
        """Test the filter method"""
        pipeline = Pipeline([1, 2, 3, 4, 5])

        # Filter even numbers
        result = pipeline.filter(lambda x: x % 2 == 0)

    def test_assign_method_with_dict(self):
        """Test the assign method with dictionary data"""
        pipeline = Pipeline({"a": 1, "b": 2})
        result = pipeline.assign(c=3, d=4)

        assert result is pipeline
        assert pipeline.data == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_validate_method_success(self):
        """Test the successful validate method case"""

        def is_positive_list(data):
            return all(x > 0 for x in data)

        pipeline = Pipeline([1, 2, 3])
        result = pipeline.validate(is_positive_list, "All numbers must be positive")

        assert result is pipeline
        assert pipeline.data == [1, 2, 3]

    def test_validate_method_failure(self):
        """Test the failing validate method case"""

        def is_positive_list(data):
            return all(x > 0 for x in data)

        pipeline = Pipeline([-1, 2, 3])

        with pytest.raises(RuntimeError, match="All numbers must be positive"):
            pipeline.validate(is_positive_list, "All numbers must be positive")

    def test_apply_method_functional_style(self):
        """Test the functional style of the apply method"""

        def double(data):
            return [x * 2 for x in data]

        original = Pipeline([1, 2, 3])
        new_pipeline = original.apply(double)

        # The original pipeline is unchanged
        assert original.data == [1, 2, 3]

        # The new pipeline is updated
        assert new_pipeline.data == [2, 4, 6]
        assert new_pipeline is not original
        assert new_pipeline.name == "Pipeline_copy"

    def test_complex_pipeline_workflow(self):
        """Test a complex pipeline workflow"""

        @pipeline_step(name="normalize")
        def normalize(data):
            """Normalize data to 0-1 range"""
            max_val = max(data)
            return [x / max_val for x in data]

        @multiout_step(stats="statistics", summary="summary")
        def analyze(data):
            """Analyze normalized data"""
            processed = [round(x, 2) for x in data]
            stats = {"mean": sum(data) / len(data), "max": max(data), "min": min(data)}
            summary = f"Processed {len(data)} items"
            return processed, stats, summary

        # Build a complex pipeline
        pipeline = (
            Pipeline([10, 20, 30, 40, 50], name="complex_workflow")
            .then(normalize)
            .store("normalized", lambda data: data.copy())
            .then(analyze)
            .store("final_result")
        )

        # Verify the main data flow
        assert pipeline.data == [0.2, 0.4, 0.6, 0.8, 1.0]

        # Verify artifacts
        assert "normalized" in pipeline.artifacts
        assert "analyze.statistics" in pipeline.artifacts
        assert "analyze.summary" in pipeline.artifacts
        assert "final_result" in pipeline.artifacts

        # Verify statistics
        stats = pipeline.artifacts["analyze.statistics"]
        assert stats["max"] == 1.0
        assert stats["min"] == 0.2

        # Verify structured data
        structured = pipeline.structured_data
        assert isinstance(structured, PipelineOutput)
        assert structured.data == pipeline.data
        assert len(structured.artifacts) == 4

        # Verify visualization
        viz = pipeline.visualize_pipeline()
        assert "complex_workflow" in viz
        assert "normalize" in viz
        assert "analyze" in viz


class TestSimplifiedPipelineErrorHandling:
    """Test error handling of the simplified Pipeline"""

    def test_step_execution_failure(self):
        """Test step execution failure"""

        def failing_function(data):
            raise ValueError("Processing failed")

        pipeline = Pipeline([1, 2, 3])

        with pytest.raises(
            RuntimeError, match="Pipeline failed at step 'failing_function'"
        ):
            pipeline.then(failing_function)

        assert len(pipeline.steps) == 1
        assert pipeline.steps[0].success is False
        assert isinstance(pipeline.steps[0].error, ValueError)

    def test_multiout_step_wrong_return_count(self):
        """Test an incorrect number of return values from multiout_step"""

        @multiout_step(stats="statistics", metadata="info")  # Expect 3 values
        def wrong_return_count(data):
            return data, {"count": len(data)}  # Returns only 2 values

        pipeline = Pipeline([1, 2, 3])

        with pytest.raises(RuntimeError, match="expected 3 return values but got 2"):
            pipeline.then(wrong_return_count)

    def test_no_data_error(self):
        """Test the error raised when no data is available"""
        pipeline = Pipeline()

        def dummy_func(x):
            return x

        with pytest.raises(ValueError, match="No data to process"):
            pipeline.then(dummy_func)

    def test_undecorated_function_warning(self):
        """Test that an undecorated function emits a warning"""

        def undecorated_func(data):
            return [x * 2 for x in data]

        pipeline = Pipeline([1, 2, 3])

        with pytest.warns(UserWarning, match="is not decorated with @pipeline_step"):
            pipeline.then(undecorated_func)

        assert pipeline.data == [2, 4, 6]  # The function still works correctly


class TestDelayedPipeline:
    """Test delayed execution features of Pipeline"""

    def test_delayed_then_does_not_execute_immediately(self):
        """Test that delayed_then does not execute steps immediately"""
        pipeline = Pipeline([1, 2, 3])

        def double(data):
            return [x * 2 for x in data]

        # Add a delayed step; data should not change
        pipeline.delayed_then(double)

        assert pipeline.data == [1, 2, 3]  # Data is unchanged
        assert len(pipeline.delayed_steps) == 1  # There is one delayed step
        assert len(pipeline.steps) == 0  # There are no executed steps
        assert pipeline.has_pending_steps is True

    def test_execute_runs_delayed_steps(self):
        """Test that execute runs delayed steps"""
        pipeline = Pipeline([1, 2, 3])

        def double(data):
            return [x * 2 for x in data]

        def add_one(data):
            return [x + 1 for x in data]

        # Add delayed steps
        pipeline.delayed_then(double).delayed_then(add_one)

        assert pipeline.data == [1, 2, 3]  # Data is unchanged before execution
        assert len(pipeline.delayed_steps) == 2

        # Execute all delayed steps
        result = pipeline.execute()

        assert result is pipeline  # Return self for method chaining
        assert pipeline.data == [3, 5, 7]  # (1*2)+1, (2*2)+1, (3*2)+1
        assert len(pipeline.delayed_steps) == 0  # Delayed steps have been cleared
        assert len(pipeline.steps) == 2  # There are now 2 executed steps
        assert pipeline.has_pending_steps is False

    def test_execute_with_step_count(self):
        """Test that execute runs a specified number of steps"""
        pipeline = Pipeline([1, 2, 3])

        def double(data):
            return [x * 2 for x in data]

        def add_one(data):
            return [x + 1 for x in data]

        def multiply_by_three(data):
            return [x * 3 for x in data]

        # Add 3 delayed steps
        pipeline.delayed_then(double).delayed_then(add_one).delayed_then(
            multiply_by_three
        )

        # Run only the first 2 steps
        pipeline.execute(2)

        assert pipeline.data == [3, 5, 7]  # Only double and add_one were executed
        assert len(pipeline.delayed_steps) == 1  # There is 1 delayed step left
        assert len(pipeline.steps) == 2  # Executed 2 steps

        # Execute the remaining steps
        pipeline.execute()

        assert pipeline.data == [9, 15, 21]  # multiply_by_three is executed last
        assert len(pipeline.delayed_steps) == 0

    def test_execute_with_specific_indices(self):
        """Test that execute runs steps at specified indices"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return [x + 10 for x in data]

        def step2(data):
            return [x * 2 for x in data]

        def step3(data):
            return [x - 5 for x in data]

        # Add 3 delayed steps
        pipeline.delayed_then(step1).delayed_then(step2).delayed_then(step3)

        # Execute steps 0 and 2, skipping step 1
        pipeline.execute([0, 2])

        assert len(pipeline.delayed_steps) == 1  # There is 1 delayed step left: step2
        assert len(pipeline.steps) == 2  # Executed 2 steps

        # Verify the execution order: step1 first, then step3
        # [1,2,3] -> step1 -> [11,12,13] -> step3 -> [6,7,8]
        assert pipeline.data == [6, 7, 8]

    def test_execute_all(self):
        """Test execute_all"""
        pipeline = Pipeline([1, 2, 3])

        def double(data):
            return [x * 2 for x in data]

        pipeline.delayed_then(double)
        pipeline.execute()

        assert pipeline.data == [2, 4, 6]
        assert len(pipeline.delayed_steps) == 0

    def test_mixed_usage_warning(self):
        """Test the warning when mixing delayed_then and then"""
        pipeline = Pipeline([1, 2, 3])

        @pipeline_step
        def double(data):
            return [x * 2 for x in data]

        @pipeline_step
        def add_one(data):
            return [x + 1 for x in data]

        # Add delayed steps
        pipeline.delayed_then(double)

        # Using then should emit a warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            pipeline.then(add_one)

            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "pending delayed steps" in str(w[0].message)

        # Verify the execution result: then executes immediately using the original data
        assert pipeline.data == [2, 3, 4]  # [1,2,3] + 1
        assert len(pipeline.delayed_steps) == 1  # Delayed steps still exist

    def test_has_pending_steps_property(self):
        """Test the has_pending_steps property"""
        pipeline = Pipeline([1, 2, 3])

        # Initial state
        assert pipeline.has_pending_steps is False

        # Add delayed steps
        pipeline.delayed_then(lambda x: x)
        assert pipeline.has_pending_steps is True

        # Execute delayed steps
        pipeline.execute()
        assert pipeline.has_pending_steps is False

        # Clear delayed steps
        pipeline.delayed_then(lambda x: x)
        assert pipeline.has_pending_steps is True

    def test_get_delayed_steps_info(self):
        """Test retrieving delayed step information"""
        pipeline = Pipeline([1, 2, 3])

        @pipeline_step
        def decorated_step(data):
            return data

        def regular_step(data):
            return data

        # Add different types of steps
        pipeline.delayed_then(decorated_step)
        pipeline.delayed_then(regular_step)

        info = pipeline.get_delayed_steps_info()

        assert len(info) == 2

        # Check the first decorated step
        assert info[0]["index"] == 0
        assert info[0]["name"] == "decorated_step"
        assert info[0]["is_pipeline_step"] is True
        assert info[0]["step_type"] == "single_output"

        # Check the second regular function step
        assert info[1]["index"] == 1
        assert info[1]["name"] == "regular_step"
        assert info[1]["is_pipeline_step"] is False
        assert info[1]["step_type"] == "unknown"

    def test_visualize_pipeline_with_delayed_steps(self):
        """Test pipeline visualization with delayed steps"""
        pipeline = Pipeline([1, 2, 3], name="TestPipeline")

        def executed_step(data):
            return [x * 2 for x in data]

        @pipeline_step
        def delayed_step(data):
            """This is a delayed step"""
            return data

        # Execute one step and add one delayed step
        pipeline.then(executed_step)
        pipeline.delayed_then(delayed_step)

        visualization = pipeline.visualize_pipeline()

        # Check the key information included
        assert "TestPipeline" in visualization
        assert "executed_step" in visualization
        assert "Delayed Steps:" in visualization
        assert "delayed_step" in visualization
        assert "This is a delayed step" in visualization
        assert "Delayed steps: 1" in visualization
        assert "✓" in visualization  # Successful execution marker
        assert "⏸" in visualization  # Delayed step marker

    def test_execution_summary_with_delayed_steps(self):
        """Test the execution summary with delayed steps"""
        pipeline = Pipeline([1, 2, 3], name="TestPipeline")

        def step1(data):
            return [x * 2 for x in data]

        def step2(data):
            return [x + 1 for x in data]

        # Execute one step and add one delayed step
        pipeline.then(step1)
        pipeline.delayed_then(step2)

        summary = pipeline.get_execution_summary()

        assert summary["pipeline_name"] == "TestPipeline"
        assert summary["total_steps"] == 1  # Executed steps
        assert summary["delayed_steps"] == 1  # Delayed steps
        assert summary["successful_steps"] == 1
        assert summary["failed_steps"] == 0
        assert len(summary["delayed_steps_info"]) == 1
        assert summary["delayed_steps_info"][0]["name"] == "step2"

    def test_copy_preserves_delayed_steps(self):
        """Test that copy preserves delayed steps"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return [x * 2 for x in data]

        def step2(data):
            return [x + 1 for x in data]

        # Add delayed steps
        pipeline.delayed_then(step1).delayed_then(step2)

        # Copy the pipeline
        copied = pipeline.copy()

        assert len(copied.delayed_steps) == 2
        assert copied.has_pending_steps is True
        assert copied.data == [1, 2, 3]

        # The original and copied pipelines should be independent
        pipeline.execute()
        assert pipeline.data == [3, 5, 7]
        assert copied.data == [1, 2, 3]  # The copied pipeline data is unchanged

    def test_str_and_repr_with_delayed_steps(self):
        """Test string representations with delayed steps"""
        pipeline = Pipeline([1, 2, 3], name="TestPipeline")

        def step1(data):
            return data

        # Execute one step and add a delayed step
        pipeline.then(step1)
        pipeline.delayed_then(step1)

        str_repr = str(pipeline)
        repr_str = repr(pipeline)

        assert "TestPipeline" in str_repr
        assert "1/1 steps executed" in str_repr
        assert "1 delayed" in str_repr

        assert "TestPipeline" in repr_str
        assert "steps=1" in repr_str
        assert "delayed=1" in repr_str

    def test_pipeline_step_decorator_with_delayed_execution(self):
        """Test decorator behavior during delayed execution"""
        pipeline = Pipeline([1, 2, 3])

        @pipeline_step
        def double_values(data):
            """Double all values in the list"""
            return [x * 2 for x in data]

        @multiout_step(stats="statistics")
        def analyze_data(data):
            """Analyze data and return stats"""
            total = sum(data)
            return data, {"sum": total, "count": len(data)}

        # Use delayed execution
        pipeline.delayed_then(double_values)
        pipeline.delayed_then(analyze_data)

        # Execute delayed steps
        pipeline.execute()

        assert pipeline.data == [2, 4, 6]
        assert "analyze_data.statistics" in pipeline.artifacts
        assert pipeline.artifacts["analyze_data.statistics"]["sum"] == 12
        assert pipeline.artifacts["analyze_data.statistics"]["count"] == 3

    def test_error_handling_in_delayed_execution(self):
        """Test error handling during delayed execution"""
        pipeline = Pipeline([1, 2, 3])

        def working_step(data):
            return [x * 2 for x in data]

        def failing_step(data):
            raise ValueError("Intentional error")

        # Add a working step and a failing step
        pipeline.delayed_then(working_step)
        pipeline.delayed_then(failing_step)

        # Execution should fail at the second step
        with pytest.raises(RuntimeError) as exc_info:
            pipeline.execute()

        assert "Pipeline failed at delayed step 'failing_step'" in str(exc_info.value)

        # The first step should have executed successfully
        assert len(pipeline.steps) == 2
        assert pipeline.steps[0].success is True
        assert pipeline.steps[1].success is False
        assert pipeline.data == [2, 4, 6]  # Result from the first step

    def test_add_delayed_step_at_end(self):
        """Test adding a delayed step at the end by default"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return [x * 2 for x in data]

        def step2(data):
            return [x + 1 for x in data]

        def step3(data):
            return [x * 3 for x in data]

        # Add two steps first
        pipeline.delayed_then(step1).delayed_then(step2)

        # Add the third step at the end
        pipeline.add_delayed_step(step3)

        assert len(pipeline.delayed_steps) == 3
        assert pipeline.delayed_steps[0].name == "step1"
        assert pipeline.delayed_steps[1].name == "step2"
        assert pipeline.delayed_steps[2].name == "step3"

        # Execute and verify the order
        pipeline.execute()
        # [1,2,3] -> *2 -> [2,4,6] -> +1 -> [3,5,7] -> *3 -> [9,15,21]
        assert pipeline.data == [9, 15, 21]

    def test_add_delayed_step_at_beginning(self):
        """Test inserting a delayed step at the beginning"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return [x * 2 for x in data]

        def step2(data):
            return [x + 1 for x in data]

        def step0(data):  # Step to insert at the beginning
            return [x + 10 for x in data]

        # Add two steps first
        pipeline.delayed_then(step1).delayed_then(step2)

        # Insert a step at the beginning
        pipeline.add_delayed_step(step0, 0)

        assert len(pipeline.delayed_steps) == 3
        assert pipeline.delayed_steps[0].name == "step0"
        assert pipeline.delayed_steps[1].name == "step1"
        assert pipeline.delayed_steps[2].name == "step2"

        # Execute and verify the order
        pipeline.execute()
        # [1,2,3] -> +10 -> [11,12,13] -> *2 -> [22,24,26] -> +1 -> [23,25,27]
        assert pipeline.data == [23, 25, 27]

    def test_add_delayed_step_at_middle(self):
        """Test inserting a delayed step in the middle"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return [x * 2 for x in data]

        def step2(data):
            return [x + 1 for x in data]

        def step_middle(data):
            return [x + 100 for x in data]

        # Add two steps first
        pipeline.delayed_then(step1).delayed_then(step2)

        # Insert a step in the middle
        pipeline.add_delayed_step(step_middle, 1)

        assert len(pipeline.delayed_steps) == 3
        assert pipeline.delayed_steps[0].name == "step1"
        assert pipeline.delayed_steps[1].name == "step_middle"
        assert pipeline.delayed_steps[2].name == "step2"

        # Execute and verify the order
        pipeline.execute()
        # [1,2,3] -> *2 -> [2,4,6] -> +100 -> [102,104,106] -> +1 -> [103,105,107]
        assert pipeline.data == [103, 105, 107]

    def test_add_delayed_step_negative_index(self):
        """Test inserting a delayed step with a negative index"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return [x * 2 for x in data]

        def step2(data):
            return [x + 1 for x in data]

        def step_before_last(data):
            return [x + 100 for x in data]

        # Add two steps first
        pipeline.delayed_then(step1).delayed_then(step2)

        # Insert at the last position, before step2
        pipeline.add_delayed_step(step_before_last, -1)

        assert len(pipeline.delayed_steps) == 3
        assert pipeline.delayed_steps[0].name == "step1"
        assert pipeline.delayed_steps[1].name == "step_before_last"
        assert pipeline.delayed_steps[2].name == "step2"

    def test_add_delayed_step_out_of_bounds(self):
        """Test that an out-of-bounds index is adjusted automatically"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return data

        def step2(data):
            return data

        # Add one step first
        pipeline.delayed_then(step1)

        # Try inserting at an out-of-bounds position; it should be adjusted to the end
        pipeline.add_delayed_step(step2, 100)

        assert len(pipeline.delayed_steps) == 2
        assert pipeline.delayed_steps[1].name == "step2"

    def test_remove_delayed_step_by_index(self):
        """Test removing a delayed step by index"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return data

        def step2(data):
            return data

        def step3(data):
            return data

        # Add three steps
        pipeline.delayed_then(step1).delayed_then(step2).delayed_then(step3)

        # Remove the middle step
        pipeline.remove_delayed_step(1)

        assert len(pipeline.delayed_steps) == 2
        assert pipeline.delayed_steps[0].name == "step1"
        assert pipeline.delayed_steps[1].name == "step3"

    def test_remove_delayed_step_by_name(self):
        """Test removing a delayed step by name"""
        pipeline = Pipeline([1, 2, 3])

        def step1(data):
            return data

        @pipeline_step(name="custom_name")
        def step2(data):
            return data

        def step3(data):
            return data

        # Add three steps
        pipeline.delayed_then(step1).delayed_then(step2).delayed_then(step3)

        # Remove the step by name
        pipeline.remove_delayed_step("custom_name")

        assert len(pipeline.delayed_steps) == 2
        assert pipeline.delayed_steps[0].name == "step1"
        assert pipeline.delayed_steps[1].name == "step3"

    def test_remove_delayed_step_invalid_cases(self):
        """Test invalid cases for removing delayed steps"""
        pipeline = Pipeline([1, 2, 3])

        @pipeline_step
        def step1(data):
            return data

        pipeline.delayed_then(step1)

        # Test a nonexistent name
        with pytest.raises(ValueError):
            pipeline.remove_delayed_step("nonexistent")

        # Test an invalid type
        with pytest.raises(TypeError):
            pipeline.remove_delayed_step(1.5)  # type: ignore

    def test_delayed_step_management_integration(self):
        """Test integrated usage of delayed step management"""
        pipeline = Pipeline([1, 2, 3])

        def multiply(data):
            return [x * 2 for x in data]

        def add(data):
            return [x + 10 for x in data]

        def subtract(data):
            return [x - 5 for x in data]

        def divide(data):
            return [x // 2 for x in data]

        # Build a complex delayed execution sequence
        pipeline.delayed_then(multiply)  # 0: multiply
        pipeline.add_delayed_step(add, 0)  # Insert add at the beginning: [add, multiply]
        pipeline.delayed_then(subtract)  # Append subtract at the end: [add, multiply, subtract]
        pipeline.add_delayed_step(
            divide, 2
        )  # Insert divide at position 2: [add, multiply, divide, subtract]
        # Remove add
        pipeline.remove_delayed_step("add")  # [multiply, divide, subtract]
        # Verify the final execution order
        assert len(pipeline.delayed_steps) == 3
        assert pipeline.delayed_steps[0].name == "multiply"
        assert pipeline.delayed_steps[1].name == "divide"
        assert pipeline.delayed_steps[2].name == "subtract"

        # Execute and verify the result
        pipeline.execute()
        # [1,2,3] -> -5 -> [-4,-3,-2] -> *2 -> [-8,-6,-4] -> //2 -> [-4,-3,-2]
        assert pipeline.data == [-4, -3, -2]

    def test_empty_delayed_steps_execute(self):
        """Test calling execute when there are no delayed steps"""
        pipeline = Pipeline([1, 2, 3])

        # Call execute when there are no delayed steps
        result = pipeline.execute()

        assert result is pipeline
        assert pipeline.data == [1, 2, 3]  # Data is unchanged
        assert len(pipeline.steps) == 0
        assert len(pipeline.delayed_steps) == 0
