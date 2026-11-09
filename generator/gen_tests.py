import yaml
import argparse
from pathlib import Path

TEST_FILE_TEMPLATE = """//
// AUTO-GENERATED TESTS. DO NOT EDIT MANUALLY.
// Source: {spec_source}
// Generator: gen_tests.py v1.0

using System;
using NUnit.Framework;
using Lab.Interfaces;
using Lab.Implementations;

namespace Module.Tests
{{
    [TestFixture]
    [Description("Автоматически сгенерированные тесты для {module_name}")]
    public class {module_name}Tests
    {{
        private I{module_name} _sut;

        [SetUp]
        public void SetUp()
        {{
            _sut = new {module_name}();
        }}

        {test_methods}
    }}
}}
"""

TEST_METHOD_TEMPLATE = """
        [Test]
        [Description("{case_desc}")]
        public void {method_name}_{case_name}()
        {{
            // Arrange
            // Precondition: {pre}

            // Act
            {act_code}

            // Assert
            {assert_code}
        }}
"""

def format_csharp_input(inp):
    if inp == "null": return "null"
    if isinstance(inp, str): return f'"{inp}"'
    return str(inp)

def generate_method_tests(method_data):
    case_blocks = []
    for eq_class in method_data.get("equivalence_classes", []):
        inputs_str = ", ".join(format_csharp_input(inp) for inp in eq_class["inputs"])
        method_name = method_data["name"]
        
        # Генерируем вызов метода
        if method_data["signature"].startswith("void"):
            act_code = f"_sut.{method_name}({inputs_str});"
        else:
            act_code = f"var result = _sut.{method_name}({inputs_str});"
            
        assert_code = 'Assert.Pass("Generated assertion placeholder.");'

        case_name = eq_class["case"].replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(".", "").replace("-", "_").replace(",", "")
        
        case_blocks.append(TEST_METHOD_TEMPLATE.format(
            case_desc=eq_class["case"],
            method_name=method_name,
            case_name=case_name,
            pre=method_data["pre"],
            act_code=act_code,
            assert_code=assert_code
        ))
    return case_blocks

def render_and_save(spec, config):
    module_name = spec["module"]
    test_methods = []
    for method in spec["methods"]:
        test_methods.extend(generate_method_tests(method))

    tests_block = "\n".join(test_methods)
    file_content = TEST_FILE_TEMPLATE.format(
        spec_source=config.get("spec_path", "N/A"),
        module_name=module_name,
        test_methods=tests_block
    )

    out_dir = Path(config.get("output_dir", "tests/Module.Tests"))
    out_dir.mkdir(parents=True, exist_ok=True)
    output_file = out_dir / f"{module_name}Tests.Generated.cs"
    
    output_file.write_text(file_content, encoding="utf-8")
    print(f"[OK] Сгенерирован файл: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="C# NUnit Test Generator from YAML Spec")
    parser.add_argument("--config", default="config.yaml", help="Путь к config.yaml")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    with open(config['spec_path'], "r", encoding="utf-8") as f:
        spec_data = yaml.safe_load(f)

    render_and_save(spec_data, config)
    print("[OK] Готово.")
